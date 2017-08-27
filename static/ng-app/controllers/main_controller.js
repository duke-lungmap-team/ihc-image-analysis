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
        'ImageSet',
        'Species',
        function ($scope, $q, ImageSet, Species) {
            $scope.species = Species.query();

            var image_set_counts = ImageSet.query({});

            image_set_counts.$promise.then(function(results) {
                $scope.imagesetscounts = [];
                results.forEach(function(result) {
                    var temp = {};
                    temp['image_set_name'] = result['image_set_name'];
                    temp['id'] = result['id'];
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

            // drw-poly vars
            $scope.enabled = false;
            $scope.regions = {
                'svg': []
            };
            $scope.poly_height = 997;
            $scope.poly_width = 997;

            var imageset = ImageSet.get({'image_set_id': $routeParams.image_set_id});

            imageset.$promise.then(function(data) {
                $scope.anatomies = [];
                $scope.animageset = data;
                data.probes.forEach(function(probe) {
                    $scope.anatomies.push(AnatomyByProbe.get(
                        {
                            'probe_id': probe.probe
                        }).$promise
                    );
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
                        $scope.regions.svg = new_regions;
                        $scope.enabled = false;
                    } else {
                        $scope.regions.svg = [];
                        $scope.enabled = true;
                    }
                });
            };

            $scope.set_mode = function (mode) {
                $scope.mode = mode;
                $scope.regions.svg = [];

                if (mode === 'classify') {
                    $scope.enabled = true;
                } else if (mode === 'train') {
                    if ($scope.selected_classification !== null) {
                        $scope.select_classification($scope.selected_classification);
                    }
                } else {
                    $scope.enabled = false;
                }
            };

            $scope.post_regions = function () {
                // will post all the regions for this classification in bulk,
                // since there cannot be any existing regions for the image / class combo.
                var regions = [];

                if ($scope.regions.svg.length === 0) {
                    $window.alert('There are no regions drawn, please segment something first.');
                } else if ($scope.selected_classification === null) {
                    $window.alert('There is no label associated with the active polygon, please choose a label first.');
                } else {
                    $scope.regions.svg.forEach(function(p) {
                        var region = {};
                        var region_points = [];

                        //Get points
                        for (var i = 0; i < p.length; i++) {
                            region_points.push(
                                {
                                    "x": p[i][0],
                                    "y": p[i][1],
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
                            $scope.regions.svg = new_regions;
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
                var classify_promises = [];

                $scope.regions.svg.forEach(function (region) {
                    var payload = {};
                    var points = [];

                    //Get points
                    for (var i = 0; i < region.length; i++) {
                        points.push(
                            {
                                "x": region[i][0],
                                "y": region[i][1],
                                "order": i
                            }
                        );
                    }
                    payload.image_id = $scope.selected_image.id;
                    payload.points = points;

                    // How to get results of post to conditionally get ready for next
                    classify_promises.push(Classify.save(payload).$promise);
                });

                $q.all(classify_promises).then(function (results) {
                    console.log(results);
                    $window.alert(JSON.stringify(results, null, 4));
                });
            }
        }
    ]
);
