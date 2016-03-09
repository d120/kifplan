(function (window, document, undefined) {

  "use strict";

  var app = angular.module('kiffel', [
    'ngMaterial', 'ngRoute', 'ngMdIcons', 'restangular', 'angular-underscore'
  ]);

  app.config(['$mdThemingProvider', function($mdThemingProvider) {
    $mdThemingProvider
      .theme('default')
      .primaryPalette('light-green', {
        'default': '300'
      })
      .accentPalette('green', {
        'default': '500'
      });
  }]);

})( window, document );
