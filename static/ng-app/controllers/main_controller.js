app.controller(
    'MainController',
    [
        '$scope',
        '$timeout',
        'Image',
        'Experiments',
        'Train',
        function ($scope, $timeout, Image, Experiments, Train) {
            $scope.experiments = Experiments.query();
            $scope.imageSrc = null;
            $scope.enabled = true;
            $scope.colorArray = ['#00FF00'];
            $scope.activePolygon = 0;
            $scope.points = [[]];
            $scope.poly_height = 800;
            $scope.poly_width = 800;
            $scope.experiment_selected = function (item) {
                $scope.images = "http://localhost:8000/api/experiment/" + item.experiment_id + "/images";
                $scope.current_experiment = item.experiment_id;
            };

            $scope.image_selected = function (item) {
                // $scope.$broadcast('ngAreas:remove_all', {});
                $scope.imageSrc = "http://localhost:5000/api/images/" + item.id + "?type=jpg";
                $scope.current_image_name = item.name;
                $scope.current_image_id = item.id;
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
                Train.save(
                    { 'id': $scope.current_image_id },
                    {
                        'points': $scope.points
                    }
                )
            };
        }
    ]
);
