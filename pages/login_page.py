from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")
    ERROR_MSG = (By.ID, "login-error")
    SUCCESS_MSG = (By.ID, "login-success")

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def is_error_visible(self):
        return self.is_visible(self.ERROR_MSG)

    def is_success_visible(self):
        return self.is_visible(self.SUCCESS_MSG)

    def get_error_text(self):
        return self.get_text(self.ERROR_MSG)