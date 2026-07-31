from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://dzen.ru/?yredirect=true"


driver = webdriver.Safari()
wait = WebDriverWait(driver, 15)


print("Открываем Дзен...")
driver.get(url)


wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("Страница загружена!")


search_input = wait.until(EC.visibility_of_element_located((By.NAME, "text")))
print("Поле поиска найдено!")


search_input.clear()
search_input.send_keys("selenium")
search_input.send_keys(Keys.ENTER)
print("Текст введён, Enter нажат!")


time.sleep(10)


driver.quit()
