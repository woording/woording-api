app.controller('MainController', function($scope, $http) {
	$scope.title = 'Wording';
	$scope.loadData = function(url){
		$http.get('http://127.0.0.1:5000' + url).
			success(function(data, status, headers, config) {
				$scope.jsonData = data;
				window.history.pushState('page2', 'Title', url);
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			}); 
	}	
	$scope.loadData(window.location.pathname);
});
