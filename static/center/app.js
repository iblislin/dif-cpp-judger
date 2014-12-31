(function(){
	var app = angular.module('center', ['ngRoute',
							 'angularFileUpload', 'angular-loading-bar'])
	.config(['$interpolateProvider', '$httpProvider', '$routeProvider',
			'cfpLoadingBarProvider',
		function($interpolateProvider, $httpProvider, $routeProvider,
				cfpLoadingBarProvider) {
			$interpolateProvider.startSymbol('[[');
			$interpolateProvider.endSymbol(']]');

			$httpProvider.defaults.xsrfCookieName = 'csrftoken';
			$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
			$httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';

			cfpLoadingBarProvider.latencyThreshold = 100
			cfpLoadingBarProvider.includeSpinner = false


			$routeProvider.
				when('/?', {
					templateUrl: url.judge.list,
					controllen: 'CenterController',
				}).
				when('/judge/list/:page?/',{
					templateUrl: url.judge.list,
					controller: 'JudgeListController',
				}).
				when('/judge/detail/:qid/', {
					templateUrl: function(urlattr){
						return url.judge.detail + urlattr.qid + '/'
					},
					controller: 'JudgeDetailController',
				})
	}])

	app.controller('CenterController', ['$scope', '$http',
	function($scope, $http){
		var self = this
	}])
	app.controller('JudgeListController', ['$scope', '$http',
	function($scope, $http){
		var self = this
	}])
	app.controller('JudgeDetailController', ['$scope', '$http', '$upload',
				   '$routeParams',
	function($scope, $http, $upload, $routeParams){
		var self = this
		var upload_url = url.judge.upload + $routeParams.qid + '/'

		$scope.result_url = ''
		$scope.upload_progress = 0
		$scope.$watch('upload_file', function(){
			if (! $scope.upload_file)
				return

			var f = $scope.upload_file

			console.log(f)
			$scope.upload_progress = 0
			$scope.upload = $upload.upload({
				url: upload_url,
				method: 'POST',
				file: f,
			}).progress(function(evt){
				$scope.upload_progress = parseInt(100.0 * evt.loaded / evt.total)
			}).success(function(d){
				console.log(d)
				$scope.result_url = d.result_url
			}).error(function(d){
				console.log(d)
			})
		})

	}])
})();
