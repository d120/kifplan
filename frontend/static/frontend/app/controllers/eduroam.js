(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('eduroamCtrl', ['$scope', 'Restangular', 'toolbarService', function($scope, Restangular, toolbarService) {

    toolbarService.title('eduroam Gastaccounts')

    var accounts = Restangular.all('eduroam/guest-accounts');

    $scope.loading = true;
    accounts.getList().then(function(data) {
      $scope.accounts = data;
      $scope.loading = false;
    });

    $scope.json = function(o) {
      return JSON.stringify(o, null, 4);
    };

  }]);

})( window, document );
