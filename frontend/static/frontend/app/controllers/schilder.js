(function (window, document, undefined) {

  "use strict";
  var app = angular.module('kiffel');

  app.controller('schilderCtrl', ['$scope', '$window', 'toolbarService', function($scope, $window, toolbarService) {

    toolbarService.title('Schildergenerator');

    $scope.template = 'headline-top_arrowdown_text-right.tex';

    $scope.generate = function() {
      var search = '?text=' + $scope.text + '&headline=' + $scope.headline + '&template=' + $scope.template;
      $window.open('api/v1/signs/'+search, '_blank');
    };

  }]);

})( window, document );
