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