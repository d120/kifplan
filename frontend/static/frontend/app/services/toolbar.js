(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.factory('toolbarService', [function() {

    var title = "Kiffel Verwaltung";

    var receivers = [];
    var notifyAll = function() {
      receivers.forEach(function(callback) { callback(); });
    };

    return {
      title: function(_title) {
        if (_title) {
          title = _title;
          notifyAll();
        }
        return title;
      },
      registerReceiver: function(callback) {
        receivers.push(callback);
      }
    };
  }]);

})( window, document );
