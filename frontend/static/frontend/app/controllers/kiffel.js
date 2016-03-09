(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('kiffelCtrl', ['$scope', '$routeParams', 'Restangular', 'toolbarService', function($scope, $routeParams, Restangular, toolbarService) {

    var kiffel = Restangular.one('kiffels', $routeParams.id);

    $scope.loading = true;
    kiffel.get().then(function(data) {
      $scope.kiffel = data;
      $scope.loading = false;

      toolbarService.title(data.nickname)

      $scope.json = JSON.stringify($scope.kiffel, null, 4);
    });

  }]);

})( window, document );
