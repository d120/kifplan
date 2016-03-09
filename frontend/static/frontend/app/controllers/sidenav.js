(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('sidenavCtrl', ['$scope', '$mdSidenav', '$location', '$http', 'authService', function($scope, $mdSidenav, $location, $http, authService) {

    $scope.title = "Kiffel Verwaltung";

    $scope.navigation = [
      {
        title: 'Kiffel',
        items: [
          { title: 'Alle Kiffel', url: '/kiffels' },
        ]
      },
      {
        title: 'Anmeldung',
        items: [
          { title: 'Dashboard', url: '/anmeldung' },
        ]
      }
    ];

    $scope.isActive = function(url) {
      return $location.path() === url;
    };

    $scope.close = function() {
      $mdSidenav('nav').toggle();
    };

    $scope.logout = function() {
      authService.logout();
    };

  }]);

})( window, document );
