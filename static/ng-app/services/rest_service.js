var URLS = {
    'lm_exp': '/api/lungmapexperiments/',
    'exp': '/api/experiments/',
    'probes': '/api/probes/',
    'exp_probes': '/api/experiment_probes/',
    'images': '/api/images/',
    'classifications': '/api/classifications/'
};

var service = angular.module('IHCApp');

service.factory(
    'LungMapExperiment',
    function ($resource) {
        return $resource(
            URLS.lm_exp + ':id',
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
).factory('Classification',
    function($resource) {
        return $resource(
            URLS.classifications + ':id',
            {},
            {}
        );
    }
).factory('Image', function ($resource) {
        return  $resource(
            URLS.images + ':id',
            {},
            {}
        );
});
