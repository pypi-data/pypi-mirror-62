import logging
import multiprocessing
import time
from hashlib import sha1

from revscoring import Model, dependencies
from revscoring.dependencies import dig
from revscoring.extractors import Extractor
from revscoring.features import trim

logger = logging.getLogger(__name__)


class ScoringContext(dict):
    """
    Represents a context in which scoring can take place.  Usually, a wiki is
    1:1 with a "ScoringContext".

    :Parameters:
        name : str
           The name of the context in which scoring will happen.  This is
           usually a wiki's database name.
        model_map : dict
           A mapping between names and
           :class:`revscoring.ScorerModel`
           instances
        extractor : :class:`revscoring.Extractor`
           An extractor to use for gathering feature values
    """

    class ModelLoader:
        def load(self, config, key):
            return Model.from_config(config, key)

    def __init__(self, name, model_map, extractor):
        super().__init__()
        self.name = str(name)
        self.update(model_map)
        self.extractor = extractor

    def format_model_info(self, model_name, paths=None):
        model_info = self._get_model_info_for(model_name)
        return model_info.format(paths, formatting="json")

    def format_id_string(self, model_name, rev_id, request, injection_cache=None):
        version = self.model_version(model_name)
        score_id = ":".join(
            str(v) for v in [self.name, model_name, version, rev_id])
        if request.include_features:
            score_id += ":features"
        if injection_cache is None:
            return score_id
        else:
            sorted_tuple = tuple(sorted(injection_cache.items()))
            cache_hash = sha1(bytes(str(sorted_tuple), 'utf8')).hexdigest()
            return score_id + ":" + cache_hash

    def _get_model_info_for(self, model_name):
        return self[model_name].info

    def model_version(self, model_name):
        return self[model_name].version

    def model_features(self, model_name):
        return self[model_name].features

    def process_model_scores(self, model_names, root_cache,
                             include_features=False):
        """
        Generates a score map for a set of models based on a `root_cache`.
        This method performs no substantial IO, but may incur substantial CPU
        usage.

        :Parameters:
            model_names : `set` ( `str` )
                A set of models to score
            root_cache : `dict` ( `str` --> `mixed` )
                A cache of pre-computed root_dependencies for a specific
                revision.  See `extract_root_dependency_caches()`
            include_features : `bool`
                If True, include a map of basic features used in scoring along
                with the model score.  If False, just generate the scores.
        """
        model_scores = {}

        for model_name in model_names:
            model_scores[model_name] = {}

            # Mostly CPU
            model_scores[model_name]['score'] = \
                self._process_score(model_name, dependency_cache=root_cache)

            # Essentially free
            if include_features:
                base_feature_map = self._solve_base_feature_map(
                    model_name, dependency_cache=root_cache)
                model_scores[model_name]['features'] = base_feature_map

        return model_scores

    def _solve_features(self, model_name, dependency_cache=None):
        """
        Solves the vector (`list`) of features for a given model using
        the `dependency_cache` and returns them.
        """
        features = self[model_name].features
        return list(self.extractor.solve(features, cache=dependency_cache))

    def _solve_base_feature_map(self, model_name, dependency_cache=None):
        """
        Solves the leaf :class:`revscoring.Feature` from the dependency for
        `model_name` using `dependency_cache`.  This will return a mapping
        between the `str` name of the base features and the solved values.
        """
        features = list(trim(self[model_name].features))
        feature_values = self.extractor.solve(features, cache=dependency_cache)
        return {str(f): v
                for f, v in zip(features, feature_values)}

    def _process_score(self, model_name, dependency_cache=None):
        """
        Generates a score for a given model using the `dependency_cache`.
        """
        version = self[model_name].version

        start = time.time()
        feature_values = self._solve_features(model_name, dependency_cache)
        logger.debug("Extracted features for {0}:{1}:{2} in {3} secs"
                     .format(self.name, model_name, version,
                             round(time.time() - start, 3)))

        start = time.time()
        score = self[model_name].score(feature_values)
        logger.debug("Scored features for {0}:{1}:{2} in {3} secs"
                     .format(self.name, model_name, version,
                             round(time.time() - start, 3)))

        return score

    def _generate_root_datasources(self, model_names):
        for model_name in model_names:
            for dependency in dependencies.dig(self.model_features(model_name)):
                yield dependency

    def extract_root_dependency_caches(
            self, model_names, rev_ids, injection_caches=None):
        """
        Extracts a mapping of root :class:`revscoring.Datasource`
        capable of generating the features needed for a particular set of
        models without additional IO.  This method implements all of the IO
        heavy operations.  The roots dependency caches produced by calling
        this method can then be passed to `process_model_scores()` for scoring.

        :Parameters:
            model_names : `list` ( `str` )
                The names of a :class:`revscoring.ScorerModel` to
                extract the roots dependencies for
        """
        # Make a copy of injection_caches
        _injection_caches = {}
        for rev_id in rev_ids:
            injection_cache = injection_caches.get(rev_id, {}) \
                              if injection_caches is not None else {}
            _injection_caches[rev_id] = dict(injection_cache.items())

        # Find our root datasources
        root_datasources = \
            list(set(self._generate_root_datasources(model_names)))

        start = time.time()
        error_root_vals = self.extractor.extract(
            rev_ids, root_datasources, caches=_injection_caches)

        # Check each extraction for errors
        root_caches = {}
        errors = {}
        for rev_id, (error, values) in zip(rev_ids, error_root_vals):
            if error is not None:
                errors[rev_id] = error
                if rev_id in root_caches:
                    del root_caches[rev_id]
            else:
                root_caches[rev_id] = dict(zip(root_datasources, values))
                root_caches[rev_id].update(_injection_caches[rev_id])
        logger.debug("Extracted root datasources for {0}:{1}:{2} in {3} secs"
                     .format(self.name, set(model_names), rev_ids,
                             round(time.time() - start, 3)))

        # Note that root_caches should have been modified in place
        return root_caches, errors

    @classmethod
    def map_from_config(cls, config, context_names,
                        section_key="scoring_contexts"):
        """
        Loads a whole set of ScoringContext's from a configuration file
        while maintaining a cache of model names.  This aids in better memory
        management and allows model aliases to be implemented at the
        configuration level.

        :Returns:
            A map of context_names and ScoringContext's where models are loaded
            once and reused cross contexts.
        """
        model_key_map = {}
        context_map = {}
        model_loader = cls.ModelLoader()

        for context_name in context_names:
            section = config[section_key][context_name]
            model_map = {}
            for model_name, key in section['scorer_models'].items():
                if key in model_key_map:
                    scorer_model = model_key_map[key]
                else:
                    scorer_model = model_loader.load(config, key)
                    model_key_map[key] = scorer_model
                model_map[model_name] = scorer_model

            extractor = Extractor.from_config(config, section['extractor'])
            context_map[context_name] = cls(
                context_name, model_map=model_map, extractor=extractor)

        return context_map

    @classmethod
    def from_config(cls, config, name, section_key="scoring_contexts"):
        """
        Expects:

            scoring_contexts:
                enwiki:
                    scorer_models:
                        damaging: enwiki_damaging_2014
                        good-faith: enwiki_good-faith_2014
                    extractor: enwiki
                ptwiki:
                    scorer_models:
                        damaging: ptwiki_damaging_2014
                        good-faith: ptwiki_good-faith_2014
                    extractor: ptwiki

            extractors:
                enwiki_api: ...
                ptwiki_api: ...

            scorer_models:
                enwiki_damaging_2014: ...
                enwiki_good-faith_2014: ...
        """
        logger.info("Loading {0} '{1}' from config."
                    .format(cls.__name__, name))
        section = config[section_key][name]
        model_loader = cls.ModelLoader()

        model_map = {}
        for model_name, key in section['scorer_models'].items():
            scorer_model = model_loader.load(config, key)
            model_map[model_name] = scorer_model

        extractor = Extractor.from_config(config, section['extractor'])

        return cls(name, model_map=model_map, extractor=extractor)


class ServerScoringContext(ScoringContext):
    """
    A scoring context that is only capable of scoring.  This ScoringContext is
    intended to be used in clients where a web service (client) implements all
    of the model_info actions (e.g. :class:`ores.scoring_systems.CeleryQueue`).

    This ScoringContext saves on unnecessary memory usage, but still provides
    access to basic scoring functionality.
    """

    class ModelLoader:
        def load_model_and_queue(self, q, config, key):
            model = Model.from_config(config, key)
            model.info = None  # We don't need info on the server-side
            q.put(model)

        def load(self, config, key):
            logger.warning("Loading model {0} with sub-process".format(key))
            q = multiprocessing.Queue()
            p = multiprocessing.Process(
                target=self.load_model_and_queue, args=(q, config, key),
                daemon=True)
            p.start()
            model = q.get()
            p.join()
            return model

    def __init__(self, name, *args, **kwargs):
        logger.info("Loading {0} as a ServerScoringContext".format(name))
        super().__init__(name, *args, **kwargs)


class ClientScoringContext(ScoringContext):
    """
    A simplistic scoring context that is not capable of performing the scoring
    itself.  This ScoringContext is intended to be used in clients where an
    external service actually implements the scoring pattern
    (e.g. :class:`ores.scoring_systems.CeleryQueue`).  This ScoringContext
    saves on unnecessary memory usage, but still provides access to basic
    informational functionality.
    """

    class ModelLoader:
        def load_model_and_queue(self, q, config, key):
            model = Model.from_config(config, key)
            # Just return the model info and the root of the features
            q.put((model.info, list(dig(model.features))))

        def load(self, config, key):
            logger.warning("Loading model {0} with sub-process".format(key))
            q = multiprocessing.Queue()
            p = multiprocessing.Process(
                target=self.load_model_and_queue, args=(q, config, key),
                daemon=True)
            p.start()
            model_info, root_features = q.get()
            p.join()
            return model_info, root_features

    def __init__(self, name, model_map, *args, **kwargs):
        logger.info("Loading {0} as a ClientScoringContext".format(name))
        # Load an empty model map
        bare_model_map = {model_name: NotImplemented
                          for model_name, _ in model_map.items()}
        super().__init__(name, bare_model_map, *args, **kwargs)

        # Create an info map for use when formatting information
        self.info_map = {model_name: info
                         for model_name, (info, _) in model_map.items()}
        self.features_map = {model_name: root_features
                             for model_name, (_, root_features) in model_map.items()}

    def _get_model_info_for(self, model_name):
        return self.info_map[model_name]

    def model_version(self, model_name):
        return self.info_map[model_name].get("version")

    def model_features(self, model_name):
        return self.features_map[model_name]

    def process_score(self, *args, **kwargs):
        raise NotImplementedError()
