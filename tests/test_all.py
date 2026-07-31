import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Импорты страниц (без них ничего не работает)
from pages.login_page import LoginPage
from pages.todo_page import TodoPage


# ============================================================
# 1. ТЕСТЫ ДЛЯ ЛОГИНА
# ============================================================

def test_login_button_disabled_initially(driver):
    page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_btn = driver.find_element(*page.LOGIN_BTN)
    assert login_btn.get_attribute("disabled") is not None
    print("✅ 1. Кнопка 'Войти' изначально недоступна")


def test_login_button_enabled_after_fill(driver):
    page = LoginPage(driver)
    driver.get("http://localhost:8080")
    page.type(page.USERNAME_INPUT, "adm")
    page.type(page.PASSWORD_INPUT, "any_password")
    login_btn = driver.find_element(*page.LOGIN_BTN)
    assert login_btn.get_attribute("disabled") is None
    print("✅ 2. Кнопка стала активной")


def test_login_invalid_credentials(driver):
    page = LoginPage(driver)
    driver.get("http://localhost:8080")
    page.login("adm", "wrong_password")
    assert page.is_error_visible()
    print("✅ 3. Ошибка при неверных данных")


def test_login_valid_credentials(driver):
    page = LoginPage(driver)
    driver.get("http://localhost:8080")
    page.login("admin", "admin123")
    assert page.is_success_visible()
    print("✅ 4. Успех при правильных данных")


# ============================================================
# 2. ТЕСТЫ ДЛЯ ЗАДАЧ
# ============================================================

def test_add_todo_task(driver):
    login_page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_page.login("admin", "admin123")
    
    todo_page = TodoPage(driver)
    initial_count = todo_page.get_task_count()
    todo_page.add_task("Купить хлеб")
    
    assert todo_page.get_task_count() == initial_count + 1
    print("✅ 5. Задача добавлена")


def test_delete_todo_task(driver):
    login_page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_page.login("admin", "admin123")
    
    todo_page = TodoPage(driver)
    initial_count = todo_page.get_task_count()
    todo_page.add_task("Задача для удаления")
    assert todo_page.get_task_count() == initial_count + 1
    
    tasks = driver.find_elements(*todo_page.TODO_LIST)
    delete_btn = tasks[-1].find_element(By.CSS_SELECTOR, ".delete-btn")
    delete_btn.click()
    
    assert todo_page.get_task_count() == initial_count
    print("✅ 6. Задача удалена")


def test_add_task_with_spaces(driver):
    login_page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_page.login("admin", "admin123")
    
    todo_page = TodoPage(driver)
    initial_count = todo_page.get_task_count()
    todo_page.add_task("   ")
    
    assert todo_page.get_task_count() == initial_count
    print("✅ 7. Задача из пробелов НЕ добавилась")


def test_add_task_with_trimmed_spaces(driver):
    login_page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_page.login("admin", "admin123")
    
    todo_page = TodoPage(driver)
    initial_count = todo_page.get_task_count()
    todo_page.add_task("   Написать автотест   ")
    
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(todo_page.TODO_LIST))
    
    tasks = driver.find_elements(*todo_page.TODO_LIST)
    assert len(tasks) == initial_count + 1, "Задача не появилась"
    
    # ✅ ИСПРАВЛЕНИЕ: берём текст только у спана внутри задачи
    task_span = tasks[-1].find_element(By.TAG_NAME, "span")
    actual_text = task_span.text
    expected_text = "Написать автотест"
    
    assert actual_text == expected_text, f"Ожидалось: '{expected_text}', а получили: '{actual_text}'"
    
    delete_btn = tasks[-1].find_element(By.CSS_SELECTOR, ".delete-btn")
    delete_btn.click()
    print("✅ 8. Задача с пробелами обрезана")

# ============================================================
# 3. АСИНХРОННАЯ ЗАГРУЗКА
# ============================================================

def test_async_loading(driver):
    driver.get("http://localhost:8080")
    wait = WebDriverWait(driver, 10)
    
    delay_btn = driver.find_element(By.ID, "delay-btn")
    delay_btn.click()
    
    assert delay_btn.get_attribute("disabled") is not None
    status = driver.find_element(By.ID, "delay-status")
    assert status.is_displayed()
    print("✅ 9. Кнопка заблокирована, 'Загрузка...' видна")
    
    modal = wait.until(EC.visibility_of_element_located((By.ID, "modal")))
    assert modal.is_displayed()
    assert delay_btn.get_attribute("disabled") is None
    print("✅ 10. Модалка появилась, кнопка активна")