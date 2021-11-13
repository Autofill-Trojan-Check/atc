// what the extension is supposed to do

document.addEventListener('DOMContentLoaded', function() {
    console.log("page loaded, in first event listener");

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
        
            // chrome.tabs.executeScript({
            //     code: `var value = $(username);`
            // }, function() {
            //     127.0.0.1:5000/
            // }
            //)
        });
    }
});