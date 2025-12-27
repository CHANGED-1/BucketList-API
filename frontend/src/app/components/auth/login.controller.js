angular.module('bucketlistApp')
    .controller('LoginController', ['$scope', '$location', 'AuthService', 
        function($scope, $location, AuthService) {
            $scope.credentials = {};
            $scope.error = null;
            
            $scope.login = function() {
                $scope.error = null;
                
                AuthService.login($scope.credentials)
                    .then(function(response) {
                        $location.path('/bucketlists');
                    })
                    .catch(function(error) {
                        $scope.error = error.data.message || 'Login failed';
                    });
            };
        }
    ]);