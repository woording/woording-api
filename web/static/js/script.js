var right = document.getElementById('right_content');

function checkWord(word){
	var input = document.getElementById('word_input').value;

	if(input == word.language_2_text){
		document.getElementById('word_input').value = '';
		document.getElementById('goed').innerHTML++;
	}

	else {
		document.getElementById('current_word').innerHTML = word.language_2_text;
		document.getElementById('fout').innerHTML++;
	}

	document.getElementById('word_input').value = '';
	angular.element(document.getElementById('main_controller')).scope().getRandomWord();
}

function showPractice() {
	var practice = document.getElementById('practice_div');
	var left = document.getElementById('left_content');
	var middle = document.getElementById('middle_content');

	var content = [left, middle, right];

	practice.style.display = 'block';

	for (item of content){
		item.style.display = 'none';
	}
}

function showList() {
	right.style.display = 'block';
}
