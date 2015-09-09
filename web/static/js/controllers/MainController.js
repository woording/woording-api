app.controller('MainController', function($scope, $http, $window) {
	$scope.title = 'Wording';

	$scope.authenticate = function(username, password) {
		var data = {
			'username':username,
			'password':password
		};
		$http.post('http://127.0.0.1:5000/authenticate', data)
			.success(function(data, status, headers, config) {
				$scope.loadUser("/" + username);
				console.log(data);
			}).error(function(data, status, headers, config) {
				console.error("could not authenticate");
				// Function to go to home page
			});
	};

	// json loading functions
	$scope.loadUser = function(url){
		$http.get('http://127.0.0.1:5000' + url)
			.success(function(data, status, headers, config) {
				if (data.username == 'ERROR: This shouldn\'t happen') {
					$scope.authenticate("me", "password"); // Angular should get these values, now there is no function for it...
				} else {
					window.history.pushState('page2', 'Title', url);
					$scope.userData = data;
					$scope.listData = 0;
				}
			})
			.error(function(data, status, headers, config) {
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
