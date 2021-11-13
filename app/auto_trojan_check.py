# created by: Nicolas Lee 2021

def get_trojan_check(username,password,savefileto):

    # #### Setup
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

    import os

    # get chrome service
    s=Service(ChromeDriverManager().install())

    # create instance of webdriver
    driver=webdriver.Chrome(service=s)

    driver.set_window_size(500,700)


    # #### Login

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
        
    # check if login successful
    # look until "Before you Begin" OR ".form-element.form-error" found
    while(1):
        try:
            header=driver.find_element(By.XPATH,'//h1[text()="Before you begin"]')
            print('header',header)
            break
        except:
            pass
        try:
            error=driver.find_element(By.CSS_SELECTOR,'.form-element.form-error')
            print('error',error)
            print('Login failed.')
            driver.quit()
            return 1
        except:
            pass


    # #### Consent

    # wait until button found
    WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent')))

    # submit
    driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent').click()


    # check if previously completed or not
    # look until image found or button found
    prev_completed=False

    # potential errors from below code potentially because the button defined by its CSS_SELECTOR
    # may be present in both forms
    while(1):
        try:
            # previously completed
            image=driver.find_element(By.CLASS_NAME,'day-pass')
            prev_completed=True
            break
        except:
            pass
        try:
            # not previously completed
            button=driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.mat-flat-button.mat-button-base.btn-begin-assessment')
            prev_completed=False
            break
        except:
            pass
        
    if (not prev_completed):
        # wait until button is clickable
        WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-wrapper')))

        # submit
        driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.mat-flat-button.mat-button-base.btn-begin-assessment').click()


        # #### Start screening

        # wait until button is clickable
        WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-wrapper')))

        # submit
        driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-assessment-start.mat-flat-button.mat-button-base').click()


        # #### Do any of these apply to you?

        # wait until button is clickable
        WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

        # select NO
        driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[1].click()
        driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[3].click()

        # submit
        driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


        # #### Do you currently have any of these symptoms?

        # wait until button is found
        WebDriverWait(driver,timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')))

        # select NO for all symptoms
        for i in list(range(0,7)):
            driver.find_elements(By.CSS_SELECTOR,'.mat-button-toggle-button.mat-focus-indicator')[i*2+1].click()
            
        # submit
        driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-next.mat-flat-button.mat-button-base').click()


        # #### Your responses

        # wait until checkbox is found
        WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.mat-checkbox-inner-container')))

        # check box
        driver.find_element(By.CSS_SELECTOR,'.mat-checkbox-inner-container').click()

        # submit
        driver.find_element(By.CSS_SELECTOR,'.mat-focus-indicator.btn-submit.mat-flat-button.mat-button-base').click()


    # #### Save Image

    # wait until image loads
    WebDriverWait(driver,timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,'day-pass-qr-code')))

    # get day-pass element
    qr_element=driver.find_element(By.CLASS_NAME,'day-pass')

    # scroll to put QR code in view
    driver.execute_script('arguments[0].scrollIntoView();',(qr_element))

    # save screenshot
    driver.save_screenshot(os.path.join(savefileto,'trojancheck.png'))

    driver.quit()

    return 0

if __name__=='__main__':
    # specify absolute path to folder
    username=input('Username: ')
    password=input('Password: ')
    savefileto=input('Save to: ')
    get_trojan_check(username,password,savefileto)