# Autofill Trojan Check
## Team Members
Aditya Hariharan, Ariana Goldstein, Fil Graniczny, Kesha Srivatsan, Moses Lee, Netanel Sadeghi, Nicolas Lee, Ryan Lee, Sohee Yoon, Will Buckser-Schulz

## Overview
Structured as a flask application app.py that takes in user input (username, password) for TrojanCheck with an html form. Then calls function declared in auto_trojan_check.py to create a chrome webdriver and navigate the form either returning that login failed or a page containing the QR code image. 

Needs to be re-tested on trojan checks where not previously completed. 
