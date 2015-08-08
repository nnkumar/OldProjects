import urllib2, urllib

def checkcaptcha (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """
    API_SSL_SERVER="https://api-secure.recaptcha.net"
    API_SERVER="http://api.recaptcha.net"
    VERIFY_SERVER="api-verify.recaptcha.net"

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return False 
    
    
    
    params = urllib.urlencode ({
	    'privatekey': private_key,
            'remoteip' : remoteip,
	    'challenge': recaptcha_challenge_field,
	    'response' : recaptcha_response_field,
	    })

    request = urllib2.Request (
        url = "http://%s/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return True
    else:
        return False

