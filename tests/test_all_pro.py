import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.login_page import LoginPage
from pages.todo_page import TodoPage



@pytest.mark.parametrize("username, password, expected_result", [
    ("adm", "wrong", "error"),
    ("admin", "admin123", "success"),
])
def test_login_with_checks(driver, username, password, expected_result):

    
    page = LoginPage(driver)
    driver.get("http://localhost:8080")
    

    login_btn = driver.find_element(*page.LOGIN_BTN)
    try:
        assert login_btn.get_attribute("disabled") is not None
        print("✅ Кнопка 'Войти' недоступна")
    except AssertionError:
        print("❌ Ошибка: кнопка доступна, а должна быть недоступна")

        pytest.assume(False, "Кнопка должна быть недоступна")
    

    page.type(page.USERNAME_INPUT, username)
    page.type(page.PASSWORD_INPUT, password)

    try:
        assert login_btn.get_attribute("disabled") is None
        print("✅ Кнопка 'Войти' активна")
    except AssertionError:
        print("❌ Ошибка: кнопка не стала активной")
        pytest.assume(False, "Кнопка должна стать активной")
    

    page.click(page.LOGIN_BTN)
    

    if expected_result == "error":
        try:
            assert page.is_error_visible()
            print("✅ Ошибка появилась")
        except AssertionError:
            print("❌ Ошибка: ошибка не появилась")
            pytest.assume(False, "Ошибка не появилась")
    else:
        try:
            assert page.is_success_visible()
            print("✅ Успех появился")
        except AssertionError:
            print("❌ Ошибка: успех не появился")
            pytest.assume(False, "Успех не появился")




def test_todo_with_checks(driver):
    """Тест списка задач с обработкой ошибок"""
    
    # 1. Логинимся
    login_page = LoginPage(driver)
    driver.get("http://localhost:8080")
    login_page.login("admin", "admin123")
    
    todo_page = TodoPage(driver)
    

    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(todo_page.TODO_LIST))
        print("✅ Список задач загружен")
    except TimeoutException:
        print("❌ Ошибка: список задач не загрузился")
        pytest.assume(False, "Список задач не загрузился")
        return
    

    initial_count = todo_page.get_task_count()
    print(f"📊 Начальное количество задач: {initial_count}")
    

    todo_page.add_task("Купить хлеб")
    

    new_count = todo_page.get_task_count()
    try:
        assert new_count == initial_count + 1
        print(f"✅ Задача добавлена. Количество: {new_count}")
    except AssertionError:
        print("❌ Ошибка: задача не добавилась")
        pytest.assume(False, "Задача не добавилась")
    

    try:
        tasks = driver.find_elements(*todo_page.TODO_LIST)
        task_span = tasks[-1].find_element(By.TAG_NAME, "span")
        actual_text = task_span.text
        assert "хлеб" in actual_text
        print(f"✅ Текст задачи: {actual_text}")
    except (AssertionError, NoSuchElementException):
        print("❌ Ошибка: задача не найдена или текст неверный")
        pytest.assume(False, "Текст задачи неверный")
    

    try:
        delete_btn = tasks[-1].find_element(By.CSS_SELECTOR, ".delete-btn")
        delete_btn.click()
        print("✅ Задача удалена")
    except NoSuchElementException:
        print("❌ Ошибка: не найдена кнопка удаления")
        pytest.assume(False, "Кнопка удаления не найдена")
    

    final_count = todo_page.get_task_count()
    try:
        assert final_count == initial_count
        print(f"✅ Задача удалена. Количество: {final_count}")
    except AssertionError:
        print("❌ Ошибка: задача не удалилась")
        pytest.assume(False, "Задача не удалилась")




def test_async_loading_stable(driver):

    
    driver.get("http://localhost:8080")
    wait = WebDriverWait(driver, 15)  # Увеличили время
    
    delay_btn = driver.find_element(By.ID, "delay-btn")
    delay_btn.click()

    try:
        assert delay_btn.get_attribute("disabled") is not None
        print("✅ Кнопка недоступна")
    except AssertionError:
        print("❌ Ошибка: кнопка не стала недоступной")
        pytest.assume(False, "Кнопка должна стать недоступной")
    

    try:
        status = driver.find_element(By.ID, "delay-status")
        assert status.is_displayed()
        print("✅ Статус 'Загрузка...' виден")
    except (AssertionError, NoSuchElementException):
        print("❌ Ошибка: статус загрузки не появился")
        pytest.assume(False, "Статус загрузки не появился")
    
 
    try:
        modal = wait.until(EC.visibility_of_element_located((By.ID, "modal")))
        assert modal.is_displayed()
        print("✅ Модалка появилась")
    except TimeoutException:
        print("❌ Ошибка: модалка не появилась")
        pytest.assume(False, "Модалка не появилась")
    

    try:
        assert delay_btn.get_attribute("disabled") is None
        print("✅ Кнопка снова активна")
    except AssertionError:
        print("❌ Ошибка: кнопка не стала активной")
        pytest.assume(False, "Кнопка должна стать активной")