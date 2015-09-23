app.controller('MainController', function($scope, $http, $window, ngDialog, $interval, $cookies) {
	$scope.title = 'Wording';
	$scope.Object = Object;
	$scope.apiAdress = 'http://127.0.0.1:5000';

	$scope.sizeOf = function(obj) {
		return Object.keys(obj).length;
	};

	$scope.error = null;
	$scope.isOwner = true;
	$scope.prefferedLanguage = "eng"; // Need a way to set this
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
		shared_with: "",
		words: []
	};
	$scope.importData = {
		name: "",
		language1: "",
		language2: ""
	}

	// load translations from translations.json
	$http.get('/translations.json').then(function(result) {
		console.log(result.data[$scope.prefferedLanguage])
		$scope.translations = result.data[$scope.prefferedLanguage];
	});

	// Switch language on page
	$scope.switchLanguage = function(newLanguage) {
		$scope.prefferedLanguage = newLanguage;
		$http.get('/translations.json').then(function(result) {
			$scope.translations = result.data[$scope.prefferedLanguage];
		});
	};

	// Dialogs
	$scope.openSignUp = function() {
		ngDialog.open({
			template:'\
				<h1>[[ translations.login.signup ]]</h1><br>\
				<p ng-if="error" class="error">[[ error ]]</p>\
				<form ng-submit="registerUser()">\
					<table>\
						<tr>\
							<td>[[ translations.login.username ]]: </td>\
							<td><input type="text" ng-model="user.username" name="username" placeholder="[[ translations.login.username ]]"></td>\
						</tr>\
						<tr>\
							<td>[[ translations.login.password ]]: </td>\
							<td><input type="password" ng-model="user.password" name="password" placeholder="[[ translations.login.password ]]"></td>\
						</tr>\
						<tr>\
							<td>[[ translations.login.email ]]: </td>\
							<td><input type="email" ng-model="user.email" name="email" placeholder="[[ translations.login.email ]]"></td>\
						</tr>\
					</table>\
					<input type="submit" value="[[ translations.login.signup ]]">\
				</form>',
			plain:true,
			scope:$scope
		});
	};
	$scope.openLogIn = function() {
		ngDialog.open({
			template:'\
				<h1>[[ translations.login.login ]]</h1><br>\
				<p ng-if="error" class="error">[[ error ]]</p>\
				<form ng-submit="loginUser()">\
					<table>\
						<tr>\
							<td>[[ translations.login.username ]]: </td>\
							<td><input type="text" ng-model="user.username" name="username" placeholder="[[ translations.login.username ]]"></td>\
						</tr>\
						<tr>\
							<td>[[ translations.login.password ]]: </td>\
							<td><input type="password" ng-model="user.password" name="password" placeholder="[[ translations.login.password ]]"></td>\
						</tr>\
					</table>\
					<input type="submit" value="[[ translations.login.login ]]"> <a ng-click="openSignUp()">[[ translations.login.option ]]</a>\
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
		$http.post($scope.apiAdress + '/authenticate', data)
			.success(function(data, status, headers, config) {
				if (data.indexOf('ERROR') > -1) {
					if (data == 'ERROR, Email not verified') $scope.error = $scope.translations.errors.emailNotVerified;
				} else {
					$scope.user.token = data;
					$scope.loggedIn = true;
					$scope.loadUser("/" + username);

					// First delete before saving cookies
					$cookies.remove('user');
					$cookies.remove('loggedIn');
					// Save Cookies
					$cookies.put('loggedIn', $scope.loggedIn);
					$cookies.putObject('user', $scope.user);

					ngDialog.closeAll();
					$scope.error = null;
				}
			}).error(function(data, status, headers, config) {
				console.error("could not authenticate");
				// If error is 401 display it...
				if (status == 401) $scope.error = $scope.translations.errors.validation;
				else $scope.error = $scope.translations.errors.unknown;
			});
	};

	$scope.registerUser = function() {
		if ($scope.user.username && $scope.user.password && $scope.user.email) {
			data = {
				'username':this.user.username,
				'password':this.user.password,
				'email':this.user.email
			};
			$http.post($scope.apiAdress + '/register', data)
				.success(function(data, status, headers, config) {
					if (data.indexOf("ERROR") > - 1) {
						// An error...
						if (data == "ERROR, not everything filled in") {
							$scope.error = $scope.translations.errors.notEverythingFilledIn;
						} else if (data == "ERROR, username and/or email do already exist") {
							$scope.error = $scope.translations.errors.alreadyExist;
						}
					} else {
						// Give success
						console.log("Verify email");
						ngDialog.close('registerDialog');
						$scope.error = null;
					}
					console.log($scope.error);
				}).error(function(data, status, headers, config) {
					// Give registration error
					console.error("Failed");
					$scope.error = $scope.translations.errors.unknown;
				});
			// Reset the values
			$scope.user.password = ''
		} else $scope.error = $scope.translations.errors.notEverythingFilledIn;
	};

	$scope.loginUser = function() {
		console.log('Start logging in');
		if ($scope.user.username && $scope.user.password) {
			$scope.authenticate(this.user.username, this.user.password);
			// Reset the fields
			$scope.user.password = '';
		} else $scope.error = $scope.translations.errors.notEverythingFilledIn;
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
	};

	$scope.oldUrl = '';
	$scope.currentUrl = '';

	$scope.checkUrl = function(){
		$scope.oldUrl = $scope.currentUrl;
		$scope.currentUrl = window.location.href.split('/');
		var index = $scope.currentUrl.length;

		if ($scope.currentUrl.length < $scope.oldUrl.length){
			ngDialog.close();
			left.style.display = 'inline-block';
			middle.style.display = 'inline-block';
			right.style.display = 'none';
			practice.style.display = 'none';
		}

		else if ($scope.oldUrl && $scope.currentUrl.length > $scope.oldUrl.length) {
			right.style.display = 'inline-block';
		}

		else if ($scope.oldUrl && $scope.currentUrl.length == $scope.oldUrl.length && $scope.currentUrl[index - 1] != $scope.oldUrl[index - 1]) {
			console.log('changed');
			$scope.loadList('/' + $scope.currentUrl[index - 2] + '/' + $scope.currentUrl[index - 1]);
		}
	};

	$interval($scope.checkUrl, 100);

	// json loading functions
	// Password list for users that are in the database
	// cor 		Hunter2
	// leon		all_i_see_is_*****
	// philip	***hunter***
	$scope.loadUser = function(url){
		$http.post($scope.apiAdress + url, { 'token':$scope.user.token })
			.success(function(data, status, headers, config) {
				if (data.username == 'ERROR, No token' || data.username == 'ERROR, No user') {
					// Show login screen
					$scope.openLogIn();
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
		showList();

		if ($scope.userData.username != $scope.user.username) $scope.isOwner = false;
		else $scope.isOwner = true;

		$http.get($scope.apiAdress + url).
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
			words: [],
			shared_with: "",
		};

		for (i = 0; i < 3; i++) {
			$scope.editData.words[i] = {
				language_1_text: "",
				language_2_text: ""
			}
		}
	};

	$scope.importList = function() {
		ngDialog.open({
			template: '\
				<h1>[[ translations.import.title ]]</h1><br>\
				<p>[[ translations.import.desc ]]</p>\
				<table>\
					<tr>\
						<td>[[ translations.import.name ]]: </td>\
						<td><input type="text" ng-model="importData.name"></td>\
					</tr>\
					<tr>\
						<td>[[ translations.import.language1 ]]: </td>\
						<td>\
							<select ng-model="importData.language1" value="">\
								<option value="">[[ translations.listControls.language1 ]]</option>\
								<option ng-repeat="language in translations.languages" value="[[ language.iso ]]">[[ language.displayText ]]</option>\
							</select>\
						</td>\
					</tr>\
					<tr>\
						<td>[[ translations.import.language2 ]]: </td>\
						<td>\
							<select ng-model="importData.language2" value="">\
								<option value="">[[ translations.listControls.language2 ]]</option>\
								<option ng-repeat="language in translations.languages" value="[[ language.iso ]]">[[ language.displayText ]]</option>\
							</select>\
						<td>\
					</tr>\
					<tr>\
						<td>[[ translations.sharing.sharedWith ]]? </td>\
						<td>\
							<select ng-model="importData.shared_with" value="">\
								<option value="">[[ translations.sharing.sharedWith ]]?</option>\
								<option value="0">[[ translations.sharing.nobody ]]</option>\
								<option value="1">[[ translations.friends ]]</option>\
								<option value="2">[[ translations.sharing.everybody ]]</option>\
							</select>\
						</td>\
					</tr>\
				</table>\
				<textarea id="import_area" name="" cols="30" rows="10"></textarea>\
				<button ng-click="submitImportedList()">[[ translations.import.title ]]</button>\
			',
			plain:true,
			scope:$scope
		});
	}

	$scope.submitImportedList = function() {
		var words = document.getElementById('import_area').value.split(/ = |=|\n/g);
		var wordObjectArray = [];
		console.log(wordObjectArray)
		for (var i = 0, x = words.length; i < x; i+=2){
			wordObjectArray.push({
				language_1_text: words[i],
				language_2_text: words[i+1]
			});
		}

		console.log(words);
		$scope.editData = { // Hard coded
			listname: $scope.importData.name,
			language_1_tag: $scope.importData.language1,
			language_2_tag: $scope.importData.language2,
			words: wordObjectArray
		}

		console.log($scope.editData);

		$scope.saveList();
		ngDialog.close();
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
	};

	$scope.saveList = function() {
		var data = {
			'username':$scope.user.username,
			'list_data':$scope.editData,
			'token':$scope.user.token
		};
		console.log(data);
		$http.post($scope.apiAdress + '/savelist', data)
			.success(function(data, status, headers, config) {
				console.log('saved');
				$scope.loadUser('/' + $scope.userData.username);
				$scope.loadList('/' + $scope.userData.username + '/' + $scope.editData.listname);
				$scope.editData = null;

				if (!$scope.isOwner) {
					alert("Edited list saved on own account.")
				}
			}).error(function(data, status, headers, config) {
				console.error('error');
			});
	};

	$scope.deleteList = function(listname) {
		var data = {
			'username':$scope.userData.username,
			'listname':listname,
			'token':$scope.user.token
		};
		$http.post($scope.apiAdress + '/deleteList', data)
			.success(function(data, status, headers, config) {
				$scope.loadUser('/' + $scope.userData.username);
				listData = null;
				editData = null;
			}).error(function(data, status, headers, config){
				console.error('Error while deleting list')
			});
	};

	// Start practice
	$scope.startList = function(){
		$http.get('/translations.json').then(function(result) {
			$scope.translations = result.data[$scope.prefferedLanguage];
			for(var i = 0, x = $scope.translations.languages.length; i < x; i++){
				if ($scope.translations.languages[i].iso == $scope.listData.language_1_tag){
					$scope.firstLanguage = $scope.translations.languages[i].displayText;
				}

				else if ($scope.translations.languages[i].iso == $scope.listData.language_2_tag){
					$scope.secondLanguage = $scope.translations.languages[i].displayText;
				}
			}
			
			ngDialog.open({
				template:'\
					<h1>[[ translations.practice.options ]]</h1>\
					<br>\
					[[ translations.practice.questionedLanguage ]]?<br>\
					<form>\
						<input type="radio" name="language" value="first" id="firstLanguage"> ' + $scope.firstLanguage + '\
						<br>\
						<input type="radio" name="language" value="second" id="secondLanguage"> ' + $scope.secondLanguage + '\
						<br>\
						<input type="radio" name="language" value="both" id="bothLanguages"> [[ translations.practice.both ]]\
						<br>\
						<input type="submit" ng-click="chooseLanguage()" value="[[ translations.practice.start ]]">\
						<br>\
					</form>\
					',
				plain:true,
				scope:$scope,
				closeByEscape: false,
				closeByDocument: false,
				showClose: false
			});
		});


		$scope.getRandomWord();
		$scope.numberOfQuestions = $scope.listData.words.length;
		document.getElementById('words_left').innerHTML = $scope.numberOfQuestions;
	};

	$scope.chooseLanguage = function(){
		if (document.getElementById('firstLanguage').checked) {
			$scope.questionedLanguage = true;
		}

		else if (document.getElementById('secondLanguage').checked){
			$scope.questionedLanguage = false;
		}

		else if (document.getElementById('bothLanguages').checked){
			document.getElementById('words_left').innerHTML *= 2;
			for (var i = 0, x = $scope.listData.words.length; i < x; i++){
				$scope.listData.words.push({
					language_1_text: $scope.listData.words[i].language_2_text,
					language_2_text: $scope.listData.words[i].language_1_text
				});
			}
		}

		ngDialog.close();
	};

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

		$scope.checkWord(this.text, $scope.randomWord);
		this.text = '';
	};

	$scope.checkWord = function(wordOne, wordTwo){
		wordTwo = $scope.questionedLanguage ? wordTwo.language_2_text : wordTwo.language_1_text
		if(wordOne == wordTwo){
			document.getElementById('words_left').innerHTML--;
			document.getElementById('correct').innerHTML++;
			$scope.getRandomWord();
		}

		else {
			document.getElementById('words_left').innerHTML++;
			document.getElementById('wrong_word').innerHTML = wordTwo;
			document.getElementById('wrong_word').style.color = 'red';
			if ($scope.usedWords.indexOf(wordTwo) > -1){
				$scope.usedWords.splice($scope.usedWords.indexOf(wordTwo));
			}

			document.getElementById('incorrect').innerHTML++;

			$scope.numberOfQuestions++;
			$scope.incorrectWords.push({
				correctWord: wordTwo,
				incorrectWord: wordOne
			});
		}

		console.log($scope.usedWords);
	};
});
