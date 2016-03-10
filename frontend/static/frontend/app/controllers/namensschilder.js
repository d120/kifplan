(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('namensschilderCtrl', ['$scope', 'Restangular', 'toolbarService', function($scope, Restangular, toolbarService) {

    toolbarService.title('Namensschilder erstellen')

  }]);

})( window, document );
