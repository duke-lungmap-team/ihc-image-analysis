app.controller(
    'MainController',
    [
        '$scope',
        function ($scope) {
            // placeholder
        }
    ]
);

app.controller(
    'ExperimentListController',
    [
        '$scope',
        'LungMapExperiment',
        function ($scope, LungMapExperiment) {
            $scope.lm_experiments = LungMapExperiment.query({});
        }
    ]
);
