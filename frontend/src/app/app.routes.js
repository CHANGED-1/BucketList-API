angular.module('bucketListApp')
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'app/components/home/home.html',
                controller: 'HomeController'
            })
            .when('/login', {
                templateUrl: 'app/components/auth/login.html',
                controller: 'LoginController'
            })
            .when('/register', {
                templateUrl: 'app/components/auth/register.html',
                controller: 'RegisterController'
            })
            .when('/bucketlists', {
                templateUrl: 'app/components/bucketlists/bucketlist.html',
                controller: 'BucketListController',
                requireAuth: true
            })
            .otherwise({
                redirectTo: '/'
            });
    }]);