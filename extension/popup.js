// what the extension is supposed to do

document.addEventListener('DOMContentLoaded', function() {

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://localhost/phpchrome.php", true);
    xhr.onreadystatechange = function() {

        if (xhr.readyState == 4) {
            varxhrjson = JSON.parse(xhr.responseText);
        }
    }
    xhr.send();
});

function onSubmitFunction() {
    console.log("we're in the onSubmit function!");
}