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
    'ModalInstanceCtrl',
    function ($scope, $uibModalInstance, title, message_items) {
        $scope.title = title;
        $scope.items = message_items;

        $scope.ok = function () {
            $uibModalInstance.close(true);
        };

        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        };
    }
);

app.controller(
    'ImageSetListController',
    [
        '$scope',
        'ImageSet',
        'Species',
        'Magnification',
        'DevelopmentStage',
        'Probe',
        function ($scope, ImageSet, Species, Magnification, DevelopmentStage, Probe) {
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
    'ImageSetDetailController',
    [
        '$scope',
        '$q',
        '$routeParams',
        '$uibModal',
        'ImageSet',
        'Image',
        'Subregion',
        'AnatomyProbeMap',
        'Classify',
        'TrainModel',
        function ($scope, $q, $routeParams, $uibModal, ImageSet, Image,
                  Subregion, AnatomyProbeMap, Classify, TrainModel) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_classification = null;
            $scope.mode = 'train';  // can be 'train', or 'classify'
            $scope.currently_training = false; //boolean for UI to know if backend is training a model

            // drw-poly vars
            $scope.enabled = false;
            $scope.regions = {
                'svg': []
            };
            $scope.poly_height = 997;
            $scope.poly_width = 997;

            // modal setup
            $scope.modal_title = null;
            $scope.modal_items = null;
            $scope.animationsEnabled = true;
            $scope.open_modal = function (size, template_type, confirm_callback) {
                var template_url;

                if (template_type === 'confirm') {
                    template_url = 'static/ng-app/partials/confirm-modal.html';
                } else {
                    template_url = 'static/ng-app/partials/generic-modal.html';
                }

                var modalInstance = $uibModal.open(
                    {
                        animation: $scope.animationsEnabled,
                        templateUrl: template_url,
                        controller: 'ModalInstanceCtrl',
                        size: size,
                        resolve: {
                            title: function() {
                                return $scope.modal_title;
                            },
                            message_items: function () {
                                return $scope.modal_items;
                            }
                        }
                    }
                );

                modalInstance.result.then(function (selectedItem) {
                    if (selectedItem && confirm_callback != undefined) {
                        confirm_callback();
                    }
                });
            };

            $scope.launch_info_modal = function() {
                $scope.modal_title = 'How to Use the Segmentation Tool';
                $scope.modal_items = [
                    "- If training, ensure that an anatomical structure is selected from the drop down menu",
                    "- Using the mouse, left-click around the anatomical structure you are segmenting",
                    "- Lines connecting the points will automatically be drawn",
                    "- If you make a mistake, use the right-click button to remove a point",
                    "- You can also left-click, hold, and drag points to manipulate their placement",
                    "- Once finished, simply hit return and focus will be taken away from the created polygon",
                    "- Now, you can begin segmenting another structure (following the same procedure as above)",
                    "- Or, if you have segmented all subregions, you can click the 'Save Regions' button when training",
                    "- If classifing regions click 'Classify Region' when segmentation is complete"
                ];
                $scope.open_modal();
            };

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

                    if (new_regions.length > 0 || $scope.image_set.trainedmodel !== null) {
                        $scope.regions.svg = new_regions;
                        $scope.enabled = false;
                        $scope.displaying_saved_regions = true;
                    } else {
                        $scope.regions.svg = [];
                        $scope.enabled = true;
                        $scope.displaying_saved_regions = false;
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
                    } else {
                        $scope.enabled = false;
                    }
                } else {
                    $scope.enabled = false;
                }
            };

            $scope.post_regions = function () {
                // will post all the regions for this classification in bulk,
                // since there cannot be any existing regions for the image / class combo.
                var regions = [];

                if ($scope.regions.svg.length < 4) {
                    $scope.modal_title = 'Error';
                    $scope.modal_items = [
                        'A minimum of 4 items per class must be drawn'
                    ];
                    $scope.open_modal();
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
                            $scope.displaying_saved_regions = true;
                            $scope.image_set = ImageSet.get(
                                {
                                    'image_set_id': $routeParams.image_set_id
                                }
                            );
                        }
                    }, function (error) {
                        $scope.modal_title = 'Error';
                        $scope.modal_items = ['An error occured when attempting to save regions'];
                        $scope.open_modal();
                    });
                }
            };

            $scope.delete_saved_regions = function () {
                var delete_response = Subregion.delete({
                    'image': $scope.selected_image.id,
                    'anatomy': $scope.selected_classification.id
                });

                delete_response.$promise.then(function (data) {
                    // update the image set to refresh the region counts
                    var image_set_response = $scope.image_set = ImageSet.get(
                        {
                            'image_set_id': $routeParams.image_set_id
                        }
                    );

                    image_set_response.$promise.then(function (image_set_data) {
                        // reset mode to clear regions
                        $scope.set_mode($scope.mode);
                    });
                }, function (error) {
                    $scope.modal_title = 'Error';
                    $scope.modal_items = [error.data['detail']];
                    $scope.open_modal();
                });
            };

            $scope.train_model = function () {
                $scope.currently_training = true;
                var response = TrainModel.save(
                    {
                        'imageset': $scope.image_set.id
                    }
                );

                response.$promise.then(function (data) {
                    var response2 = ImageSet.get(
                        {
                            'image_set_id': $routeParams.image_set_id
                        }
                    );
                    //TODO: attempting to make the transition from delete to train not 'jump'
                    response2.$promise.then(function(data) {
                        $scope.image_set = data;
                        $scope.currently_training = false;

                        }
                    );
                }, function (error) {
                    $scope.currently_training = false;
                    $scope.modal_title = 'Error';
                    $scope.modal_items = [error.data['detail']];
                    $scope.open_modal();
                });
            };

            $scope.launch_delete_trained_model_modal = function() {
                $scope.modal_title = 'Delete Trained Model?';
                $scope.modal_items = ['Are you sure you want to delete this trained model?'];
                $scope.open_modal('md', 'confirm', delete_trained_model);
            };

            function delete_trained_model() {
                var response = TrainModel.delete(
                    {
                        'id': $scope.image_set.trainedmodel
                    }
                );

                response.$promise.then(function (data) {
                    $scope.image_set = ImageSet.get(
                        {
                            'image_set_id': $routeParams.image_set_id
                        }
                    );
                });
            }

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
                    $scope.modal_title = 'Classification Results';
                    $scope.modal_items = [];
                    results[0].results.forEach(function(r) {
                        $scope.modal_items.push(Object.keys(r)[0] + ': ' + (r[Object.keys(r)[0]] * 100).toFixed(2) + '%');
                    });
                    $scope.open_modal();
                });
            }
        }
    ]
);
