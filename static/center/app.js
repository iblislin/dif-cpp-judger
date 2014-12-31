(function(){
	var app = angular.module('center', ['ngRoute', 'angularFileUpload'])
	.config(['$interpolateProvider', '$httpProvider', '$routeProvider',
		function($interpolateProvider, $httpProvider, $routeProvider) {
			$interpolateProvider.startSymbol('[[');
			$interpolateProvider.endSymbol(']]');

			$httpProvider.defaults.xsrfCookieName = 'csrftoken';
			$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
			$httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';

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
	function($scope, $http, $upload){
		var self = this

		$scope.uploader = new FileUploader({
			headers: {
				'X-Requested-With': 'XMLHttpRequest'
			}
		})
		$scope.uploader.onErrorItem = function(i, d){
				console.log(d)
		}
		$scope.upload_code = function(item){
			item.url = $scope.upload_url
			console.log(item.url)
			item.upload()
		}
	}])
})();
