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
        '$q',
        'LungMapExperiment',
        'Experiment',
        function ($scope, $q, LungMapExperiment, Experiment) {
            var lm_experiments = LungMapExperiment.query({});
            var experiments = Experiment.query({});

            // wait for both experiment lists to resolve,
            // then build combined list
            $q.all([
                lm_experiments.$promise,
                experiments.$promise
            ]).then(function (results) {
                $scope.all_experiments = {};

                results[0].forEach(function(exp) {
                    $scope.all_experiments[exp] = {
                        'retrieved': false
                    }
                });

                results[1].forEach(function(exp) {
                    if ($scope.all_experiments.hasOwnProperty(exp.experiment_id)) {
                        $scope.all_experiments[exp.experiment_id].retrieved = true;
                        $scope.all_experiments[exp.experiment_id].retrieving = false;
                    }
                });

            });

            $scope.retrieve_experiment = function (exp_id) {
                $scope.all_experiments[exp_id].retrieving = true;

                var save_response = Experiment.save(
                    {
                        'experiment_id': exp_id
                    }
                );

                save_response.$promise.then(function(data) {
                    $scope.all_experiments[data.experiment_id].retrieved = true;
                    $scope.all_experiments[data.experiment_id].retrieving = false;
                }, function (error) {
                    // TODO: figure out how to turn retrieving off for experiment
                });
            };
        }
    ]
);

app.controller(
    'ExperimentDetailController',
    [
        '$scope',
        '$q',
        '$routeParams',
        'Experiment',
        'Image',
        function ($scope, $q, $routeParams, Experiment, Image) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.mode = 'view';  // can be 'view', 'train', or 'classify'

            $scope.experiment = Experiment.get(
                {
                    'experiment_id': $routeParams.experiment_id
                }
            );

            $scope.experiment.$promise.then(function (data) {
                $scope.images = Image.query({experiment: $routeParams.experiment_id});

                $scope.images.$promise.then(function (data) {
                    console.log('adf');
                });

            });

            $scope.image_selected = function(img) {
                $scope.selected_image = img;
            }

        }
    ]
);
