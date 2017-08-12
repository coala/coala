app.directive('languages',  ['$http',  '$timeout' ,function ($http, $timeout) {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/languages.html',
        controller: function ($scope, $sessionStorage) {
            self = this
            $scope.$storage = $sessionStorage
            $scope.bearList = []
            $scope.currentBear = {}
            self.theatreLoader = false;
            $scope.lang_loader = false;
            self.theatreLoaderMessages = [
                "Waking up little joeys",
                "Dodging the bushfires",
                "Gulping the eucalypt"
            ]
            if($scope.$storage.bear_data){
                $scope.bearList = ($scope.$storage.bear_data)
            }else{
                $scope.lang_loader=true;
                $http.get(api_link + '/list/bears')
                    .then(function(data){
                        arr = []
                        angular.forEach(Object.keys(data["data"]), function(value, key){
                            arr.push({
                                "name" : value,
                                "desc" : data["data"][value]["desc"],
                                "languages": data["data"][value]["languages"]
                            })
                        })
                        $scope.bearList = arr
                        $scope.$evalAsync();
                        $scope.lang_loader = false;
                        $scope.$storage.bear_data = arr
                    })
            }

            $scope.setCurrentBear = function (bear_data) {
                $scope.currentBear = bear_data["data"]
            }
            self.showTheatre = function (bear_selected) {

                $http.get(api_link + '/search/bears?bear=' + bear_selected["name"])
                    .then(function (bear_data) {
                        params_list = {
                            "optional_params": [],
                            "non_optional_params": []
                        }
                        angular.forEach(bear_data["data"]["metadata"]["optional_params"], function(value, key){
                            params_list["optional_params"].push(Object.keys(value)[0])
                        });
                        angular.forEach(bear_data["data"]["metadata"]["non_optional_params"], function(value, key){
                            params_list["non_optional_params"].push(Object.keys(value)[0])
                        });
                        bear_data["data"]["metadata"]["params_list"] = params_list;
                        $scope.setCurrentBear(bear_data);
                        $scope.$evalAsync();
                        $('#modal1').modal('open');
                    })
            }
        },
        controllerAs: 'lc'
    }
}]);

