from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TodoPage(BasePage):
    TODO_INPUT = (By.ID, "todo-input")
    ADD_BTN = (By.ID, "add-todo-btn")
    TODO_LIST = (By.CSS_SELECTOR, "#todo-list li")

    def add_task(self, text):
        self.type(self.TODO_INPUT, text)
        self.click(self.ADD_BTN)

    def get_task_count(self):
        return len(self.driver.find_elements(*self.TODO_LIST))