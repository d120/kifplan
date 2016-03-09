(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('kiffelsCtrl', ['$scope', 'Restangular', 'toolbarService', function($scope, Restangular, toolbarService) {

    toolbarService.title('Alle Kiffels')

    var kiffels = Restangular.all('kiffels');

    $scope.loading = true;
    kiffels.getList().then(function(data) {
      $scope.kiffels = data;
      $scope.loading = false;
    });

  }]);

})( window, document );
