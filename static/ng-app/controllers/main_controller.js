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
        'Classification',
        'ExperimentProbe',
        function ($scope, $q, $routeParams, Experiment, Image, Classification, ExperimentProbe) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_subregion = null;
            $scope.mode = 'view';  // can be 'view', 'train', or 'classify'

            // training mode vars
            $scope.enabled = true;
            $scope.colorArray = ['#00FF00'];
            $scope.activePolygon = 0;
            $scope.points = [[]];
            $scope.poly_height = 862;
            $scope.poly_width = 862;
            $scope.classifications = Classification.query();


            $scope.experiment = Experiment.get(
                {
                    'experiment_id': $routeParams.experiment_id
                }
            );


            $scope.experiment.$promise.then(function (data) {
                $scope.images = Image.query({experiment: $routeParams.experiment_id});
                $scope.probes = ExperimentProbe.query({experiment: $routeParams.experiment_id});
            });

            $scope.image_selected = function(img) {
                $scope.selected_image = img;
            };

            $scope.select_subregion = function(classification) {
                $scope.selected_subregion = classification;
            }

            $scope.set_mode = function (mode) {
                $scope.mode = mode;
            };

            $scope.undo = function(){
                $scope.points[$scope.activePolygon].splice(-1, 1);
            };

            $scope.clearAll = function(){
                $scope.points[$scope.activePolygon] = [];
            };

            $scope.removePolygon = function (index) {
                $scope.points.splice(index, 1);
                if(index <= $scope.activePolygon) {
                    --$scope.activePolygon;
                }
                if ($scope.points.length === 0) {
                    $scope.enabled = false;
                }
            };

            $scope.add = function (index) {
                $scope.enabled = true;
                $scope.points.push([]);
                $scope.activePolygon = $scope.points.length - 1;
            };

            $scope.delete_all_regions = function () {
                $scope.$broadcast("ngAreas:remove_all");
            };

            $scope.post_regions = function () {
                // placeholder
            };

        }
    ]
);


app.controller(
    'ProbeListController',
    [
        '$scope',
        '$q',
        'Probe',
        function ($scope, $q, Probe) {
            $scope.probes = Probe.query({});
        }
    ]
);