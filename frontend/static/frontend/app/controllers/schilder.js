(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('schilderCtrl', ['$scope', '$window', 'toolbarService', function($scope, $window, toolbarService) {

    toolbarService.title('Schildergenerator');

    $scope.generate = function() {
      $window.open('api/v1/signs/?text=' + $scope.text, '_blank');
    };

  }]);

})( window, document );
