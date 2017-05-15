var URLS = {
    'lm_exp': '/api/lungmapexperiments/',
    'exp': '/api/experiments/',
    'probes': '/api/probes/',
    'images': '/api/images/'
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
).factory('Image', function ($resource) {
        return  $resource(
            URLS.images + ':id',
            {},
            {}
        );
});
