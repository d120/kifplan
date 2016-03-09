(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('loginCtrl', ['$rootScope', '$scope', '$location', 'authService', function($rootScope, $scope, $location, authService) {

    $scope.login = function() {
      authService.login($scope.creds.username, $scope.creds.password);
      $location.path(authService.getNextPath());
    };

  }]);

})( window, document );
