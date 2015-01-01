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
				when('/', {
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
				   '$routeParams', '$templateCache', '$timeout',
	function($scope, $http, $upload, $routeParams, $templateCache,
			 $timeout){
		var self = this
		var question_id = $routeParams.qid
		var upload_url = url.judge.upload + question_id + '/'
		var result_url = function(code_id){
			var _url = url.judge.result + question_id + '/'
			if(! code_id)
				return _url
			return _url + code_id + '/'
		}
		var get_code = function(Callback){
			$http.get(result_url()
			).success(function(d){
				console.log(d)
				$scope.code = d.code
				if (typeof Callback == 'function') {
					Callback()
				}
			}).error(function(d){
				console.log(d)
			})
		}
		get_code()

		$scope.upload_progress = 0
		$scope.$watch('upload_file', function(){
			if (! $scope.upload_file)
				return

			var f = $scope.upload_file

			$scope.upload_progress = 0
			$scope.upload = $upload.upload({
				url: upload_url,
				method: 'POST',
				file: f,
			}).success(function(d){
				console.log(d);
				(function reload_result(){
					get_code(function(){
						if ($scope.code.status == 'PD') {
							$timeout(reload_result, 500)
						}
					})
				})();
			}).error(function(d){
				console.log(d)
			})
		})
		$scope.$on('$routeChangeStart', function(event, next, current){
			if (typeof(current) !== 'undefined'){
				$templateCache.remove(current.templateUrl);
			}
		})

	}])
})();
