angular.module('bucketListApp')
    .controller('BucketListController', ['$scope', 'BucketListService',
        function($scope, BucketListService) {
            $scope.bucketlists = [];
            $scope.newBucketList = {};
            $scope.newItem = {};
            $scope.searchQuery = '';
            $scope.currentPage = 1;
            $scope.limit = 20;
            $scope.error = null;
            $scope.success = null;
            
            // Load bucket lists
            $scope.loadBucketLists = function() {
                var params = {
                    limit: $scope.limit,
                    page: $scope.currentPage
                };
                
                if ($scope.searchQuery) {
                    params.q = $scope.searchQuery;
                }
                
                BucketListService.getAll(params)
                    .then(function(data) {
                        $scope.bucketlists = data.bucketlists;
                        $scope.totalPages = data.pages;
                        $scope.total = data.total;
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to load bucket lists';
                    });
            };
            
            // Create bucket list
            $scope.createBucketList = function() {
                if (!$scope.newBucketList.name) return;
                
                BucketListService.create($scope.newBucketList)
                    .then(function(response) {
                        $scope.success = 'Bucket list created successfully!';
                        $scope.newBucketList = {};
                        $scope.loadBucketLists();
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to create bucket list';
                    });
            };
            
            // Delete bucket list
            $scope.deleteBucketList = function(id) {
                if (!confirm('Are you sure you want to delete this bucket list?')) return;
                
                BucketListService.delete(id)
                    .then(function() {
                        $scope.success = 'Bucket list deleted successfully!';
                        $scope.loadBucketLists();
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to delete bucket list';
                    });
            };
            
            // Create item
            $scope.createItem = function(bucketlistId) {
                var itemData = $scope.newItem[bucketlistId];
                if (!itemData || !itemData.name) return;
                
                BucketListService.createItem(bucketlistId, itemData)
                    .then(function() {
                        $scope.success = 'Item added successfully!';
                        $scope.newItem[bucketlistId] = {};
                        $scope.loadBucketLists();
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to add item';
                    });
            };
            
            // Toggle item done status
            $scope.toggleItem = function(bucketlistId, item) {
                BucketListService.updateItem(bucketlistId, item.id, { done: !item.done })
                    .then(function() {
                        item.done = !item.done;
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to update item';
                    });
            };
            
            // Delete item
            $scope.deleteItem = function(bucketlistId, itemId) {
                if (!confirm('Are you sure you want to delete this item?')) return;
                
                BucketListService.deleteItem(bucketlistId, itemId)
                    .then(function() {
                        $scope.success = 'Item deleted successfully!';
                        $scope.loadBucketLists();
                    })
                    .catch(function(error) {
                        $scope.error = 'Failed to delete item';
                    });
            };
            
            // Search
            $scope.search = function() {
                $scope.currentPage = 1;
                $scope.loadBucketLists();
            };
            
            // Pagination
            $scope.nextPage = function() {
                if ($scope.currentPage < $scope.totalPages) {
                    $scope.currentPage++;
                    $scope.loadBucketLists();
                }
            };
            
            $scope.prevPage = function() {
                if ($scope.currentPage > 1) {
                    $scope.currentPage--;
                    $scope.loadBucketLists();
                }
            };
            
            // Initialize
            $scope.loadBucketLists();
        }
    ]);