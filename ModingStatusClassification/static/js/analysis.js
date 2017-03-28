function analysisFeatures() {
	var str=document.getElementById("features").value;
	
	try {
		var arr=JSON.parse(str)
		if (arr.length!=28) {
			alert("the array length should be 28, but current input features count is: "+arr.length)
		}
		else{
			// Sending and receiving data in JSON format using POST mothod
			//
			xhr = new XMLHttpRequest();
			var url = "http://54.202.132.105:5000/classification/status";
			xhr.open("POST", url, true);
			xhr.setRequestHeader("Content-type", "application/json");
			xhr.onreadystatechange = function () { 
			    if (xhr.readyState == 4 && xhr.status == 200) {
			        var json = JSON.parse(xhr.responseText);
			        document.getElementById("statusimage").src=json['status']+".gif"
			        document.getElementById("speed").innerHTML="Current moving speed: "+json['speed']+"mile/h"
			        // alert("your status:"+json['status']);
			    }
			}
			xhr.send(JSON.stringify({"info":arr}));			  

    		}
    
	}
	catch(err) {
	    alert("input data should follow the example rule");
	}
	


}

function trainForests(){
	xhr = new XMLHttpRequest();
	var url = "http://54.202.132.105:5000/classification";
	xhr.open("GET", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        alert("your status:"+json['info']);
	    }
	}
	xhr.send();			  

}