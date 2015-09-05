app.controller('MainController', function($scope, $http) {
	$scope.title = 'Wording';
	$http.get('http://127.0.0.1:5000/' + window.location.hash.substring(1)).
		success(function(data, status, headers, config) {
			$scope.jsonData = data;
		}).
		error(function(data, status, headers, config) {
			console.log("error");
		});
});
