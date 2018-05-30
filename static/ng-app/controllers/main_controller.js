app.controller(
    'MainController',
    [
        '$scope',
        '$window',
        '$uibModal',
        'Idle',
        'Keepalive',
        'Heartbeat',
        function ($scope, $window, $uibModal, Idle, Keepalive, Heartbeat) {
            // Setup ng-idle for monitoring user's session timeout
            $scope.$on('IdleStart', function() {
                open_session_timeout_modal();
            });

            $scope.$on('IdleTimeout', function() {
                $window.location.href = '/logout';
            });

            $scope.$on('Keepalive', function() {
                Heartbeat.get();
                if ($scope.hasOwnProperty('session_modal')) {
                    $scope.session_modal.close();
                }
            });

            function open_session_timeout_modal() {
                $scope.session_modal = $uibModal.open(
                    {
                        animation: $scope.animationsEnabled,
                        templateUrl: 'static/ng-app/partials/session-timeout-modal.html',
                        controller: 'MainController',
                        size: 'lg',
                        resolve: {}
                    }
                );
            }
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
        'ProbeProteinMap',
        'OntoEntityPartOf',
        'Classify',
        'TrainModel',
        function ($scope, $q, $routeParams, $uibModal, ImageSet, Image,
                  Subregion, ProbeProteinMap, OntoEntityPartOf, Classify, TrainModel) {
            $scope.images = [];
            $scope.selected_image = null;
            $scope.selected_classification = null;
            $scope.mode = 'train';  // can be 'train', or 'classify'
            $scope.currently_training = false; //boolean if backend is busy training a model

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

            // disable drawing if a trained model exists
            $scope.$watch('image_set.trainedmodel', function () {
                if ($scope.image_set.trainedmodel === null || $scope.image_set.trainedmodel === undefined) {
                    $scope.enabled = true;
                } else {
                    if ($scope.mode === 'classify') {
                        $scope.enabled = true;
                    }
                    $scope.enabled = false;
                }
            });

            $scope.open_modal = function (size, template_type, confirm_callback, custom_path) {
                var template_url;

                if (template_type === 'confirm') {
                    template_url = 'static/ng-app/partials/confirm-modal.html';
                } else {
                    template_url = 'static/ng-app/partials/generic-modal.html';
                }

                if (template_type === 'custom') {
                    template_url = custom_path;
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
                $scope.open_modal('lg', 'custom', undefined, 'static/ng-app/partials/info_modal.html');
            };

            function get_items_from_nested_entities(relations, wanted_type) {
                var wanted = [];

                relations.forEach(function(r) {
                    if (r.type_name === wanted_type) {
                        wanted.push({'id': r.id, 'name': r.name});
                    }
                    wanted = wanted.concat(get_items_from_nested_entities(r['relations'], wanted_type));
                });

                return wanted;
            }

            function get_structures_by_proteins(proteins) {
                var entity_promises = [];
                $scope.onto_structures = [];

                proteins.forEach(function(protein) {
                    entity_promises.push(OntoEntityPartOf.get(
                        {
                            'id': protein.id
                        }).$promise
                    );
                });

                $q.all(entity_promises).then(function(results) {
                    var temp_structures = [];
                    var uniq_structures = {};
                    results.forEach(function (r) {
                        temp_structures = get_items_from_nested_entities(r['relations'], 'structure');

                        temp_structures.forEach(function (s) {
                            if (!(s.id in uniq_structures)) {
                                uniq_structures[s.id] = s.name;
                            }
                        })
                    });

                    Object.keys(uniq_structures).forEach(function (k) {
                        $scope.onto_structures.push(
                            {
                                'id': k,
                                'name': uniq_structures[k]
                            }
                        )
                    })
                });
            }

            $scope.image_set = ImageSet.get({'image_set_id': $routeParams.image_set_id});

            $scope.image_set.$promise.then(function(data) {
                $scope.images = Image.query({'image_set': data.id});
                var protein_promises = [];

                data.probes.forEach(function(probe) {
                    protein_promises.push(ProbeProteinMap.query(
                        {
                            'probe': probe.probe
                        }).$promise
                    );
                });

                $q.all(protein_promises).then(function(results) {
                    $scope.proteins = [];
                    var protein_keys = [];

                    results.forEach(function(probe_protein_map) {
                        probe_protein_map.forEach(function(probe_protein) {
                            if (protein_keys.indexOf(probe_protein.protein_name) === -1) {
                                protein_keys.push(probe_protein.protein_name);

                                $scope.proteins.push(
                                    {
                                        'id': probe_protein.protein,
                                        'name': probe_protein.protein_name
                                    }
                                );
                            }
                        });
                    });
                    get_structures_by_proteins($scope.proteins);
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
                        'entity': classification.id
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
                    } else {
                        $scope.regions.svg = [];
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

                    if ($scope.image_set.trainedmodel === null || $scope.image_set.trainedmodel === undefined) {
                        $scope.enabled = true;
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

                    region.entity = $scope.selected_classification.id;
                    region.image = $scope.selected_image.id;
                    region.points = region_points;

                    regions.push(region)
                });

                // Sub-region POST is handled a little differently as we cannot keep
                // track of modified regions so any new save will first delete the old regions
                // first
                var delete_response = Subregion.delete({
                    'image': $scope.selected_image.id,
                    'entity': $scope.selected_classification.id
                });

                delete_response.$promise.then(function (delete_data) {
                    if (regions.length === 0) {
                        $scope.set_mode($scope.mode);
                        $scope.image_set = ImageSet.get(
                            {
                                'image_set_id': $routeParams.image_set_id
                            }
                        );
                        return;
                    }

                    var post_region_response = Subregion.save(regions);

                    var new_regions = [];
                    var new_region_points = [];

                    post_region_response.$promise.then(function (data) {
                        // clear regions
                        $scope.regions.svg = [];

                        data.forEach(function (region) {
                            // empty array for our new region
                            new_region_points = [];

                            region.points.forEach(function (p) {
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
                });
            };

            $scope.delete_saved_regions = function () {
                var delete_response = Subregion.delete({
                    'image': $scope.selected_image.id,
                    'entity': $scope.selected_classification.id
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
                        $scope.modal_items.push({
                            anatomy: Object.keys(r)[0],
                            probability: (r[Object.keys(r)[0]] * 100).toFixed(2)*1
                        })
                    });
                    $scope.open_modal(undefined, 'custom', undefined, 'static/ng-app/partials/classify_region_modal.html');
                });
            }
        }
    ]
);
