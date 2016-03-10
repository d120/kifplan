(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.config(['$routeProvider', function($routeProvider) {

    $routeProvider
      .when('/login', {
        templateUrl: 'static/frontend/partials/login.html',
        controller: 'loginCtrl'
      })
      .whenAuthenticated('/kiffels', {
        templateUrl: 'static/frontend/partials/kiffels.html',
        controller: 'kiffelsCtrl'
      })
      .whenAuthenticated('/kiffels/:id', {
        templateUrl: 'static/frontend/partials/kiffel.html',
        controller: 'kiffelCtrl'
      })
      .whenAuthenticated('/anmeldung', {
        templateUrl: 'static/frontend/partials/anmeldung.html',
        controller: 'anmeldungCtrl'
      })
      .whenAuthenticated('/namensschilder', {
        templateUrl: 'static/frontend/partials/namensschilder.html',
        controller: 'namensschilderCtrl'
      })
      .whenAuthenticated('/teilnahme', {
        templateUrl: 'static/frontend/partials/teilnahme.html',
        controller: 'teilnahmeCtrl'
      })
      .whenAuthenticated('/hilfe', {
        templateUrl: 'static/frontend/partials/hilfe.html',
        controller: 'hilfeCtrl'
      })
      .whenAuthenticated('/schilder', {
        templateUrl: 'static/frontend/partials/schilder.html',
        controller: 'schilderCtrl'
      })
      .otherwise({
        redirectTo: '/anmeldung'
      });

  }]);

})( window, document );
