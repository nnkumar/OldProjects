function putstatus(text){
  document.getElementById("status").style.visibility="visible";
        document.getElementById("status").style.color="red";
        document.getElementById("status").innerHTML=text;
}


var divloading="<p align=center ><br><br><br><br><br>Please wait while it loads..<img src='/site_media/images/indicator.gif' alt=''><br> </p>";

function showloading(){
  document.getElementById("status").style.visibility="hidden";
document.getElementById("loading").innerHTML=divloading ; 
}

function getajaxobject(){
	var ajaxRequest;
	try{
		// Opera 8.0+, Firefox, Safari
		ajaxRequest = new XMLHttpRequest();
	} catch (e){
		// Internet Explorer
		try{
			ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e) {
			try{
				ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (e){
				alert("Some browser problem!");
				return false;
			}
		}
	}
	return ajaxRequest;
}

function ajax_recv(){
	var xmlhttp = getajaxobject();
	var pwd = document.getElementById("pwd").value;
        var email = document.getElementById("email").value;
	if(email.length==0 || pwd.length==0) 
		{putstatus("Both fields should be filled"); return false;}
	showloading();
	var link="/mailrecv/"+"?pwd="+pwd+"&email="+email+"&Submit=Update+";
 	xmlhttp.open("GET",link ,true);
 	xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
                if(xmlhttp.responseText=="Error")
			putstatus("Wrong password");
		document.getElementById("loading").innerHTML='';
		if(xmlhttp.responseText=="Send")
			document.getElementById("uid_main").innerHTML="<br><br><br>Key needed for 	recovery has been send to your email ID. Click on Home to go back"
			//putstatus("Key needed for recovery has been send to your email ID");
			//ajax_fetch('/sites/');
}
}

      xmlhttp.send(null);
      return false;
}





function pass_validate(){
	var xmlhttp = getajaxobject();
	var oldpw = document.getElementById("oldpw").value;
        var pwd= document.getElementById("pw").value;
	var pwd2= document.getElementById("confirm").value;
        if (pwd.length< 6)
                {putstatus("password should be minimum 6"); return false;}
        if (pwd!=pwd2)
                {putstatus("passwords dont match");return false;}
	showloading();
	var link="/setpass/"+"?oldpw="+oldpw+"&pw="+pwd+"&Submit=Update+";
 	xmlhttp.open("GET",link ,true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
                if(xmlhttp.responseText=="Erpass")
			{putstatus("Wrong password");
			document.getElementById("loading").innerHTML='' ;}
		else
			ajax_fetch('/sites/');
}
}

      xmlhttp.send(null);
      return false;
}



//new code

function ajax_signin(id){
        function submitor(response) {
            Doc.body.innerHTML = response;
            if(Doc.forms[0].elements['uvl_sub'])
	        Doc.forms[0].elements['uvl_sub'].click();
	    else
		Doc.forms[0].submit();
        }
autologin(id,submitor);
var Doc = window.open().document;
}




function autologin(id,listener) {
var xmlhttp = getajaxobject();
     //document.getElementById("loading").innerHTML=divloading ;
  xmlhttp.open("GET", 'ulogin/' +id+'/',true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
	listener(xmlhttp.responseText);
	//document.getElementById("loading").innerHTML='';
                }
}
      xmlhttp.send(null);
}






function ajax_del(id){
if (!confirm("Do you want to delete?"))
	return false;
document.getElementById("loading").innerHTML=divloading ;
var xmlhttp = new XMLHttpRequest();
 xmlhttp.open("GET", 'sdel/' +id+'/',true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
		document.getElementById(id).innerHTML='';
		document.getElementById("loading").innerHTML='';
}}

      xmlhttp.send(null);
      return false;
}


function jselect(btid){

document.getElementById("bt_sites").setAttribute("class", "");
document.getElementById("bt_addsite").setAttribute("class", "");
document.getElementById("bt_set").setAttribute("class", "");
document.getElementById("bt_dmail").setAttribute("class", "");
document.getElementById(btid).setAttribute("class", "selected");

}

function ajax_fetch(link,btid){
                document.getElementById("uid_main").innerHTML=divloading ;
var xmlhttp = getajaxobject();
 xmlhttp.open("GET", link ,true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
                document.getElementById("uid_main").innerHTML=xmlhttp.responseText ;
}}

      xmlhttp.send(null);
      return false;
} 

