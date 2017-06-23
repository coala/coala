app.directive('coalaonline',[ '$http', function ($http) {
    return {
        restrict: 'E',
        templateUrl: 'partials/tabs/coalaonline.html',
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
