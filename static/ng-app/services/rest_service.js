var URLS = {
    'species': '/api/species/',
    'magnifications': '/api/magnifications/',
    'development_stages': '/api/development-stages/',
    'exp': '/api/experiments/',
    'probes': '/api/probes/',
    'exp_probes': '/api/experiment_probes/',
    'images': '/api/images/',
    'classify': '/api/classify/',
    'subregions': '/api/subregions/',
    'image_sets': '/api/image-sets/',
    'anatomy_probe_map': '/api/anatomy-probe-map/',
    'subregionanatomycount': '/api/subregion-anatomy-count',
    'train_model': '/api/train-model/'
};

var service = angular.module('IHCApp');

service.factory(
    'Species',
    function ($resource) {
        return $resource(
            URLS.species,
            {},
            {}
        );
    }
).factory(
    'Magnification',
    function ($resource) {
        return $resource(
            URLS.magnifications,
            {},
            {}
        );
    }
).factory(
    'DevelopmentStage',
    function ($resource) {
        return $resource(
            URLS.development_stages,
            {},
            {}
        );
    }
).factory(
    'SubregionAnatomyCount',
    function ($resource) {
        return $resource(
            URLS.subregionanatomycount,
            {},
            {}
        );
    }
).factory(
    'Experiment',
    function ($resource) {
        return $resource(
            URLS.exp + ':experiment_id',
            {},
            {}
        );
    }
).factory(
    'ImageSet',
    function ($resource) {
        return $resource(
            URLS.image_sets + ':image_set_id',
            {},
            {}
        );
    }
).factory(
    'Probe',
    function ($resource) {
        return $resource(
            URLS.probes,
            {},
            {}
        );
    }
).factory(
    'ExperimentProbe',
    function ($resource) {
        return $resource(
            URLS.exp_probes + ':experiment_probe_id',
            {},
            {}
        );
    }
).factory(
    'AnatomyProbeMap',
    function ($resource) {
        return $resource(
            URLS.anatomy_probe_map,
            {},
            {}
        );
    }
).factory('Classify',
    function($resource) {
        return $resource(
            URLS.classify,
            {},
            {}
        );
    }
).factory(
    'Subregion',
    function($resource) {
        return $resource(
            URLS.subregions + ':id',
            {},
            {
                save: {
                    method: 'POST',
                    isArray: true
                }
            }
        );
    }
).factory(
    'Image',
    function ($resource) {
        return  $resource(
            URLS.images + ':id',
            {},
            {}
        );
    }
).factory(
    'TrainModel',
    function ($resource) {
        return  $resource(
            URLS.train_model,
            {},
            {}
        );
    }
);
