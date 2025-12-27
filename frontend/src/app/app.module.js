angular.module('bucketlistApp', ['ngRoute'])
    .constant('API_URL', 'http://localhost:5000/api/v1')
    .run(['$rootScope', '$location', 'AuthService', function($rootScope, $location, AuthService) {
        $rootScope.isLoggedIn = function() {
            return AuthService.isAuthenticated();
        };
        
        $rootScope.logout = function() {
            AuthService.logout();
            $location.path('/login');
        };
        
        $rootScope.$on('$routeChangeStart', function(event, next) {
            if (next.requireAuth && !AuthService.isAuthenticated()) {
                event.preventDefault();
                $location.path('/login');
            }
        });
    }]);