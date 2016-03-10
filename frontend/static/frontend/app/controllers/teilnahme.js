(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('teilnahmeCtrl', ['$scope', '$window', 'toolbarService', function($scope, $window, toolbarService) {

    toolbarService.title('Teilnahmebestätigungen erstellen');

    $scope.filterChoice = 'all';

    $scope.generate = function() {
      var search = '';
      if ($scope.filterChoice === 'nickname') {
        search = '?nickname=' + encodeURIComponent($scope.filterValue);
      } else if ($scope.filterChoice === 'hochschule') {
        search = '?hochschule=' + encodeURIComponent($scope.filterValue);
      }
      $window.open('api/v1/reports/' + search, '_blank');
    };

  }]);

})( window, document );
