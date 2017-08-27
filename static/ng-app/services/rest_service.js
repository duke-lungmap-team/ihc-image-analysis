var URLS = {
    'species': '/api/species/',
    'magnifications': '/api/magnifications/',
    'lm_exp': '/api/lungmapexperiments/',
    'exp': '/api/experiments/',
    'probes': '/api/probes/',
    'exp_probes': '/api/experiment_probes/',
    'images': '/api/images/',
    'classify': '/api/classify/',
    'subregion': '/api/subregion/',
    'image_sets': '/api/image-sets/',
    'anatomybyprobe': '/api/anatomybyprobe/',
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
    'LungMapExperiment',
    function ($resource) {
        return $resource(
            URLS.lm_exp + ':id',
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
            URLS.probes + ':probe_id',
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
    'AnatomyByProbe',
    function ($resource) {
        return $resource(
            URLS.anatomybyprobe + ':probe_id',
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
            URLS.subregion,
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
