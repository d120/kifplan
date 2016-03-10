(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('teilnahmeCtrl', ['$scope', 'Restangular', 'toolbarService', function($scope, Restangular, toolbarService) {

    toolbarService.title('Teilnahmebestätigungen erstellen')

  }]);

})( window, document );
