var app = angular.module(
    'IHCApp',
    [
        'ngResource',
        'ngRoute',
        'ngCookies',
        'ui.bootstrap',
        'ngIdle',
        'drwPolygon'
    ]
);

app.config(['KeepaliveProvider', 'IdleProvider', function(KeepaliveProvider, IdleProvider) {
    IdleProvider.idle(900);  // 15 minutes
    IdleProvider.timeout(30);  // give user 30 seconds notification before logging out
    KeepaliveProvider.interval(60); // keep session alive once a minute, not too chatty
}]);

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

app.run(function(Idle) {
    Idle.watch();
});
