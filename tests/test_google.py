from selenium import webdriver

driver = webdriver.Safari()
driver.get("https://www.google.com")
print(driver.title)
driver.quit()