app.controller('MainController', function($scope, $http, $window) {
	$scope.title = 'Wording';
	$scope.token = "";

	$scope.username = "";
	$scope.password = "";
	$scope.email = "";

	$scope.authenticate = function(username, password) {
		var data = {
			'username':username,
			'password':password
		};
		$http.post('http://127.0.0.1:5000/authenticate', data)
			.success(function(data, status, headers, config) {
				$scope.token = data;
				$scope.loadUser("/" + username);
			}).error(function(data, status, headers, config) {
				console.error("could not authenticate");
				// If error is 401 display it...
				// Function to go to home page
			});
	};

	$scope.registerUser = function() {
		if ($scope.username && $scope.password && $scope.email) {
			data = {
				'username':this.username,
				'password':this.password,
				'email':this.email
			};
			$http.post('http://127.0.0.1:5000/register', data)
				.success(function(data, status, headers, config) {
					// Give success
					console.log("Verify email")

				}).error(function(data, status, headers, config) {
					// Give registration error
					console.error("Failed")
				});
			// Reset the values
			$scope.username = ''
			$scope.password = ''
			$scope.email = ''
		}
	}

	$scope.loginUser = function() {
		if ($scope.username && $scope.password) {
			$scope.authenticate(this.username, this.password);
		}
		$scope.username = '';
		$scope.password = '';
	}

	// Password list for users that are in the database
	// cor 		Hunter2
	// leon		all_i_see_is_*****
	// philip	***hunter***

	// json loading functions
	$scope.loadUser = function(url){
		$http.post('http://127.0.0.1:5000' + url, { 'token':$scope.token })
			.success(function(data, status, headers, config) {
				if (data.username == 'ERROR, No token' || data.username == 'ERROR, No user') {
					// Should show login screen
					$scope.authenticate("cor", "Hunter2"); // Angular should get these values, now there is no function for it...
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
		$scope.usedWords = [];
		$scope.incorrectWords = [];

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
		if ($scope.usedWords.length == $scope.listData.words.length){
			showResults();
			setResult($scope.usedWords.length, $scope.incorrectWords.length);
			return true;
		}

		if($scope.listData){
			$scope.randomWord = $scope.listData.words[Math.floor(Math.random() * $scope.listData.words.length)];

			if ($scope.usedWords.indexOf($scope.randomWord) > -1){
				$scope.getRandomWord();
			}

			else {
				$scope.usedWords.push($scope.randomWord)
			}
		}
	};

	$scope.usedWords = [];
	$scope.incorrectWords = [];

	$scope.submit = function(){
		document.getElementById('wrong_word').innerHTML = '';

		if ($scope.text || !$scope.text) {
			$scope.checkWord(this.text, $scope.randomWord);
			this.text = '';
        }
	}

	$scope.checkWord = function(wordOne, wordTwo){
		if(wordOne == wordTwo.language_2_text){
			document.getElementById('correct').innerHTML++;
			$scope.getRandomWord();
		}

		else {
			document.getElementById('wrong_word').innerHTML = wordTwo.language_2_text;
			document.getElementById('wrong_word').style.color = 'red';
			$scope.usedWords.splice($scope.usedWords.indexOf(wordTwo));
			document.getElementById('incorrect').innerHTML++;

			$scope.incorrectWords.push({
				correctWord: wordTwo.language_2_text,
				incorrectWord: wordOne
			});
		}

		console.log($scope.usedWords);
	}
});
