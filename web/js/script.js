var data_file = "http://127.0.0.1:8000/words.json"

var currentWord = document.getElementById("currentWord");
var rightOrWrong = document.getElementById("rightOrWrong");
var nextButton = document.getElementById("checkWord");
var answerInput = document.getElementById("answerInput");

var usedWords = [];

function getJSON(path, callback){
	var http_request = new XMLHttpRequest();
	http_request.onreadystatechange = function(){
		if (http_request.readyState == 4){
			if (http_request.status === 200) {
                var data = JSON.parse(http_request.responseText);
                if (callback) callback(data);
            }
		}
	};
	http_request.open("GET", path, true);
	http_request.send();
}

nextButton.onclick = function(){
	getJSON(data_file, function(data){
		if(checkWord(data))
		getWord(data);
		else return false;
	});
}

function getWord(data){
	while(true){
		var randomWord = Math.floor(Math.random() * data.words.length);
		if (usedWords.indexOf(randomWord) > -1){
			if (usedWords.length == data.words.length) {
				listFinished();
				return true
			}
		}
		else {
			usedWords.push(randomWord);
			break;
		}
	}

	console.log(usedWords);
	currentWord.innerHTML = data.words[randomWord].languageOne;
}

function checkWord(data){
	var lastWord = data.words[usedWords[usedWords.length-1]];
	console.log(answerInput.input);
	console.log(lastWord.languageTwo);
	if (answerInput.value == lastWord.languageTwo){
		rightOrWrong.innerHTML = "Goed!";
		answerInput.value = "";
		return true;
	}
	else {
		rightOrWrong.innerHTML = "Fout!";
		return false;
	}
}

function listFinished(){
	console.log('finished');
	currentWord.innerHTML = "Done!";
	return false;
}

getJSON(data_file, function(data){
	getWord(data);
});
