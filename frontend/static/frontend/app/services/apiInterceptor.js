(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.service('APIInterceptor', ['$rootScope', function($rootScope) {
    this.request = function(config) {
      if ($rootScope.user && $rootScope.user.authenticated) {
        var username = $rootScope.user.username || '';
        var password = $rootScope.user.password || '';
        config.headers.Authorization = 'Basic ' + btoa(username + ':' + password);
      }
      return config;
    };
  }]);

  app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('APIInterceptor');
  }]);

})( window, document );
