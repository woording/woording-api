app.controller('MainController', function($scope, $http, $window) {
	$scope.title = 'Wording';

	// json loading functions
	$scope.loadUser = function(url){
		$http.get('http://127.0.0.1:5000' + url).
			success(function(data, status, headers, config) {
				window.history.pushState('page2', 'Title', url);
				$scope.userData = data;
				$scope.listData = 0;
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			});
	};

	$scope.loadList = function(url){
		$http.get('http://127.0.0.1:5000' + url).
			success(function(data, status, headers, config) {
				window.history.pushState('page2', 'Title', url);
				$scope.listData = data;
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			});
	};

	$scope.getRandomWord = function(){
		if($scope.listData){
			$scope.randomWord = $scope.listData.words[Math.floor(Math.random() * $scope.listData.words.length)];
			$window.randomWord = $scope.randomWord;
		}
	};
});
