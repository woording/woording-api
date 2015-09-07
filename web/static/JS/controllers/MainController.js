app.controller('MainController', function($scope, $http) {
	$scope.title = 'Wording';

	// json loading functions
	$scope.loadUser = function(url){
		$http.get('http://127.0.0.1:5000' + url).
			success(function(data, status, headers, config) {
			window.history.pushState('page2', 'Title', url);
				$scope.userData = data;
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			});
	};

	$scope.loadList = function(url){
		$http.get('http://127.0.0.1:5000' + url).
			succes(function(data, status, headers, config) {
				$scope.listData = data;
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			});
	};
});
