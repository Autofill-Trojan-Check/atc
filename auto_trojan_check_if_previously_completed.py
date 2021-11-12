# created by: nicolas lee; nicolasmatthewlee@gmail.com; 2021
#!/usr/bin/env python
# coding: utf-8

# In[1]:

username=input('Username: ')
password=input('Password: ')
# specify absolute path to folder
savefileto=input('Save file to: ')

# #### Setup

# In[2]:


# requires selenium and webdriver_managers

# get webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# to access class names in webdriver.Chrome().find_elements()
from selenium.webdriver.common.by import By

# for waiting for page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# get chrome service
s=Service(ChromeDriverManager().install())

# create instance of webdriver
driver=webdriver.Chrome(service=s)

driver.set_window_size(500,700)


# #### Login

# In[3]:


# navigate to page given by url and wait until the page is loaded
# before returning to your script
driver.get('https://trojancheck.usc.edu/login')

# find and click login button
# CSS SELECTOR found at class= and then add '.' before each
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-login.mat-flat-button.mat-button-base').click()

# must wait for elements to be loaded before can look for them
# timeout specifies max time to wait
# use // to specify non-absoluate location
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,'//input[@id="username"]')))
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,'//input[@id="password"]')))
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,'//button')))
# enter username and password
driver.find_element(By.XPATH,'//input[@id="username"]').send_keys(username)
driver.find_element(By.XPATH,'//input[@id="password"]').send_keys(password)

# submit
driver.find_element(By.XPATH,'//button').click()


# #### Consent

# In[4]:


# wait until button found
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent')))

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent').click()


# #### Forms

# #### Save Image

# In[5]:


# wait until image loads
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,'day-pass-qr-code')))

# get day-pass element
qr_element=driver.find_element(By.CLASS_NAME,'day-pass')

# scroll to put QR code in view
driver.execute_script('arguments[0].scrollIntoView();',(qr_element))

# screenshot
driver.save_screenshot(savefileto+'/trojan_check.png')

print('trojan_check.png saved to '+savefileto+'/trojan_check.png')