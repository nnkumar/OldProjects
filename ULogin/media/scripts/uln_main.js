var divloading="<p align=center ><br><br><br><br><br>Please wait while it loads..<img src='/site_media/images/indicator.gif' alt=''><br> </p>";

function showloading(){
  document.getElementById("status").style.visibility="hidden";
document.getElementById("login_main").innerHTML=divloading ; 
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


function putstatus(text){
  document.getElementById("status").style.visibility="visible";
        document.getElementById("status").style.color="red";
        document.getElementById("status").innerHTML=text;
}

function jselect(btid){

document.getElementById("bt_what").setAttribute("class", "");
document.getElementById("bt_faq").setAttribute("class", "");
document.getElementById("bt_dmail").setAttribute("class", "");
document.getElementById(btid).setAttribute("class", "selected");

}

function ajax_accrecv(){
	var xmlhttp = getajaxobject();
	var uname = document.getElementById("uname").value;
        var rkey = document.getElementById("rkey").value;
	if(uname.length==0 || rkey.length==0) 
		{putstatus("Both fields should be filled"); return false;}
	var link="/accrecv/"+"?uname="+uname+"&rkey="+rkey+"&Submit=Update+";
 	xmlhttp.open("GET",link ,true);
 	xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
                if(xmlhttp.responseText=="Error")
			putstatus("Wrong key or username");
		if(xmlhttp.responseText=="Send")
			document.getElementById("login_main").innerHTML="<br><br><br>Your password have been sent to your email address. Please login using it."
			
}
}
     xmlhttp.send(null);
     return false; 
}

function sl2valid(uname,pin)
{

	if(uname==""||pin==""){
		putstatus("Enter a valid username or pin");
		return false
	}
	return true;

}

function ajax_sl2(){
	//putstatus("");
	uname=document.getElementById("usrname").value;
	pin = document.getElementById("pin").value;
	keyset = document.getElementById("keyset").value;
	if(!(sl2valid(uname,pin)))
		return false;
	showloading();

  var xmlhttp = new getajaxobject();
       xmlhttp.open("GET", 'sl2login/?uname='+uname+'&pin='+pin+'&keyset='+keyset+'&Submit=Login' ,true);
     xmlhttp.onreadystatechange=function() {                               if (xmlhttp.readyState==4) { 
     if(xmlhttp.responseText=="NOK"){
		document.getElementById("loading").innerHTML='';
                document.getElementById("status").innerHTML="Incorrect username or pin";
                document.getElementById("status").style.visibility="visible";
		return false;
				    }
	else{
		document.getElementById("sl2form").submit();
		document.close();
	    }
    }
}
      xmlhttp.send(null);
     return false; 
}








function checkname(name){

if((name.substring(0,1)<"a" || name.substring(0,1)>"z") && (name.substring(0,1)<"A" || name.substring(0,1)>"Z"))
{
putstatus("The Username should begin with an alphabetic character.");	return false;
}

name_re  = new RegExp("^[a-zA-Z][a-zA-Z_0-9]+$","g");
        if (!name.match(name_re))
                {putstatus("Name should contain only letters,digits and underscore");return false; }
 return true;
}


function validate(){
	var name=document.getElementById("uname").value      
  	var pwd=document.getElementById("pwd").value      
	var pwd2=document.getElementById("pwd2").value      
	//if (!(checkname(name))) return false;
	//if(!(ajax_check(true))) return false;
        if (pwd.length<6)
                {putstatus("password should be minimum 6");return false;}
        if(pwd!=pwd2)
                {putstatus("passwords dont match");return false;}
        return true;
}





function ajax_check(sub){                
  var un=document.getElementById("uname").value      
      if (!(checkname(un))) return false;
  showloading();
  var xmlhttp = new getajaxobject(); 
       xmlhttp.open("GET", 'validate/'+un+'/' ,true);   
     xmlhttp.onreadystatechange=function() {                               if (xmlhttp.readyState==4) {                                         //alert(xmlhttp.responseText);
document.getElementById("loading").innerHTML='';
	if(xmlhttp.responseText=="avail"){
                document.getElementById("status").innerHTML="Congrats Username available";
                document.getElementById("status").style.color="green";}
	else{ sub=false;
                document.getElementById("status").innerHTML=xmlhttp.responseText;
                document.getElementById("status").style.color="red";}
                document.getElementById("status").style.visibility="visible";
}}

      xmlhttp.send(null);
      return sub;
}

function register(){
	if (validate()==false)
		return false;
//	 ajax_check(false);
//if (document.getElementById("status").style.color=="green")
//	return true;
//else
	return true;
}
function ajax_fetch(link){
//document.getElementById("login_main").innerHTML=divloading;
showloading();
var xmlhttp = new getajaxobject();
 xmlhttp.open("GET", link ,true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
                document.getElementById("login_main").innerHTML=xmlhttp.responseText ;
}}

      xmlhttp.send(null);
      return false;
}




function showloading2(){
document.getElementById("login_main").innerHTML='<p align=center style="visibility: visible;" id=preloading_uvl class=preloading />';

}

 
//function showloading(){
