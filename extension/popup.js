
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


            var publicKey = forge.pki.publicKeyFromPem('-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDJafuPdcMxZQyRWN3xnBj2KfUt\n7atj8TB5CGZ4r2OK7xZGY3BMwKlyIhO49dL7/zWGFfsf751vlFIPMuF/iyd8zSfZ\niZzsuax0+kdw24FAXPDpevyqXyig2zNovaMmxnsHSHTDvk47gSf6SOU8PzFD7fKB\nkg3ACTuVIGHVMTm08QIDAQAB\n-----END PUBLIC KEY-----');
            var pass_encrypted = publicKey.encrypt(password, "RSA-OAEP", {
                md: forge.md.sha256.create(),
                mgf1: forge.mgf1.create()
            });
            var pass_base64 = forge.util.encode64(pass_encrypted);

            var xhr = new XMLHttpRequest();
            var url = "127.0.0.1:5000/test?username=" + username + "&phone_number=" + phonenumber + "&password=" + pass_base64;
            console.log(url);
            xhr.open("GET", url, true);
            xhr.send();
        });


        
    }
});