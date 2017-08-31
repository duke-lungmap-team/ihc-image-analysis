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
        'Magnification',
        'DevelopmentStage',
        'Probe',
        function ($scope, $q, ImageSet, Species, Magnification, DevelopmentStage, Probe) {
            $scope.species = [];
            $scope.magnifications = [];
            $scope.development_stages = [];
            $scope.probes = [];
            $scope.image_sets = [];
            $scope.retrieving_data = false;

            var species = Species.query();
            species.$promise.then(function (data) {
                data.forEach(function (s) {
                    $scope.species.push(
                        {
                            'name': s,
                            'query': false
                        }
                    )
                });
            });

            var magnifications = Magnification.query();
            magnifications.$promise.then(function (data) {
                data.forEach(function (m) {
                    $scope.magnifications.push(
                        {
                            'name': m,
                            'query': false
                        }
                    )
                });
            });

            var development_stages = DevelopmentStage.query();
            development_stages.$promise.then(function (data) {
                data.forEach(function (d) {
                    $scope.development_stages.push(
                        {
                            'name': d,
                            'query': false
                        }
                    )
                });
            });

            var probes = Probe.query();
            probes.$promise.then(function (data) {
                data.forEach(function (p) {
                    $scope.probes.push(
                        {
                            'id': p.id,
                            'name': p.label,
                            'query': false
                        }
                    )
                });
            });

            $scope.filter_image_sets = function () {
                $scope.retrieving_data = true;
                $scope.image_sets = [];

                var species_filters = [];
                $scope.species.forEach(function (s) {
                    if (s.query) {
                        species_filters.push(s.name);
                    }
                });

                var mag_filters = [];
                $scope.magnifications.forEach(function (m) {
                    if (m.query) {
                        mag_filters.push(m.name);
                    }
                });

                var dev_stage_filters = [];
                $scope.development_stages.forEach(function (d) {
                    if (d.query) {
                        dev_stage_filters.push(d.name);
                    }
                });

                var probe_filters = [];
                $scope.probes.forEach(function (p) {
                    if (p.query) {
                        probe_filters.push(p.id);
                    }
                });

                $scope.image_sets = ImageSet.query(
                    {
                        'species': species_filters,
                        'magnification': mag_filters,
                        'development_stage': dev_stage_filters,
                        'probe': probe_filters
                    }
                );

                $scope.image_sets.$promise.then(function (data) {
                    $scope.retrieving_data = false;
                }, function (error) {
                    $scope.retrieving_data = false;
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
        'ImageSet',
        'Image',
        'Subregion',
        'ExperimentProbe',
        'AnatomyProbeMap',
        'Classify',
        'TrainModel',
        function ($scope, $q, $routeParams, $window, ImageSet, Image,
                  Subregion, ExperimentProbe, AnatomyProbeMap, Classify, TrainModel) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_classification = null;
            $scope.mode = 'train';  // can be 'train', or 'classify'

            // drw-poly vars
            $scope.enabled = false;
            $scope.regions = {
                'svg': []
            };
            $scope.poly_height = 997;
            $scope.poly_width = 997;

            $scope.image_set = ImageSet.get({'image_set_id': $routeParams.image_set_id});

            $scope.image_set.$promise.then(function(data) {
                $scope.images = Image.query({'image_set': data.id});
                var anatomy_promises = [];

                data.probes.forEach(function(probe) {
                    anatomy_promises.push(AnatomyProbeMap.query(
                        {
                            'probe': probe.probe
                        }).$promise
                    );
                });

                $q.all(anatomy_promises).then(function(results) {
                    $scope.anatomies = [];

                    results.forEach(function(anatomy_probe_map) {
                        anatomy_probe_map.forEach(function(anatomy_probe) {
                            $scope.anatomies.push(
                                {
                                    'id': anatomy_probe.anatomy,
                                    'name': anatomy_probe.anatomy_name
                                }
                            );
                        });
                    });
                }, function(error) {
                    // Error callback where reason is the value of the first rejected promise
                    $window.alert(JSON.stringify(error, null, 4));
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
                        $scope.selected_image = data;
                        $scope.select_classification($scope.selected_classification);
                    }, function (error) {
                        // TODO: figure out how to turn retrieving off for experiment
                        $window.alert(JSON.stringify(error, null, 4))
                    });
                } else {
                    $scope.select_classification($scope.selected_classification);
                }
            };

            $scope.select_classification = function(classification) {
                $scope.selected_classification = classification;

                if ($scope.selected_classification === null) {
                    return false;
                }

                var existing_sub_regions = Subregion.query(
                    {
                        'image': $scope.selected_image.id,
                        'anatomy': classification.id
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

                        region.anatomy = $scope.selected_classification.id;
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
                        'imageset': $scope.image_set.id
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
