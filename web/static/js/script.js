var right = document.getElementById('right_content');
var practice = document.getElementById('practice_div');
var left = document.getElementById('left_content');
var middle = document.getElementById('middle_content');

var content = [left, middle, right];

document.addEventListener('keypress', function(event) {
	var activeElement;
	if (event.keyCode == 9) {
		activeElement = document.activeElement;
		if (activeElement.name == "edit_input") {
			if (activeElement.nextElementSibling == null
				&& activeElement.parentElement.nextElementSibling == null
				&& activeElement.parentElement.parentElement.nextElementSibling == null) {
				event.preventDefault();
				// Add row
				addRow();
				// Focus on next element
				activeElement.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild.focus();
			}
		}
	}
}, false);

function setResult(total, wrong){
	var correct = document.getElementById('correct_bar');
	var incorrect = document.getElementById('incorrect_bar');
	if (!wrong){
		incorrect.innerHTML = '0%';
		incorrect.style.width = '0%';
		correct.style.width = (100 - (wrong/total * 100) - 2) + '%';
		correct.innerHTML = Math.round((100 - (wrong/total * 100))) + '%';
	}

	else {
		incorrect.style.width = ((wrong/total * 100) - 1) + '%';
		incorrect.innerHTML = Math.round((wrong/total * 100)) + '%';
		correct.style.width = (100 - (wrong/total * 100) - 1) + '%';
		correct.innerHTML = Math.round((100 - (wrong/total * 100))) + '%';
	}
}

function showEditor() {
	right.style.display = 'block';
	document.getElementById('edit_list').style.display = 'block';
	document.getElementById('results').style.display = 'none';
	document.getElementById('list_items').style.display = 'none';
}

function addRow() {
	var table = document.getElementById('edit_list_table');

	var newRow = table.insertRow();
	var newCell = newRow.insertCell();
	newCell.innerHTML = '<input type="text" placeholder="Sentence" name="edit_input">';
	newCell = newRow.insertCell();
	newCell.innerHTML = '<input type="text" placeholder="Translation" name="edit_input">';

}

function showResults() {
	practice.style.display = 'none';
	document.getElementById('correct').innerHTML = 0;
	document.getElementById('incorrect').innerHTML = 0;

	for (item of content){
		item.style.display = 'block';
	}

	document.getElementById('list_items').style.display = 'none';
	document.getElementById('results').style.display = 'block';
}


function showPractice() {
	practice.style.display = 'block';

	for (item of content){
		item.style.display = 'none';
	}
}

function showList() {
	right.style.display = 'block';
	document.getElementById('edit_list').style.display = 'none';
	document.getElementById('results').style.display = 'none';
	document.getElementById('list_items').style.display = 'block';
}

