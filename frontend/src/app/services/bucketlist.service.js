angular.module('bucketlistApp')
    .factory('BucketListService', ['$http', 'API_URL', function($http, API_URL) {
        var service = {};
        
        service.getAll = function(params) {
            return $http.get(API_URL + '/bucketlists', { params: params })
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.getOne = function(id) {
            return $http.get(API_URL + '/bucketlists/' + id)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.create = function(data) {
            return $http.post(API_URL + '/bucketlists', data)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.update = function(id, data) {
            return $http.put(API_URL + '/bucketlists/' + id, data)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.delete = function(id) {
            return $http.delete(API_URL + '/bucketlists/' + id)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.createItem = function(bucketlistId, data) {
            return $http.post(API_URL + '/bucketlists/' + bucketlistId + '/items', data)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.updateItem = function(bucketlistId, itemId, data) {
            return $http.put(API_URL + '/bucketlists/' + bucketlistId + '/items/' + itemId, data)
                .then(function(response) {
                    return response.data;
                });
        };
        
        service.deleteItem = function(bucketlistId, itemId) {
            return $http.delete(API_URL + '/bucketlists/' + bucketlistId + '/items/' + itemId)
                .then(function(response) {
                    return response.data;
                });
        };
        
        return service;
    }]);