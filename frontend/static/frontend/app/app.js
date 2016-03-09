(function (window, document, undefined) {

  "use strict";

  var app = angular.module('kiffel', [
    'ngMaterial', 'ngRoute', 'ngMdIcons', 'restangular', 'angular-underscore'
  ]);

  app.config(['$mdThemingProvider', function($mdThemingProvider) {
    $mdThemingProvider
      .theme('default')
      .primaryPalette('indigo', {
        'default': '300'
      })
      .accentPalette('pink', {
        'default': '500'
      });
  }]);

  app.run(['authService', function(authService) {
    authService.loadLoginStatus();
  }]);

  app.config(['$routeProvider', function($routeProvider) {
    var checkLoggedIn = function($q, $rootScope, $location, authService) {
      return authService.checkLoggedIn($q, $rootScope, $location);
    };

    $routeProvider.whenAuthenticated = function(path, route) {
      route.resolve = route.resolve || {};
      angular.extend(route.resolve, {
        isLoggedIn: ['$q', '$rootScope', '$location', 'authService', checkLoggedIn]
      });
      return $routeProvider.when(path, route);
    };
  }]);

  app.config(['RestangularProvider', function(RestangularProvider) {
    RestangularProvider.setBaseUrl('api/v1');
  }]);

  app.factory('HeaderedRestangular', ['Restangular', function (Restangular) {
    return Restangular.withConfig(function (RestangularConfigurer) {
      RestangularConfigurer.setFullResponse(true);
    });
  }]);

})( window, document );
