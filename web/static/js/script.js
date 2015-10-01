var right = document.getElementById('right_content');
var practice = document.getElementById('practice_div');
var left = document.getElementById('left_content');
var middle = document.getElementById('middle_content');
var flipped = false;

var content = [left, middle, right];

flip_button = function(){
	if(!flipped){
		document.getElementById('flipper').style.transform = "rotateY(180deg)";
		document.getElementById('flipper').style.webkitTransform = "rotateY(180deg)";
		flipped = true;
	} else {
		document.getElementById('flipper').style.transform = "rotateY(0deg)";
		document.getElementById('flipper').style.webkitTransform = "rotateY(0deg)";
		flipped = false;
	}
};

document.addEventListener('keydown', function(event) {
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
				window.setTimeout(function() {
					activeElement.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild.focus();
				}, 100);
			}
		}
	}
}, false);

function setResult(total, wrong){
	var correct = document.getElementById('correct_bar');
	var incorrect = document.getElementById('incorrect_bar');
	if (!wrong){
		incorrect.style.display = 'none';
		correct.style.width = Math.round(100 - (wrong/total * 100)) + '%';
		correct.innerHTML = Math.round((100 - (wrong/total * 100))) + '%';
	}

	else {
		incorrect.style.display = 'inline-block';
		incorrect.style.width = Math.round((wrong/total * 100) - 1) + '%';
		incorrect.innerHTML = Math.round((wrong/total * 100)) + '%';
		correct.style.width = Math.round(100 - (wrong/total * 100) - 1) + '%';
		correct.innerHTML = Math.round((100 - (wrong/total * 100))) + '%';
	}
}

function showEditor() {
	right.style.display = 'inline-block';
	document.getElementById('edit_list').style.display = 'block';
	document.getElementById('results').style.display = 'none';
	document.getElementById('list_items').style.display = 'none';
}

function addRow() {
	var main_controller = document.getElementById('main_controller');
	var scope = angular.element(main_controller).scope();
	var size = scope.sizeOf(scope.editData.words);

	scope.editData.words[size] = {
		language_1_text: "",
		language_2_text: ""
	};
}

function showResults() {
	var top = 4;

	function slideDown(){
		if (top == 100){
			practice.style.display = 'none';
			return true;
		}

		practice.style.top = top + '%';
		top += 2;
		requestAnimationFrame(slideDown);
	}

	slideDown();

	document.getElementById('correct').innerHTML = 0;
	document.getElementById('incorrect').innerHTML = 0;

	document.getElementById('overlay').style.display = 'none';

	for (item of content){
		item.style.display = 'inline-block';
	}

	document.getElementById('list_items').style.display = 'none';
	document.getElementById('results').style.display = 'block';
}


function showPractice() {
	practice.style.display = 'block';
	document.getElementById('overlay').style.display = 'block';
	var top = 100;

	function slideUp(){
		if (top == 4){
			return true;
		}

		practice.style.top = top + '%';
		top -= 2;
		requestAnimationFrame(slideUp);
	}

	slideUp();
}

function showList() {
	right.style.display = 'inline-block';
	document.getElementById('edit_list').style.display = 'none';
	document.getElementById('results').style.display = 'none';
	document.getElementById('list_items').style.display = 'block';
}
