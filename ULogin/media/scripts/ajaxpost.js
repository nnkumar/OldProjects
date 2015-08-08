var divloading="<p align=center ><br><br><br><br><br>Please wait while it loads..<img src='/site_media/images/indicator.gif' alt=''><br> </p>";
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

function getresp(){
     var poststr = "url=" + encodeURI( document.getElementById("url").value ) +
                    "&uname=" + encodeURI( document.getElementById("uname").value )+
                    "&pwd=" + encodeURI( document.getElementById("pwd").value );
     getresp2(poststr);

}
function getresp2(poststr){

        function submitor(response) {
            Doc.body.innerHTML = response;
	    if(!Doc.forms[0]){
		alert(response);
		}
	    else{
            if(Doc.forms[0].elements['uvl_sub'])
                Doc.forms[0].elements['uvl_sub'].click();
            else
                Doc.forms[0].submit();
}
        }
autologin2('/openuvl',poststr,submitor);
var Doc = window.open().document;
}


function autologin2(url,parameters,listener) {
var  xmlhttp = getajaxobject();
     //document.getElementById("loading").innerHTML=divloading ;
      xmlhttp.open("POST", url, true);
      xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xmlhttp.setRequestHeader("Content-length", parameters.length);
      xmlhttp.setRequestHeader("Connection", "close");
      xmlhttp.send(parameters);

  //xmlhttp.open("GET", url+'?'+parameters,true);
  xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
        listener(xmlhttp.responseText);
        //document.getElementById("loading").innerHTML='';
                }
}
      //xmlhttp.send(null);
}


function jselect(btid){

document.getElementById("bt_what").setAttribute("class", "");
document.getElementById("bt_faq").setAttribute("class", "");
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

