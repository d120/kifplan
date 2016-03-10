(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('sidenavCtrl', ['$scope', '$mdSidenav', '$location', '$http', 'authService', function($scope, $mdSidenav, $location, $http, authService) {

    $scope.title = "Kiffel Verwaltung";

    $scope.navigation = [
      {
        title: 'Helpdesk',
        items: [
          { title: 'Anmeldung', url: '#/anmeldung' },
          { title: 'Namensschilder', url: '#/namensschilder' },
          { title: 'Teilnahmebestätigungen', url: '#/teilnahme' },
          { title: 'Alle Kiffel', url: '#/kiffels' },
          { title: 'Schildergenerator', url: '#/schilder' },
        ]
      }, {
        title: 'Links',
        items: [
          { title: 'Hilfe und Support', url: '#/hilfe' },
          { title: 'Admin-Bereich', url: '/admin', blank: true },
          { title: 'API-Browser', url: '/api/v1', blank: true },
          { title: 'Source Code', url: 'https://git.fachschaft.informatik.tu-darmstadt.de/kif/kiffel-verwaltung', blank: true },
          { title: 'd120.de', url: 'http://www.d120.de/', blank: true },
        ]
      }
    ];

    $scope.isActive = function(url) {
      return '#'+$location.path() === url;
    };

    $scope.close = function() {
      $mdSidenav('nav').toggle();
    };

    $scope.logout = function() {
      authService.logout();
    };

  }]);

})( window, document );
