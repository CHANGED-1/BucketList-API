angular.module('bucketlistApp')
    .factory('AuthService', ['$http', 'API_URL', function($http, API_URL) {
        var service = {};
        
        service.register = function(userData) {
            return $http.post(API_URL + '/auth/register', userData)
                .then(function(response) {
                    if (response.data.token) {
                        localStorage.setItem('token', response.data.token);
                        localStorage.setItem('user', JSON.stringify(response.data.user));
                    }
                    return response.data;
                });
        };
        
        service.login = function(credentials) {
            return $http.post(API_URL + '/auth/login', credentials)
                .then(function(response) {
                    if (response.data.token) {
                        localStorage.setItem('token', response.data.token);
                        localStorage.setItem('user', JSON.stringify(response.data.user));
                    }
                    return response.data;
                });
        };
        
        service.logout = function() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        };
        
        service.getToken = function() {
            return localStorage.getItem('token');
        };
        
        service.isAuthenticated = function() {
            return !!localStorage.getItem('token');
        };
        
        service.getUser = function() {
            var user = localStorage.getItem('user');
            return user ? JSON.parse(user) : null;
        };
        
        return service;
    }])
    // .factory('AuthInterceptor', ['AuthService', function(AuthService) {
    //     return {
    //         request: function(config) {
    //             var token = AuthService.getToken();
    //             if (token) {
    //                 config.headers.Authorization = 'Bearer ' + token;
    //             }
    //             return config;
    //         }
    //     };
    // }])

    .factory('AuthInterceptor', ['$q', '$injector', function ($q, $injector) {

    return {
        request: function (config) {
            var AuthService = $injector.get('AuthService');
            var token = AuthService.getToken();

            if (token) {
                config.headers = config.headers || {};
                config.headers.Authorization = 'Bearer ' + token;
            }

            return config;
        },

        responseError: function (rejection) {
            if (rejection.status === 401) {
                var AuthService = $injector.get('AuthService');
                var $location = $injector.get('$location');

                AuthService.logout();
                $location.path('/login');
            }
            return $q.reject(rejection);
        }
    };
}])

    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.interceptors.push('AuthInterceptor');
    }]);