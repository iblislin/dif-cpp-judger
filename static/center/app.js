(function(){
	var app = angular.module('center', ['ngRoute'])
	.config(['$interpolateProvider', '$httpProvider', '$routeProvider',
		function($interpolateProvider, $httpProvider, $routeProvider) {
			$interpolateProvider.startSymbol('[[');
			$interpolateProvider.endSymbol(']]');

			$httpProvider.defaults.xsrfCookieName = 'csrftoken';
			$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
			$httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';

			$routeProvider.
				when('/', {
					templateUrl: url.judge.list,
					controller: 'CenterController',
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
	app.controller('JudgeDetailController', ['$scope', '$http',
	function($scope, $http){
		var self = this
	}])
})();
