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
      .otherwise({
        redirectTo: '/kiffels'
      });

  }]);

})( window, document );
