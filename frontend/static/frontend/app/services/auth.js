(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.factory('authService', ['$rootScope', '$http', '$q', '$location', function($rootScope, $http, $q, $location) {

    var nextPath = '/';

    return {
      checkLoggedIn: function($q, $rootScope, $location) {
        var deferred = $q.defer();
        if ($rootScope.user && $rootScope.user.authenticated === true) {
            deferred.resolve();
        } else {
            nextPath = $location.path();
            $location.path('/login');
            deferred.reject({ needsAuthentication: true });
        }
        return deferred.promise;
      },

      loadLoginStatus: function() {
        if (window.localStorage) {
          if (localStorage.getItem('user')) {
            $rootScope.user = JSON.parse(localStorage.getItem('user'));
          } else {
            $rootScope.user = { authenticated: false };
          }
        }
      },

      getNextPath: function() {
        return nextPath === '/login' ? '/' : nextPath;
      },

      login: function(username, password) {
        $rootScope.user = {
          authenticated: true,
          username: username,
          password: password
        };
        if (window.localStorage) {
          localStorage.setItem('user', JSON.stringify($rootScope.user));
        }
      },

      logout: function() {
        $rootScope.user = { authenticated: false };
        if (window.localStorage) {
          localStorage.setItem('user', JSON.stringify($rootScope.user));
        }
      }
    };
  }]);

})( window, document );
