var URLS = {
    'LMExp': '/api/lungmapexperiments/'
};

var service = angular.module('IHCApp');

service.factory(
    'LungMapExperiment',
    function ($resource) {
        return $resource(
            URLS.LMExp + ':id',
            {},
            {}
        );
    }
);
