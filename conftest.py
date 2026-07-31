import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """Фикстура: открывает и закрывает браузер для каждого теста"""
    options = Options()
    
    # ---- НАСТРОЙКИ, ЧТОБЫ НЕ БЕСИЛО ОКНО ВХОДА В GOOGLE ----
    options.add_argument("--no-first-run")                           # не показывать приветствие
    options.add_argument("--disable-blink-features=AutomationControlled")  # скрыть автоматизацию
    options.add_argument("--disable-infobars")                       # убрать плашку "Управляется автоматизированным ПО"
    options.add_argument("--disable-notifications")                  # отключить уведомления браузера
    
    # Убираем флаг автоматизации (чтобы Chrome не палился)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Запускаем браузер
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    # Дополнительно: удаляем следы автоматизации через JavaScript
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    driver.quit()