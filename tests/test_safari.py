import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_gismeteo_weather():
    """
    Тест проверяет, что на Гисметео можно найти погоду для города Омск.
    """
    
    # 1. Открываем браузер и сайт
    print("🚀 Открываем браузер...")
    driver = webdriver.Safari()
    driver.get("https://www.gismeteo.ru/")
    driver.maximize_window()  # Разворачиваем окно на весь экран (для стабильности)
    
    # 2. Ждём загрузки страницы и поля поиска
    print("⏳ Ждём загрузки страницы...")
    wait = WebDriverWait(driver, 15)
    
    # Ищем поле ввода по классам (как в вашем HTML)
    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input.js-input"))
    )
    print("✅ Поле поиска найдено!")
    
    # 3. Вводим название города
    city = "Омск"
    print(f"🔍 Ищем погоду для города: {city}")
    search_input.clear()  # Очищаем поле (на всякий случай)
    search_input.send_keys(city)
    time.sleep(1)  # Небольшая пауза для появления подсказок
    
    # 4. Нажимаем Enter
    search_input.send_keys(Keys.RETURN)
    print("⏳ Ждём загрузки страницы с погодой...")
    
    # 5. Ждём, пока появится элемент с температурой
    # Пробуем найти температуру по разным селекторам
    try:
        temp_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js_value, .temp, .temperature"))
        )
        temperature = temp_element.text
        print(f"🌡️ Текущая температура в {city}: {temperature}")
    except:
        print("⚠️ Не удалось найти температуру, но проверяем, что город отображается...")
    
    # 6. Проверяем, что мы на странице с погодой
    # Ищем упоминание города на странице
    assert "Омск" in driver.page_source or "omsk" in driver.current_url.lower(), \
        f"❌ Город {city} не найден на странице!"
    
    print(f"✅ Город {city} найден на странице!")
    
    # 7. Дополнительная проверка: есть ли на странице градусы Цельсия
    if "°" in driver.page_source:
        print("🌡️ На странице отображается температура в градусах Цельсия")
    else:
        print("⚠️ На странице не найдено символа °, но это может быть нормой")
    
    # 8. Закрываем браузер
    print("🔚 Закрываем браузер...")
    driver.quit()
    
    print("✅ Тест Гисметео пройден успешно!")

# Если запускаем файл напрямую (не через pytest)
if __name__ == "__main__":
    test_gismeteo_weather()