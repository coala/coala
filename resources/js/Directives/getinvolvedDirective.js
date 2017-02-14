app.directive('getinvolved', ['$http', function ($http) {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/getinvolved.html',
        controller: function ($scope, $sessionStorage) {
            var self = this
            $scope.$get_involved_storage = $sessionStorage
            self.contributors
            if($scope.$get_involved_storage.contributors_data){
                self.contributors = $scope.$get_involved_storage.contributors_data
            }else{
                $http.get(api_link + '/contrib/')
                    .then(function (data) {
                        $scope.$get_involved_storage.contributors_data = data["data"]
                        self.contributors = data["data"]
                    }).catch(function (c) {
                    console.log(c);
                })
            }
            $scope.totalDisplayed = 20;

            $scope.loadMore = function () {
                $scope.totalDisplayed += 20;
            };
        },
        controllerAs: "gic"
    }
}]);
