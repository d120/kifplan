(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.config(['$routeProvider', function($routeProvider) {

    $routeProvider
      .when('/', {
        templateUrl: 'static/frontend/partials/hello-world.html'
      })
      .otherwise({
        redirectTo: '/'
      });

  }]);

})( window, document );
