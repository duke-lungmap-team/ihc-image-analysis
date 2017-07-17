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
        'Imagesets',
        function ($scope, $q, LungMapExperiment, Experiment, Imagesets) {
            $scope.imagesetsresults = Imagesets.query({});

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
        '$window',
        'Imagesets',
        'Image',
        'Classification',
        'Subregion',
        'ExperimentProbe',
        function ($scope, $q, $routeParams, $window, Imagesets, Image, Classification, Subregion, ExperimentProbe) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_subregion = null;
            $scope.mode = 'view';  // can be 'view', 'train', or 'classify'

            // training mode vars
            $scope.enabled = true;
            $scope.colorArray = ['#00FF00'];
            $scope.activePolygon = 0;
            $scope.points = [[]];
            $scope.label = [[]];
            $scope.poly_height = 862;
            $scope.poly_width = 862;
            $scope.classifications = Classification.query();

            $scope.test = Image;


            $scope.animageset = Imagesets.get(
                {
                    'imagesets_id': $routeParams.imagesets_id
                }
            );


            // $scope.experiment.$promise.then(function (data) {
            //     $scope.images = Image.query({experiment: $routeParams.experiment_id});
            //     $scope.probes = ExperimentProbe.query({experiment: $routeParams.experiment_id});
            // });
            //
            $scope.image_selected = function(img) {
                $scope.selected_image = img;
                if (!img.image_jpeg) {
                    $window.alert(img.id);
                    var save_response = Image.save(
                        {
                            'id': img.id
                        },
                        {}
                    );

                    save_response.$promise.then(function(data) {
                        $scope.selected_image = data
                    }, function (error) {
                        // TODO: figure out how to turn retrieving off for experiment
                        $window.alert(JSON.stringify(error, null, 4))
                    });
                }

            };
            //
            // $scope.select_subregion = function(classification) {
            //     $scope.selected_subregion = classification;
            // }
            //
            $scope.set_mode = function (mode) {
                $scope.mode = mode;
            };
            //
            // $scope.undo = function(){
            //     $scope.points[$scope.activePolygon].splice(-1, 1);
            // };
            //
            // $scope.clearAll = function(){
            //     $scope.points[$scope.activePolygon] = [];
            // };
            //
            // $scope.removePolygon = function (index) {
            //     $scope.points.splice(index, 1);
            //     if(index <= $scope.activePolygon) {
            //         --$scope.activePolygon;
            //     }
            //     if ($scope.points.length === 0) {
            //         $scope.enabled = false;
            //     }
            // };
            //
            // $scope.add = function (index) {
            //     $scope.enabled = true;
            //     $scope.points.push([]);
            //     $scope.activePolygon = $scope.points.length - 1;
            // };
            //
            // $scope.delete_all_regions = function () {
            //     $scope.$broadcast("ngAreas:remove_all");
            // };
            //
            // $scope.zqwsd = Subregion;
            //
            // $scope.post_regions = function () {
            //     // placeholder
            //     var thesepoints = $scope.points[$scope.activePolygon];
            //
            //     if (thesepoints.length === 0) {
            //         $window.alert('The current polygon has no points selected, please segment something first.');
            //     }
            //
            //     if ($scope.selected_subregion === null) {
            //         $window.alert('There is no label associated with the active polygon, please choose a label first.');
            //     }
            //
            //     //TODO check logic here to ensure that I'm grabbing correct points
            //     var payload = {};
            //     var points = [];
            //     //Get points
            //     for (var i=0; i<thesepoints.length; i++) {
            //         points.push(
            //             {
            //                 "x": thesepoints[i][2],
            //                 "y": thesepoints[i][3],
            //                 "order": i
            //             }
            //         );
            //     }
            //     payload.classification = $scope.selected_subregion.id;
            //     payload.image = $scope.selected_image.id;
            //     payload.points = points;
            //
            //     //How to get results of post to conditionally get ready for next
            //     var newregion = Subregion.save(payload);
            //     $scope.add();
            //     $scope.selected_subregion = null;
            //
            // };

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