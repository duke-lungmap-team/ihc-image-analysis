var URLS = {
    'lm_exp': '/api/lungmapexperiments/',
    'exp': '/api/experiments/'
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
            URLS.exp + ':id',
            {},
            {}
        );
    }
);
