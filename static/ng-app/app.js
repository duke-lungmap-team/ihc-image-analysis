var app = angular.module(
    'IHCApp',
    [
        'ngResource',
        'ngRoute',
        'ngCookies',
        'ui.bootstrap',
        'drwPolygon'
    ]
);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.config(function($routeProvider) {
    $routeProvider.when(
        '/',
        {
            templateUrl: 'static/ng-app/partials/img_set_list.html',
            controller: 'ImageSetListController'
        }
    ).when(
        '/image-sets/:image_set_id',
        {
            templateUrl: 'static/ng-app/partials/img_set_detail.html',
            controller: 'ImageSetDetailController'
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
