$.fn.ajaxSubmit = function(e) {
	/* Change a form's submission type to ajax */
	this.submit(function(){
		var params = {};
		$(this)
		.find("input[@checked], input[@type='text'], input[@type='hidden'], input[@type='password'], input[@type='submit'], option[@selected], textarea")
		.filter(":enabled")
		.each(function() {
			params[ this.name || this.id || this.parentNode.name || this.parentNode.id ] = this.value;
		});
		$("body").addClass("curWait");
		
		$.post(this.getAttribute("action") + "?call=ajax", params, function(xml){
			$("body").removeClass("curWait");
			strError = "Unable to submit form. Please try again later.";
			oFocus = null;
			$("AjaxResponse", xml).each(function() {
				strRedirect = this.getAttribute("redirecturl");
				strError = this.getAttribute("error");
				oFocus = this.getAttribute("focus");
			});
			if (strError.length == 0) {
				window.location = strRedirect;
			} else {
				alert("The following errors were encountered:\n" + strError);
				$("div.formErrors").html("<h3>Error<\/h3><ul>" + strError.replace(/(\t)(.+)/g, "<li>$2<\/li>") + "<\/ul>").filter(":hidden").fadeIn("normal");
				if (oFocus) $("#" + oFocus).get(0).focus();
			}
		});
		return false;
	});
	
	return this;
}
