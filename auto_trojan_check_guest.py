#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# specify absolute path to folder
savefileto=input('Save file to: ')


# #### Setup

# In[1]:


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


# #### Continue as guest

# In[2]:


driver.get('https://trojancheck.usc.edu/login')

WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-focus-indicator.btn-login.mat-flat-button.mat-button-base')))

driver.find_elements(By.CSS_SELECTOR,'.mat-focus-indicator.btn-login.mat-flat-button.mat-button-base')[1].click()


# #### Consent

# In[3]:


# wait until button found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent')))

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent').click()


# #### Start screening

# In[4]:


# wait until button is found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-wrapper')))

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-assessment-start.mat-flat-button.mat-button-base').click()


# #### Are you fully vaccinated?

# In[5]:


# wait until button is found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

# select YES
driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[1].click()

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


# #### Do any of these apply to you?

# In[6]:


# wait until button is found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

# select NO
driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[1].click()
driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[3].click()

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


# #### Do any of these apply to you?

# In[7]:


# wait until button is found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

# select NO
driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[1].click()
driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[3].click()

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


# #### Do you currently have any of the following symptoms?

# In[8]:


# wait until button is found
WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

# select NO for all symptoms
for i in list(range(0,7)):
    driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[i*2+1].click()
    
# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


# #### Your responses

# In[9]:


# wait until checkbox is found
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-checkbox-inner-container')))

# check box
driver.find_element(By.CSS_SELECTOR,'.mat-checkbox-inner-container').click()

# submit
driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-submit.mat-flat-button.mat-button-base').click()


# #### Visitor access form

# In[10]:


# fill out form
data=['firstname','lastname','1234567890','visitor@website.com','contact','1234567890','contact@website.com','location']

driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-invalid').send_keys(data[0])
driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-invalid').send_keys(data[1])

driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-valid').send_keys(data[2])
driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-invalid').send_keys(data[3])

driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-valid').send_keys(data[4])
driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-valid').send_keys(data[5])

driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-valid').send_keys(data[6])
driver.find_element(By.CSS_SELECTOR,'.k-textbox.ng-untouched.ng-pristine.ng-invalid').send_keys(data[7])

driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.mat-flat-button.mat-button-base').click()


# #### Save image

# In[ ]:


# wait until image loads
WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,'day-pass-qr-code')))

# get day-pass element
qr_element=driver.find_element(By.CLASS_NAME,'day-pass')

# scroll to put QR code in view
driver.execute_script('arguments[0].scrollIntoView();',(qr_element))

# screenshot
driver.save_screenshot(savefileto+'/trojan_check.png')

print('trojan_check.png saved to '+savefileto+'/trojan_check.png')

driver.quit()

