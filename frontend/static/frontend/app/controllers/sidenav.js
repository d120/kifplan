(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('sidenavCtrl', ['$scope', '$mdSidenav', '$location', '$http', 'authService', function($scope, $mdSidenav, $location, $http, authService) {

    $scope.title = "Kiffel Verwaltung";

    $scope.navigation = [
      {
        title: 'Kiffel',
        items: [
          { title: 'Kiffel bearbeiten', url: '#/kiffels' },
          { title: 'Anmeldung', url: '#/anmeldung' },
          { title: 'Namensschilder', url: '#/namensschilder' },
          { title: 'Teilnahmebestätigungen', url: '#/teilnahme' },
        ]
      }, {
        title: 'eduroam',
        items: [
          { title: 'Account-Vergabe', url: '#/eduroam' },
        ],
      }, {
        title: 'Links',
        items: [
          { title: 'Hilfe und Support', url: '#/hilfe' },
          { title: 'Schildergenerator', url: '#', blank: true },
          { title: 'Engelsystem', url: 'http://www.d120.de/engelsystem', blank: true },
          { title: 'Pad Manager', url: 'http://www.d120.de/pad', blank: true },
          { title: 'Orga-Wiki', url: 'https://orga.fachschaften.org/projects/kif-orga-440/issues', blank: true },
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
