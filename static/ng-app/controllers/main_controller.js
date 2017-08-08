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
        'ImagesetSubregionCount',
        function ($scope, $q, ImagesetSubregionCount) {
            $scope.tempers = ImagesetSubregionCount;
            var imagesetcounts = ImagesetSubregionCount.query({});

            imagesetcounts.$promise.then((results) => {
                $scope.imagesetscounts = []
                results.forEach((result) => {
                    var temp = {}
                    temp['imageset_name'] = result['imageset_name']
                    temp['imageset_id'] = result['imageset_id']
                    var image_count = 0
                    var image_subregion_count = 0
                    var subregion_count=0
                    result['images'].forEach((image) =>{
                        image_count+=1
                        if (image.subregion_count>0) {
                            image_subregion_count+=1
                            subregion_count+=image.subregion_count
                        }

                    })
                    temp['image_count'] = image_count;
                    temp['image_subregion_count'] = image_subregion_count;
                    temp['subregion_count'] = subregion_count;
                    $scope.imagesetscounts.push(temp);
                })
            })
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
        'AnatomyByProbe',
        function ($scope, $q, $routeParams, $window, Imagesets, Image,
                  Classification, Subregion, ExperimentProbe, AnatomyByProbe) {
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
            // $scope.classifications = Classification.query();
            $scope.tester = AnatomyByProbe;


            var imageset = Imagesets.get({'imagesets_id': $routeParams.imagesets_id});

            imageset.$promise.then((data) => {
                $scope.anatomies = [];
                $scope.animageset = data
                angular.forEach(data.probes, (probe) => {
                    $scope.anatomies.push(AnatomyByProbe.get({'probe_id': probe.probe}).$promise)

                })

                $q.all($scope.anatomies).then(function (results) {
                    $scope.anatomies_now = [];
                    results.forEach(function(exp) {
                        $scope.anatomies_now.push.apply($scope.anatomies_now, exp.anatomies);
                    });

                    }, function(reason) {
                        // Error callback where reason is the value of the first rejected promise
                        $window.alert(JSON.stringify(reason, null, 4));
                });
            })




            $scope.image_selected = function(img) {
                $scope.selected_image = img;
                if (!img.image_orig_sha1) {
                    var save_response = Image.get(
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

            $scope.zqwsd = Subregion;

            $scope.post_regions = function () {
                // placeholder
                var thesepoints = $scope.points[$scope.activePolygon];

                if (thesepoints.length === 0) {
                    $window.alert('The current polygon has no points selected, please segment something first.');
                } else if ($scope.selected_subregion === null) {
                    $window.alert('There is no label associated with the active polygon, please choose a label first.');
                } else {
                    //TODO check logic here to ensure that I'm grabbing correct points
                    var payload = {};
                    var points = [];
                    //Get points
                    for (var i = 0; i < thesepoints.length; i++) {
                        points.push(
                            {
                                "x": thesepoints[i][2],
                                "y": thesepoints[i][3],
                                "order": i
                            }
                        );
                    }
                    payload.anatomy = $scope.selected_subregion.anatomy_id;
                    payload.image = $scope.selected_image.id;
                    payload.points = points;

                    //How to get results of post to conditionally get ready for next
                    var newregion = Subregion.save(payload);
                    $scope.add();
                    $scope.selected_subregion = null;

                }
            }

        }
    ]
);
