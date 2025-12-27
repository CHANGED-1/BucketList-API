angular.module('bucketlistApp')
    .controller('RegisterController', ['$scope', '$location', 'AuthService',
        function($scope, $location, AuthService) {
            $scope.userData = {};
            $scope.error = null;
            
            $scope.register = function() {
                $scope.error = null;
                
                if ($scope.userData.password !== $scope.userData.confirmPassword) {
                    $scope.error = 'Passwords do not match';
                    return;
                }
                
                AuthService.register($scope.userData)
                    .then(function(response) {
                        $location.path('/bucketlists');
                    })
                    .catch(function(error) {
                        $scope.error = error.data.message || 'Registration failed';
                    });
            };
        }
    ]);