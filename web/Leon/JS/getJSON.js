var data_file = "http://127.0.0.1:8000/words.json"

function getJSON(path, callback){
	var http_request = new XMLHttpRequest();
	http_request.onreadystatechange = function(){
		if (http_request.readyState == 4){
			if (http_request.status === 200) {
                var data = JSON.parse(http_request.responseText);
				listTitle.innerHTML = data.listName;
                if (callback) callback(data);
            }
		}
	};
	http_request.open("GET", path, true);
	http_request.send();
}

getJSON(data_file, function(data){
});

