app.directive('people', function () {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/people.html',
        controller: function ($scope, $http, $location) {
            $scope.person = null;
            url = $location.url()

            $scope.person = $location.path().split('/').pop()
            $http.get('/data/people/' + $scope.person + '.md')
            .then(function (res) {
                $scope.person = jsyaml.load(res.data)
            })
            .catch(function onError(response) {
                $location.path('/home');
            })

        }
    }
})

