var app = angular.module(
    'IHCApp',
    ['ngResource', 'ngRoute', 'ui.bootstrap', 'ngPolyDraw']
);


app.config(function($routeProvider) {
    $routeProvider.when(
        '/experiments/',
        {
            templateUrl: 'static/ng-app/partials/exp_list.html',
            controller: 'ExperimentListController'
        }
    ).otherwise({ redirectTo: '/' });
});