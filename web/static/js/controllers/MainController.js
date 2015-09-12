app.controller('MainController', function($scope, $http, $window, ngDialog) {
	$scope.title = 'Wording';
	
	$scope.user = {
		token	:	"",

		username:	"",
		password:	"",
		email	:	""
	};

	// Dialogs
	$scope.openSignUp = function() {
		ngDialog.open({ 
			template:'\
				<h1>Sign Up</h1><br>\
				<form ng-submit="registerUser()">\
					<!-- Need to do style... -->\
					Username: <input type="text" ng-model="user.username" name="username" placeholder="Username"><br>\
					Password: <input type="password" ng-model="user.password" name="password" placeholder="Password"><br>\
					Email:    <input type="email" ng-model="user.email" name="email" placeholder="Email"><br>\
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
					Username: <input type="text" ng-model="user.username" name="username" placeholder="Username"><br>\
					Password: <input type="password" ng-model="user.password" name="password" placeholder="Password"><br>\
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
				$scope.loadUser("/" + username);
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
			$scope.user.username = ''
			$scope.user.password = ''
			$scope.user.email = ''
		}
	};

	$scope.loginUser = function() {
		console.log('Start loggin in')
		if ($scope.user.username && $scope.user.password) {
			$scope.authenticate(this.user.username, this.user.password);
			// Reset the fields
			$scope.user.username = '';
			$scope.user.password = '';
		}
	};

	// Password list for users that are in the database
	// cor 		Hunter2
	// leon		all_i_see_is_*****
	// philip	***hunter***

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
		$http.get('http://127.0.0.1:5000' + url).
			success(function(data, status, headers, config) {
				window.history.pushState('page2', 'Title', url);
				$scope.listData = data;
			}).
			error(function(data, status, headers, config) {
				console.log("error");
			});
	};

	// Practice lists
	$scope.getRandomWord = function(){
		if ($scope.usedWords.length == $scope.listData.words.length){
			document.getElementById('current_word').innerHTML = 'DONE';
			console.log('done');
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

	$scope.submit = function(){
		document.getElementById('wrong_word').innerHTML = '';

		if ($scope.text || !$scope.text) {
			$scope.checkWord(this.text, $scope.randomWord);
			this.text = '';
        }
	};

	$scope.checkWord = function(wordOne, wordTwo){
		if(wordOne == wordTwo.language_2_text){
			console.log('correct');
			$scope.getRandomWord();
		}

		else {
			document.getElementById('wrong_word').innerHTML = wordTwo.language_2_text;
			document.getElementById('wrong_word').style.color = 'red';
			$scope.usedWords.splice($scope.usedWords.indexOf(wordTwo));
		}

		console.log($scope.usedWords);
	};
});
