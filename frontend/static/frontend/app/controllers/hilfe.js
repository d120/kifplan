(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('hilfeCtrl', ['$scope', 'Restangular', 'toolbarService', function($scope, Restangular, toolbarService) {

    toolbarService.title('Hilfe und Support')

  }]);

})( window, document );
