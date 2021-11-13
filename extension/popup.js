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


            var publicKey = forge.pki.publicKeyFromPem('../public_key.pem');
            var pass_encrypted = publicKey.encrypt(password, "RSA-OAEP", {
                md: forge.md.sha256.create(),
                mgf1: forge.mgf1.create()
            });
            var pass_base64 = forge.util.encode64(pass_encrypted);


            var xhr = new XMLHttpRequest();
            var url = "127.0.0.1:5000/test?username=" + username + "&phone_number=" + phonenumber + "&password=" + pass_base64;
            console.log(url);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    
                }
            }
            xhr.open("GET", url, true);
            xhr.send();
        });


        
    }
});