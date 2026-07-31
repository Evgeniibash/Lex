import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_qa_sandbox():
    # 1. Открываем браузер и сайт
    driver = webdriver.Chrome()
    driver.get("http://localhost:8080")
    
    # 2. Ждем появления заголовка H1 на странице (ждем максимум 10 секунд)
    wait = WebDriverWait(driver, 10)
    h1_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    
    # 3. Проверяем, что текст в H1 совпадает с ожидаемым
    assert h1_element.text == "QA Practice Sandbox"
    print("✅ Страница загружена, заголовок H1 найден!")
    
    # 4. Проверяем, что кнопка "Войти" заблокирована
    login_btn = driver.find_element(By.ID, "login-btn")
    assert login_btn.get_attribute("disabled") is not None
    print("✅ Кнопка заблокирована — ок")
    
    # 5. Вводим неверный логин и пароль
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("123")
    login_btn.click()
    
    # 6. Проверяем, что появилась ошибка
    error = driver.find_element(By.ID, "login-error")
    assert error.is_displayed()
    print("✅ Ошибка появилась — ок")
    
    # 7. Вводим правильные данные
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("admin123")
    login_btn.click()
    
    # 8. Проверяем, что появился успех
    success = driver.find_element(By.ID, "login-success")
    assert success.is_displayed()
    print("✅ Успешный вход — ок")
    
    # 9. Добавляем новую задачу
    todo_input = driver.find_element(By.ID, "todo-input")
    todo_input.send_keys("Купить хлеб")
    driver.find_element(By.ID, "add-todo-btn").click()
    
    # 10. Проверяем, что задач стало 3
    todo_items = driver.find_elements(By.CSS_SELECTOR, "#todo-list li")
    assert len(todo_items) == 3
    print("✅ Задача добавилась — ок")
    
    # 11. Закрываем браузер
    driver.quit()
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")