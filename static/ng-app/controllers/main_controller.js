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
            var image_set_counts = ImagesetSubregionCount.query({});

            image_set_counts.$promise.then(function(results) {
                $scope.imagesetscounts = [];
                results.forEach(function(result) {
                    var temp = {};
                    temp['imageset_name'] = result['imageset_name'];
                    temp['imageset_id'] = result['imageset_id'];
                    var image_count = 0;
                    var image_subregion_count = 0;
                    var subregion_count=0;
                    result['images'].forEach(function(image) {
                        image_count += 1;
                        if (image.subregion_count>0) {
                            image_subregion_count+=1;
                            subregion_count+=image.subregion_count
                        }
                    });
                    temp['image_count'] = image_count;
                    temp['image_subregion_count'] = image_subregion_count;
                    temp['subregion_count'] = subregion_count;
                    $scope.imagesetscounts.push(temp);
                })
            });
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
        'ImageSet',
        'Image',
        'Subregion',
        'ExperimentProbe',
        'AnatomyByProbe',
        'Classify',
        'TrainModel',
        function ($scope, $q, $routeParams, $window, ImageSet, Image,
                  Subregion, ExperimentProbe, AnatomyByProbe, Classify, TrainModel) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_classification = null;
            $scope.mode = 'view';  // can be 'view', 'train', or 'classify'

            // training mode vars
            $scope.enabled = false;
            $scope.colorArray = ['#00FF00'];
            $scope.activePolygon = 0;
            $scope.regions = {
                'points': [[]]
            };
            $scope.new_points = [];
            $scope.label = [[]];
            $scope.poly_height = 862;
            $scope.poly_width = 862;
            $scope.tester = AnatomyByProbe;

            var imageset = ImageSet.get({'image_set_id': $routeParams.image_set_id});

            imageset.$promise.then(function(data) {
                $scope.anatomies = [];
                $scope.animageset = data;
                data.probes.forEach(function(probe) {
                    $scope.anatomies.push(AnatomyByProbe.get(
                        {'probe_id': probe.probe}).$promise
                    )
                });

                $q.all($scope.anatomies).then(function (results) {
                    $scope.anatomies_now = [];
                    results.forEach(function(exp) {
                        $scope.anatomies_now.push.apply($scope.anatomies_now, exp.anatomies);
                    });

                    }, function(reason) {
                        // Error callback where reason is the value of the first rejected promise
                        $window.alert(JSON.stringify(reason, null, 4));
                });
            });

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

            $scope.select_classification = function(classification) {
                $scope.selected_classification = classification;

                var existing_sub_regions = Subregion.query(
                    {
                        'image': $scope.selected_image.id,
                        'anatomy': classification.anatomy_id
                    }
                );

                var new_regions = [];
                var new_region_points =[];

                existing_sub_regions.$promise.then(function(data) {
                    data.forEach(function(region) {
                        // empty array for our new region
                        new_region_points = [];

                        region.points.forEach(function(p) {
                            new_region_points.push(
                                [
                                    p.x,
                                    p.y
                                ]
                            );
                        });

                        new_regions.push(new_region_points);
                    });

                    if (new_regions.length > 0) {
                        $scope.activePolygon = -1;
                        $scope.new_points = new_regions;
                        $scope.enabled = false;
                    } else {
                        $scope.activePolygon = -1;
                        $scope.regions.points.splice(0, $scope.regions.points.length);
                        $scope.enabled = true;
                        $scope.add();
                    }
                });
            };

            $scope.set_mode = function (mode) {
                $scope.mode = mode;
            };

            $scope.undo = function(){
                if ($scope.enabled) {
                    $scope.regions.points[$scope.activePolygon].splice(-1, 1);
                }
            };

            $scope.clearAll = function(){
                $scope.regions.points[$scope.activePolygon] = [];
            };

            $scope.removePolygon = function (index) {
                $scope.regions.points.splice(index, 1);
                if(index <= $scope.activePolygon) {
                    --$scope.activePolygon;
                }
            };

            $scope.add = function (index) {
                if (!$scope.enabled) {
                    return false;
                }
                $scope.regions.points.push([]);
                $scope.activePolygon = $scope.regions.points.length - 1;
            };

            $scope.delete_all_regions = function () {
                $scope.$broadcast("ngAreas:remove_all");
            };

            $scope.post_regions = function () {
                // will post all the regions for this classification in bulk,
                // since there cannot be any existing regions for the image / class combo.
                var regions = [];

                if ($scope.regions.points.length === 0) {
                    $window.alert('There are no regions drawn, please segment something first.');
                } else if ($scope.selected_classification === null) {
                    $window.alert('There is no label associated with the active polygon, please choose a label first.');
                } else {
                    $scope.regions.points.forEach(function(p) {
                        var region = {};
                        var region_points = [];

                        //Get points
                        for (var i = 0; i < p.length; i++) {
                            region_points.push(
                                {
                                    "x": p[i][2],
                                    "y": p[i][3],
                                    "order": i
                                }
                            );
                        }

                        region.anatomy = $scope.selected_classification.anatomy_id;
                        region.image = $scope.selected_image.id;
                        region.points = region_points;

                        regions.push(region)
                    });

                    // How to get results of post to conditionally get ready for next
                    var post_region_response = Subregion.save(regions);

                    var new_regions = [];
                    var new_region_points =[];

                    post_region_response.$promise.then(function(data) {
                        data.forEach(function(region) {
                            // empty array for our new region
                            new_region_points = [];

                            region.points.forEach(function(p) {
                                new_region_points.push(
                                    [
                                        p.x,
                                        p.y
                                    ]
                                );
                            });

                            new_regions.push(new_region_points);
                        });

                        if (new_regions.length > 0) {
                            $scope.activePolygon = -1;
                            $scope.new_points = new_regions;
                            $scope.enabled = false;
                        }
                    }, function (error) {
                        $window.alert(JSON.stringify(error.data, null, 4))
                    });
                }
            };

            $scope.train_model = function () {
                TrainModel.save(
                    {
                        'imageset': imageset.id
                    }
                );
            };

            $scope.classify_region = function () {
                var thesepoints = $scope.regions.points[$scope.activePolygon];

                if (thesepoints.length === 0) {
                    $window.alert('The current polygon has no points selected, please segment something first.');
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
                    payload.image_id = $scope.selected_image.id;
                    payload.points = points;

                    //How to get results of post to conditionally get ready for next
                    var classified_region = Classify.save(payload);
                    classified_region.$promise.then(function(results) {
                        $window.alert(JSON.stringify(results, null, 4))
                    });
                }
            }
        }
    ]
);
