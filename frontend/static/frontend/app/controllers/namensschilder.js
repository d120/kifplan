(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('namensschilderCtrl', ['$scope', '$window', 'toolbarService', function($scope, $window, toolbarService) {

    toolbarService.title('Namensschilder erstellen');

    $scope.filterChoice = 'all';

    $scope.generate = function() {
      var search = '';
      if ($scope.filterChoice === 'orga') {
        search = '?ist_orga=True';
      } else if ($scope.filterChoice === 'nickname') {
        search = '?nickname=' + encodeURIComponent($scope.filterValue);
      } else if ($scope.filterChoice === 'hochschule') {
        search = '?hochschule=' + encodeURIComponent($scope.filterValue);
      }
      $window.open('api/v1/nametags/' + search, '_blank');
    };

  }]);

})( window, document );
