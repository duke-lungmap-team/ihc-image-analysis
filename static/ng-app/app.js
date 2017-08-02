var app = angular.module(
    'IHCApp',
    [
        'ngResource',
        'ngRoute',
        'ngCookies',
        'ui.bootstrap',
        'ngPolyDraw'
    ]
);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.config(function($routeProvider) {
    $routeProvider.when(
        '/imagesets/',
        {
            templateUrl: 'static/ng-app/partials/exp_list.html',
            controller: 'ExperimentListController'
        }
    ).when(
        '/imagesets/:imagesets_id',
        {
            templateUrl: 'static/ng-app/partials/exp_detail.html',
            controller: 'ExperimentDetailController'
        }
    ).when(
        '/trainingsets/',
        {
            templateUrl: 'static/ng-app/partials/training_list.html',
            controller: 'TrainingListController'
        }
    ).when(
        '/train/',
        {
            templateUrl: 'static/ng-app/partials/train.html',
            controller: 'TrainController'
        }
    ).otherwise({ redirectTo: '/' });
});

app.config(function($httpProvider) {
  $httpProvider.defaults.withCredentials = true;
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.interceptors.push(function($cookies) {
    return {
      'request': function(config) {
        config.headers['X-CSRFToken'] = $cookies.get('csrftoken');
        return config;
      }
    };
  });
});
