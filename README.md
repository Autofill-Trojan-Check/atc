# Autofill Trojan Check
## Team Members
Ariana Goldstein, Kesha Srivatsan, Moses Lee, Netanel Sadeghi, and Nicolas Lee

## Overview
Our Autofill Trojan Check is structured as a Chrome extension that runs a Flask application, `app.py`. It prompts the user for input-- username, phone number, and password-- for Trojan Check with an HTML form. It then calls function declared in `auto_trojan_check.py` to create a Chrome webdriver and navigate the form, returning either that the login failed or a page containing the QR code image. 

## Setup
Create a new Chrome extension with the files in the `atc/extension/` directory. Do this by visiting the URL <chrome://extensions/>, switching 'developer mode' on, and clicking the 'load unpacked' button. Then, navigate to the `atc/extension/` directory and click 'select.' This will load the extension onto your browser, and you can pin it so that it is always visible on your extension toolbar.

Check `requirements.txt` for the libraries and corresponding versions you need to install before running.

## To Execute
In the `atc/app/` directory, in the terminal, run the following command.
```
flask run
```
Then, open up Chrome and open the extension by clicking on the icon. Enter your username, phone number, and password and click 'submit.' This should open a new window that automatically logs into the USC login page with the given credentials and automatically fills out the form. At the end, it should display the successful screenshot and send a text message of it to the specified phone number.