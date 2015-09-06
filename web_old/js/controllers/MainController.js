app.controller('MainController', function($scope, $http) {
	$scope.title = 'Wording';
	$http.get('http://127.0.0.1:8000/words.json').
		success(function(data, status, headers, config) {
			$scope.jsonData = data;
		}).
		error(function(data, status, headers, config) {
			console.log("error");
		});
});
