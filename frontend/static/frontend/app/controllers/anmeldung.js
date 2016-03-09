(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('anmeldungCtrl', ['$scope', '$routeParams', 'Restangular', 'toolbarService', function($scope, $routeParams, Restangular, toolbarService) {

    toolbarService.title('Anmeldung');

    var kiffels = Restangular.all('kiffels');

    $scope.update = function() {
      $scope.loading = true;
      kiffels.getList({
        search: $scope.search
      }).then(function(data) {
        $scope.kiffels = data;
        $scope.loading = false;
      });
    };
    $scope.update();

    var originatorEv;
    $scope.openMenu = function($mdOpenMenu, ev) {
      originatorEv = ev;
      $mdOpenMenu(ev);
    };

  }]);

})( window, document );
