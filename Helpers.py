from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from Values import *

class HelpCycle:
    def __init__(self):
        self.driver = None
        self.ActionChain = None
        self.string = String
        self.number = Number
        self.true = true
        self.false = false
        self.nil = nil
        self.elements = {}
        self.variables = {}

    def findElement(self, element, index):
        return self.elements[element.value] if isinstance(index, nilObject) else self.elements[element.value][int(index.value)]

    def Boolean2bool(self, boolean):
        if not isinstance(boolean, Boolean):
            raise Exception(f"{boolean} is not a Boolean")
        return bool(boolean.state)

    def listOrNot(self, index):
        if isinstance(self.elements[index.value], list) and len(self.elements[index.value]) == 1:
            self.elements[index.value] = self.elements[index.value][0]
        elif isinstance(self.elements[index.value], list) and len(self.elements[index.value]) == 0:
            raise KeyError ("No element with matching attributes found")

    def sleep(self, wait):
        time.sleep(int(wait.value))

    def Print(self, *values, **kwargs):
        values = [x.value for x in values]
        print(*values, end="")

    def start(self, browser, path='/'):
        if browser.value.upper() == 'CHROME':
            self.driver = webdriver.Chrome(path.value)
        elif browser.value.upper() == 'FIREFOX':
            self.driver = webdriver.Firefox(path.value)
        elif browser.value.upper() == 'EDGE':
            self.driver = webdriver.Edge(path.value)
        elif browser.value.upper() == 'SAFARI':
            self.driver = webdriver.Safari(path.value)

    def get_element_by_name(self, name, index):
        self.elements[index.value] = self.driver.find_elements_by_name(name.value)
        self.listOrNot(index)

    def get_element_by_class(self, class_name, index):
        self.elements[index.value] = self.driver.find_elements_by_class_name(class_name.value)
        self.listOrNot(index)

    def action_initialize(self):
        self.ActionChain = ActionChains(self.driver)

    def text_action(self, *text_args, enter=true):
        text_args = [x.value for x in text_args]
        self.ActionChain.send_keys(*text_args)
        if self.Boolean2bool(enter):
            self.ActionChain.send_keys(Keys.ENTER)

    def action_perform(self):
        self.ActionChain.perform()

    def get_element_by_id(self, elem_id, index):
        self.elements[index.value] = self.driver.find_elements_by_id(elem_id.value)
        self.listOrNot(index)

    def get_element_by_xpath(self, xpath, index):
        self.elements[index.value] = self.driver.find_elements_by_xpath(xpath.value)
        self.listOrNot(index)

    def get_element_by_css_selector(self, selector, index):
        self.elements[index.value] = self.driver.find_element_by_css_selector(selector.value)
        self.listOrNot(index)

    def get_element_by_tag(self, tag, index):
        self.elements[index.value] = self.driver.find_elements_by_tag_name(tag.value)
        self.listOrNot(index)

    def get_element_by_link_text(self, mode, text, index):
        if mode.value.lower() == "absolute":
            self.elements[index.value] = self.driver.find_elements_by_link_text(text.value)
        elif mode.value.lower() == "partial":
            self.elements[index.value] = self.driver.find_elements_by_partial_link_text(text)
        else:
            raise TypeError (f"undefined type {mode}")
        self.listOrNot(index)

    def clear(self, element, index):
        self.findElement(element, index).clear()

    def write(self, element, words, index=nil, clear=true, enter=true):
        if self.Boolean2bool(clear):
            self.findElement(element, index).clear()
        self.findElement(element, index).send_keys(words.value)
        if self.Boolean2bool(enter):
            self.findElement(element, index).send_keys(Keys.RETURN)

    def click(self, element, index=nil):
        self.findElement(element, index).click()

    def switch_to(self, window_name):
        self.driver.switch_to_window(window_name.value)

    def visit(self, *args):
        args = [x.value for x in args]
        self.driver.get(*args)

    def close(self):
        self.driver.close()
