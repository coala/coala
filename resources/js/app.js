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

