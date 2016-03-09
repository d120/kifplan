(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('toolbarCtrl', ['$rootScope', '$scope', '$mdSidenav', '$location', 'authService', 'toolbarService', function($rootScope, $scope, $mdSidenav, $location, authService, toolbarService) {

    $scope.title = toolbarService.title();
    $scope.user = $rootScope.user;

    toolbarService.registerReceiver(function() {
      $scope.title = toolbarService.title();
    });

    $scope.toggleNav = function() {
      $mdSidenav('nav').toggle();
    };

    $scope.logout = function() {
      authService.logout();
      $location.path('/login');
    };

  }]);

})( window, document );
