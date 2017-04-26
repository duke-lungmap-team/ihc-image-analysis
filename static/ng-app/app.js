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
        '/experiments/',
        {
            templateUrl: 'static/ng-app/partials/exp_list.html',
            controller: 'ExperimentListController'
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
