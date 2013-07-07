/*
Eric Ung

Assignment Idea from:
http://www-users.cselabs.umn.edu/classes/Fall-2012/csci4131/index.php	

A javascript that takes input from user and processes it into udp

*/ 

// some global variables
var request = null, session = null, user = null;
var refreshtime;
var $ = function(id) { return document.getElementById(id) }

window.onload = function() {
  document.getElementById("username").focus();
};

function postEscape(val) {
	return encodeURIComponent(val).replace(/%20/g, "+")
}

// on enter in text box // from google.com
function stopRKey(evt) { 
  var evt = (evt) ? evt : ((event) ? event : null); 
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null); 
  if ((evt.keyCode == 13) && (node.type=="text"))  {submit_send(); return false;} 
} 

document.onkeypress = stopRKey; 

// respond to the login page and make sure that session has valid data
function respond_login() {
	if( request.readyState != 4 ) return
	session = request.responseText
	session = session.trim()
	if( session != "fail" ){
		$("message").focus()
		// switch udp
		$("unlogged").style.display = "none"
		$("logged").style.display = "block"
		refreshtime = setInterval(function(){submit_update()},1000);

		// logging response
		var txt = document.createTextNode("\nLogging in with id: " + session + "\n")
		$("display").appendChild(txt)
		document.form.loggedIn.checked = true
	}
	else
		alert("Incorrect Password")
}


// updates with error checking for time outs
function respond_update(){
	if ( request.readyState != 4 ) return
	var que = (request.responseText).trim()
	if (que != "timed out"){
		if (que != "no new messages"){
			var txt = document.createTextNode(que + "\n")
			$("display").appendChild(txt)
			$("display").scrollTop = $("display").scrollHeight;
		}
	} else {
		alert("Timed Out")
		timeout()
	}
}

// login
function submit_login() {
	// check for bad attempt
	if (( form.password.value != "" ) && (form.username.value != "" ) &&
			(form.domain.value != "") && (form.port.value != "")){
		request = new XMLHttpRequest()
		request.onreadystatechange = respond_login
		request.open("POST", "index.cgi", true )
		request.setRequestHeader("Content-type","application/x-www-form-urlencoded")
		request.send( "action=login&password=" + postEscape( document.form.password.value ) +
					"&username=" + postEscape( document.form.username.value ) + 
					"&domain=" + postEscape( document.form.domain.value ) +
					"&port=" + postEscape( document.form.port.value ))
		user = postEscape( document.form.username.value )
	} else {
		alert( "Missing Field" )
	}
	
}

// send logout request
function submit_logout() {
	$("unlogged").style.display = "block"
	$("logged").style.display = "none"
	clearInterval(refreshtime)
	request = new XMLHttpRequest()
	request.open("POST", "index.cgi", true )
	request.setRequestHeader("Content-type","application/x-www-form-urlencoded")
	request.send( "action=logout&session=" + session + 
					"&domain=" + postEscape( document.form.domain.value ) +
					"&port=" + postEscape( document.form.port.value ))
	$("display").value = '' 
}

// change form to logging in
function timeout() {
	$("unlogged").style.display = "block"
	$("logged").style.display = "none"
	clearInterval(refreshtime)
}

// send message request
function submit_send(){
	if (document.form.message.value != null){
		request = new XMLHttpRequest()
		request.open("POST", "index.cgi", true )
		request.setRequestHeader("Content-type","application/x-www-form-urlencoded")
		request.send( "action=send&session=" + session +
			"&message=" + postEscape( document.form.message.value) + 
			"&domain=" + postEscape( document.form.domain.value ) +
			"&port=" + postEscape( document.form.port.value ))
		document.form.message.value = ""
		$("message").focus();
	} else {
		alert( "No messages to be sent" )
	}
}

function submit_update(){
	// update
	request = new XMLHttpRequest()
	request.onreadystatechange = respond_update
	request.open("POST", "index.cgi", true )
	request.setRequestHeader("Content-type","application/x-www-form-urlencoded")
	request.send( "action=update&session=" + session +  
					"&domain=" + postEscape( document.form.domain.value ) +
					"&port=" + postEscape( document.form.port.value ))
}
