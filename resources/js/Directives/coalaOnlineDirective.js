app.directive('coalaonline',[ '$http', function ($http) {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/coalaonline.html',
        controller: function ($scope, $sessionStorage, $q) {
            $scope.storage = $sessionStorage;
            self = this
            self.LANGUAGES = exts;
            self.file_data ='';
            $scope.running_coala = false;
            $scope.loading_coajson = false;
            $scope.state = "instant";
            $(document).ready(function(){
                $('ul.tabs').tabs();
            });
            $("#file_data").on('input',function(e){
                if(e.target.value != ''){
                     self.file_data = e.target.value
                }
            });
            $('#lang').change(function(){
                $scope.lng = $('#lang').val().replace("string:", "").toLowerCase();
                json = {
                    "file_data" : $('#file-data').val(),
                    "language" :  $scope.lng,
                    "mode" : "bears"
                }
                $scope.run_quickstart(json);
            })
            $('.git-link').change(function(){
                var git_url = $('.git-link').val()
                if(git_url.slice(-4)!=".git"){
                    git_url += ".git"
                }
                json = {
                    "url" : git_url,
                    "mode" : "bears"
                }
                $scope.run_quickstart(json);
            })
            $scope.set_state = function(state) {
                $scope.sections = null;
                $scope.lang_sel = null;
                $scope.state = state;
            }
            $scope.run_quickstart = function(json){
                bear_lists = [];
                $scope.loading_coajson = true;
                $http.post(coala_online_api, JSON.stringify(json))
                .then(function(res){
                    response = res.data.response.response;
                    $scope.sections = {}
                    angular.forEach(Object.keys(response), function(section) {
                        $scope.sections[section] = {}
                        $scope.sections[section]["files"] = response[section]["files"]
                        $scope.sections[section]["bears"] = {}
                        bear_json = $scope.fetch_bear_data(
                                    response[section]["bears"]
                                    .replace(/\s/g,'')
                                    .split(','), section);
                        $scope.sections[section]["bears"] = bear_json;
                    });
                    $scope.$evalAsync();
                    $scope.loading_coajson = false;
                })
            }
            $scope.fetch_bear_data = function(bear_list, section){
                bear_json = {};
                bear_list.forEach(function(bear) {
                    $scope.sections[section]["bears"][bear] = {};
                    $scope.fetch_bear_settings(bear, section);
                });
                return bear_json;
            }
            $scope.fetch_bear_settings = function(bear, section){
                var deferred = $q.defer();
                $http.get(api_link + '/search/bears?bear=' + bear)
                .then(function(data){
                    nop_json = {};
                    nop = data.data.metadata.non_optional_params;
                    data.data["BEAR_DEPS"].forEach(function(dep){
                        dep.metadata.non_optional_params.forEach(function(dep_nop){
                            if (Array.isArray(dep_nop)){
                                dep_nop.forEach(function(dn){
                                    nop.push(dn);
                                })
                            } else {
                                nop.push(dep_nop);
                            }
                        })
                    })
                    nop.forEach(function(element){
                        elem = Object.keys(element)[0];
                        nop_json[elem] = "";
                    })

                    op_json = {};
                    op = data.data.metadata.optional_params;
                    data.data["BEAR_DEPS"].forEach(function(dep){
                        dep.metadata.optional_params.forEach(function(dep_op){
                            if (Array.isArray(dep_op)){
                                dep_op.forEach(function(dn){
                                    op.push(dn);
                                })
                            } else {
                                op.push(dep_op);
                            }
                        })
                    })
                    op.forEach(function(element){
                        elem = Object.keys(element)[0];
                        op_json[elem] = "";
                    })
                    $scope.sections[section]["bears"][bear] = {};
                    $scope.sections[section]["bears"][bear]['nop'] = nop_json;
                    $scope.sections[section]["bears"][bear]['op'] = op_json;
                    $scope.$evalAsync();
                }, function (failure) {
                    // bear not found at webServices
                    console.log(failure);
                })
                .catch(function(err){
                    console.log('Error!');
                });
            }
            $scope.run_coala = function(){

                var sections_copy = JSON.stringify($scope.sections);

                $scope.sections = $scope.pre_format_settings($scope.sections);

                var json = {
                    "sections" : $scope.sections,
                    "mode" : "coala",
                }
                if ($scope.state == "instant") {
                    json["file_data"] = $('#file-data').val(),
                    json["language"] = $scope.lng
                } else {
                    json["url"] = $(".git-link").val();
                }
                jsn_str = JSON.stringify(json)
                $scope.sections = JSON.parse(sections_copy);
                $scope.running_coala = true;
                $http.post(coala_online_api, jsn_str)
                .then(function(data){
                    $scope.results = data.data.response.results;
                    $scope.coafile = data.data.coafile;
                    $scope.$evalAsync();
                    $scope.running_coala = false;
                })
            }

            $scope.add_bears = function(section){
                $scope.sections[section]["bears"][""] = "";
                $http.get(api_link + '/list/bears')
                .then(function(data){
                    bears = {}
                    angular.forEach(Object.keys(data["data"]), function(value, key){
                        bears[value] = null;
                    })
                    $('input.autocomplete').autocomplete({
                        data: bears,
                        limit: 5,
                        onAutocomplete: function(val) {
                            delete $scope.sections[section]["bears"][""];
                            $scope.fetch_bear_settings(val, section);
                        },
                        minLength: 1,
                    });
                })
            }

            $scope.remove_bears = function(section, bear){
                delete $scope.sections[section]["bears"][bear];
            }

            $scope.add_sections = function(){
                var section = $('#new-section').val();
                $scope.sections[section] = {
                    "bears": {},
                    "files" : ""
                }
            }

            $scope.remove_sections = function(section){
                delete $scope.sections[section]
            }

            $scope.add_optional_settings = function (section, bear) {
                $scope.section_settings = section;
                $scope.current_bear = bear;
                $(document).ready(function () {
                    $('.modal').modal();
                    $('#settingmodal').modal('open');
                })
            }

            $scope.pre_format_settings = function (settings) {
                angular.forEach(settings, function(section, key){
                    angular.forEach(section['bears'], function(bears, key){
                        temp = {}
                        angular.forEach(bears, function(bear, key){
                            if (key == "nop") {
                                angular.forEach(Object.keys(bear), function(value, key){
                                    temp[value] = bear[value];
                                });
                            } else {
                                angular.forEach(Object.keys(bear), function(value, key){
                                    if (bear[value] != "") temp[value] = bear[value];
                                });
                            }
                        });
                        section['bears'][key] = temp;
                    });
                });

                return settings;
            }

        },
        controllerAs: 'toc'
    }
}]);
