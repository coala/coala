app.directive('getinvolved', ['$http', function ($http) {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/getinvolved.html',
        controller: function ($scope, $sessionStorage) {
            var self = this
            $scope.$get_involved_storage = $sessionStorage
            self.contributors

            function excludeBot(contributors) {
                return contributors.filter(function(member){
                    if (member.login == 'rultor') return false
                    if (member.login == 'gitmate-bot') return false
                    return true
                })
            }

            if($scope.$get_involved_storage.contributors_data){
                self.contributors = excludeBot($scope.$get_involved_storage.contributors_data)
            }else{
                $http.get(api_link + '/contrib/')
                    .then(function (data) {
                        $scope.$get_involved_storage.contributors_data = data["data"]
                        self.contributors = excludeBot(data["data"])
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
