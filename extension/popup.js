
//Create a script tag and add it to head (Forge is encryption)

// what the extension is supposed to do
document.addEventListener('DOMContentLoaded', function() {
    console.log("page loaded, in first event listener");

    // submit button
    var val = document.getElementById('submitbtn');
    if (val) {
        val.addEventListener('click', function(event) {
            event.preventDefault();
            var username = document.getElementById('username').value;
            var phonenumber = document.getElementById('phonenumber').value;
            var password = document.getElementById('password').value;
        
            console.log("submit button clicked")
            console.log(username);
            console.log(phonenumber);
            console.log(password);

             var publicKey = forge.pki.publicKeyFromPem('-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCP7+kpnhuL1yitNLZRZf3Ro8/oOpPbaNahK+LFVsLkOYxlzldsEgW/LjFKD1vMFP1JGxNgNdjWCCb0FCgJheop7CawsXZsBlPzK+4emTg+GhD7UR6BALR3Ki7jJ21bSojSbDNksh8aj8/KLTvtuBSDK+aG0NQZmvqHfuBwWfIErwIDAQAB-----END PUBLIC KEY-----');
             var pass_encrypted = publicKey.encrypt(password, "RSA-OAEP", {
                 md: forge.md.sha256.create(),
                 mgf1: forge.mgf1.create()
             });
             var pass_base64 = forge.util.encode64(pass_encrypted);
             console.log(pass_base64)
            var xhr = new XMLHttpRequest();
            var url = "http://127.0.0.1:5000/test?username=" + username + "&phone_number=" + phonenumber + "&password=" + pass_base64;
            console.log(url);
            xhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                }
            };
            xhr.open("GET", url, true);
            xhr.send(url);
        });


        
    }
});