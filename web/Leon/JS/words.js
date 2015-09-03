var usedWords = [];

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

	currentWord.innerHTML = data.words[randomWord].languageOne;
}

function checkWord(data){
	var lastWord = data.words[usedWords[usedWords.length-1]];
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
	currentWord.innerHTML = "Done!";
	return false;
}

getJSON(data_file, function(data){
	getWord(data);
});
