(function(){
	var app = angular.module('coala', ['ngStorage','ngRoute']);

    app.config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
            when('/home', {
                template: '<home></home>'
            }).
            when('/languages', {
                template: '<languages></languages>'
            }).
            when('/getinvolved', {
                template: '<getinvolved></getinvolved>'
            }).
            when('/tryonline', {
                template: '<tryonline></tryonline>'
            }).
            otherwise({
                redirectTo: '/home'
            });
        }]);

	app.controller('SnippetController', function(){

		self = this
		self.cur = ""
		self.snip = snippets
		self.languages = Object.keys(snippets)
		$(document).ready(function(){
			$('select').material_select();
		})
	})

    app.controller('TabController', function ($location) {
        this.tab = "/home";
        this.setTab = function (stab) {
            this.tab = stab;
            $location.path(stab);
            $(".button-collapse").sideNav('hide');
        }
        this.isSet = function (stab) {
            return this.tab == stab
        }
    })

	app.directive('home', function () {
		return {
			restrict: 'E',
			templateUrl: 'partials/tabs/home.html'
		}
	})



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
					console.log(bear_data);
					$scope.currentBear = bear_data["data"]
				}
				self.showTheatre = function (bear_selected) {	
					console.log("Im called!");
					console.log(bear_selected);
					$http.get(api_link + '/search/bears?bear=' + bear_selected["name"])
					.then(function (bear_data) {
						console.log(bear_data);
						$scope.setCurrentBear(bear_data);
					  $scope.$evalAsync();
						$('#modal1').modal('open');
					})
				}
			},
			controllerAs: 'lc'
		}
	}]);

	app.directive('tryonline',[ '$http', function ($http) {
		return {
			restrict: 'E',
			templateUrl: 'partials/tabs/tryonline.html',
			controller: function () {
				self = this;
				self.diff_data = {};
				self.update_diff_data = function (data) {
					self.diff_data = data
					console.log(self.diff_data);
				};

				self.get_diff_data = function () {
					return self.diff_data
				}
				self.submit_coa_form = function () {

			$http({
			      url: api_link + '/editor/',
			      method: "POST",
			      data: {
			              "file_data": $(".file-data").val(),
			              "bears": $(".bear-data").val(),
			              "language": $(".lang-data").val()
			           }
			  })
			  .then(function(response) {
			          self.update_diff_data(response["data"]["results"]["default"])
			  }).catch(function (c) {
			  	console.log(c);
			  })

				}
		},
		controllerAs: 'toc'
	}
	}]);
		

	app.filter('format_desc', function () {
        return function (value) {
            if (!value) return '';
            var lastspace = value.indexOf('.');
            if (lastspace != -1) {
                if (value.charAt(lastspace-1) == ',') {
                	lastspace = lastspace - 1;
                }
                  value = value.substr(0, lastspace);
            }

            return value;
        };
    });

	/* 
	Filter from http://stackoverflow.com/a/18939029
	*/
	app.filter("toArray", function(){
	    return function(obj) {
	     var result = [];
	     angular.forEach(obj, function(val, key) {
	      result.push(val);
	     });
	     return result;
	    };
	});

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
					var temp = {}
					angular.forEach(data["data"], function(project, key){
						angular.forEach(project, function(value, key){
							if(Object.keys(temp).indexOf(value["login"]) > -1){
								temp[value["login"]]["contributions"]+= value["contributions"]
							}
							else{
								temp[value["login"]] = value
							}
						});
					});
					$scope.$get_involved_storage.contributors_data = temp
					self.contributors = temp
				}).catch(function (c) {
					console.log(c);
				})
				}	
			},
			controllerAs: "gic"
		}
	}]);

})();
