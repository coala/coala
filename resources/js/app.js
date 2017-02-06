(function(){
 var app = angular.module('coala', ['ngStorage','ngRoute', 'ngSanitize', 'btford.markdown']);

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
  this.tab = $location.path();
  this.setTab = function (stab) {
   this.tab = stab;
   $location.path(stab);
   $(".button-collapse").sideNav('hide');
  }
  this.isSet = function (stab) {
   return $location.path() == stab
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
    self.diff_data_status = false;
    self.diff_loader = true;
    self.done_loading_bears = false;
    self.error_on_run = false;
    self.error_message = "";

    $http.get(api_link + '/list/bears')
    .then(function(data){
     bears = {}
     angular.forEach(Object.keys(data["data"]), function(value, key){
       bears[value] = null;
     })
     $('.chips-bears').material_chip({
       data: [{
         tag: 'PEP8Bear'
       }],
       placeholder: '+bear',
       secondaryPlaceholder: '+Add bear',
       autocompleteData: bears
     });
     self.diff_loader = false;
     self.done_loading_bears = true;
    })

    self.update_diff_data = function (data) {
     self.diff_data = data
    };

    self.get_diff_data = function () {
     return self.diff_data
    }

    self.submit_coa_form = function () {
     self.diff_loader = true;
     self.diff_data_status = false;
     var bearsList="";
     var chipsData = $('.chips-bears').material_chip('data');
     if(chipsData.length > 0) {
       bearsList += chipsData[0].tag;
       for(var i = 1; i < chipsData.length; i++)
        bearsList += ',' + chipsData[i].tag;
     }
     $http({
      url: api_link + '/editor/',
      method: "POST",
      data: {
       "file_data": $(".file-data").val(),
       "bears": bearsList,
       "language": $(".lang-data").val()
      }
     })
     .then(function(response) {
      self.diff_loader = false;
      self.diff_data_status = true;
      self.error_on_run = false;
      if(response["data"]["status"] == 'error') {
        self.error_message = response["data"]["msg"];
        self.error_on_run = true;
      } else {
        self.update_diff_data(response["data"]["results"]["default"])
      }
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

/*
Filter from http://stackoverflow.com/a/27963602
*/
app.filter('orderEmpty', function () {
    return function (array, key, type) {
        var present, empty, result;

        if(!angular.isArray(array)) return;
        present = array.filter(function (item) {
            return item[key];
        });
        empty = array.filter(function (item) {
            return !item[key]
        });
        switch(type) {
            case 'toBottom':
                result = present.concat(empty);
                break;
            case 'toTop':
                result = empty.concat(present);
                break;
            default:
                result = array;
                break;
        }
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

})();
