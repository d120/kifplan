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
      .otherwise({
        redirectTo: '/kiffels'
      });

  }]);

})( window, document );
