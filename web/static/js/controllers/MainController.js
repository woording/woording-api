app.controller('MainController', function($scope, $http, $window, ngDialog, $interval, $cookies) {
	$scope.title = 'Wording';
	$scope.Object = Object;

	$scope.sizeOf = function(obj) {
	    return Object.keys(obj).length;
	};

	$scope.loggedIn = $cookies.get('loggedIn') ? $cookies.get('loggedIn') : false;
	$scope.user = $cookies.getObject('user') ? $cookies.getObject('user') : {
		token	:	"",

		username:	"",
		password:	"",
		email	:	""
	};
	$scope.editData = {
		listname: "",
		language_1_tag: "",
		language_2_tag: "",
		words: []
	};

	// Dialogs
	$scope.openSignUp = function() {
		ngDialog.open({
			template:'\
				<h1>Sign Up</h1><br>\
				<form ng-submit="registerUser()">\
					<!-- Need to do style... -->\
					<table>\
						<tr>\
							<td>Username: </td>\
							<td><input type="text" ng-model="user.username" name="username" placeholder="Username"></td>\
						</tr>\
						<tr>\
							<td>Password: </td>\
							<td><input type="password" ng-model="user.password" name="password" placeholder="Password"></td>\
						</tr>\
						<tr>\
							<td>Email: </td>\
							<td><input type="email" ng-model="user.email" name="email" placeholder="Email"></td>\
						</tr>\
					</table>\
					<input type="submit" value="Sign Up">\
				</form>',
			plain:true,
			scope:$scope
		});
	};
	$scope.openLogIn = function() {
		ngDialog.open({
			template:'\
				<h1>Log In</h1><br>\
				<form ng-submit="loginUser()">\
					<!-- Need to do style... -->\
					<table>\
						<tr>\
							<td>Username: </td>\
							<td><input type="text" ng-model="user.username" name="username" placeholder="Username"></td>\
						</tr>\
						<tr>\
							<td>Password: </td>\
							<td><input type="password" ng-model="user.password" name="password" placeholder="Password"></td>\
						</tr>\
					</table>\
					<input type="submit" value="Log In"> <a ng-click="openSignUp()">Or Sign Up</a>\
				</form>',
			plain:true,
			scope:$scope
		});
	};

	// Authentication functions
	$scope.authenticate = function(username, password) {
		var data = {
			'username':username,
			'password':password
		};
		$http.post('http://127.0.0.1:5000/authenticate', data)
			.success(function(data, status, headers, config) {
				$scope.user.token = data;
				$scope.loggedIn = true;
				$scope.loadUser("/" + username);

				// First delete before saving cookies
				$cookies.remove('user');
				$cookies.remove('loggedIn');
				// Save Cookies
				$cookies.put('loggedIn', $scope.loggedIn);
				$cookies.putObject('user', $scope.user);

				ngDialog.closeAll()
			}).error(function(data, status, headers, config) {
				console.error("could not authenticate");
				// If error is 401 display it...
				// Function to go to home page
			});
	};

	$scope.registerUser = function() {
		if ($scope.user.username && $scope.user.password && $scope.user.email) {
			data = {
				'username':this.user.username,
				'password':this.user.password,
				'email':this.user.email
			};
			$http.post('http://127.0.0.1:5000/register', data)
				.success(function(data, status, headers, config) {
					// Give success
					console.log("Verify email")
					ngDialog.close('registerDialog')
				}).error(function(data, status, headers, config) {
					// Give registration error
					console.error("Failed")
				});
			// Reset the values
			$scope.user.password = ''
		}
	};

	$scope.loginUser = function() {
		console.log('Start logging in')
		if ($scope.user.username && $scope.user.password) {
			$scope.authenticate(this.user.username, this.user.password);
			// Reset the fields
			$scope.user.password = '';
		}
	};

	$scope.logoutUser = function() {
		$scope.loggedIn = false;
		$scope.user.username = '';
		$scope.user.token = '';
		$scope.user.email = '';

		// Remove the cookies
		$cookies.remove('user');
		$cookies.remove('loggedIn');

		// Need function to go to main page
	}

	// Password list for users that are in the database
	// cor 		Hunter2
	// leon		all_i_see_is_*****
	// philip	***hunter***

	$scope.oldUrl = '';
	$scope.currentUrl = '';

	$scope.checkUrl = function(){
		$scope.oldUrl = $scope.currentUrl;
		$scope.currentUrl = window.location.href.split('/');

		if ($scope.currentUrl.length < $scope.oldUrl.length){
			left.style.display = 'block';
			middle.style.display = 'block';
			right.style.display = 'none';
			practice.style.display = 'none';
		}

		else if ($scope.oldUrl && $scope.currentUrl.length > $scope.oldUrl.length) {
			right.style.display = 'block';
		}
	}

	$interval($scope.checkUrl, 100);

	// json loading functions
	$scope.loadUser = function(url){
		$http.post('http://127.0.0.1:5000' + url, { 'token':$scope.user.token })
			.success(function(data, status, headers, config) {
				if (data.username == 'ERROR, No token' || data.username == 'ERROR, No user') {
					// Should show login screen
					$scope.openLogIn();
					//$scope.authenticate("cor", "Hunter2"); // Angular should get these values, now there is no function for it...
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

	// Create list
	$scope.createList = function() {
		$scope.editData = {
			listname: "",
			language_1_tag: "",
			language_2_tag: "",
			words: []
		}

		for (i = 0; i < 3; i++) {
			$scope.editData.words[i] = {
				language_1_text: "",
				language_2_text: ""
			}		
		}
	}

	$scope.editList = function() {
		$scope.editData = $scope.listData;
		
		var size = $scope.sizeOf($scope.editData.words);
		for (i = 0; i < 3; i++) {
			$scope.editData.words[size] = {
				language_1_text: "",
				language_2_text: ""
			};
		}
	}

	$scope.saveList = function() {
		var data = {
			'username':$scope.userData.username,
			'list_data':$scope.editData
		}
		$http.post('http://127.0.0.1:5000/savelist', data)
			.success(function(data, status, headers, config) {
				console.log('saved');
				$scope.loadUser('/' + $scope.userData.username);
			}).error(function(data, status, headers, config) {
				console.error('error');
			});
	}

	// Start practice
	$scope.startList = function(){
		$scope.getRandomWord();
		$scope.numberOfQuestions = $scope.listData.words.length;
	}

	// Practice lists
	$scope.getRandomWord = function(){
		if ($scope.usedWords.length == $scope.listData.words.length){
			showResults();
			setResult($scope.numberOfQuestions, $scope.incorrectWords.length);
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

	$scope.numberOfQuestions = 0;
	$scope.usedWords = [];
	$scope.incorrectWords = [];

	$scope.submit = function(){
		document.getElementById('wrong_word').innerHTML = '';

		if ($scope.text || !$scope.text) {
			$scope.checkWord(this.text, $scope.randomWord);
			this.text = '';
        }
	};

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

			$scope.numberOfQuestions++;
			$scope.incorrectWords.push({
				correctWord: wordTwo.language_2_text,
				incorrectWord: wordOne
			});
		}

		console.log($scope.usedWords);
	};
});
