(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('kiffelCtrl', ['$scope', '$routeParams', 'Restangular', function($scope, $routeParams, Restangular) {

    var kiffel = Restangular.one('kiffels', $routeParams.id);

    $scope.loading = true;
    kiffel.get().then(function(data) {
      $scope.kiffel = data;
      $scope.loading = false;

      $scope.json = JSON.stringify($scope.kiffel, null, 4);
    });

  }]);

})( window, document );
