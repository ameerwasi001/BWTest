from Helpers import HelpCycle

class Helper(HelpCycle):
    def __init__(self):
        super().__init__()

    def vispy(self):
        self.visit("http://www.python.org")
        self.get_element_by_link_text("absolute", "Become a Member", index="button")
        self.click("button")
        self.sleep(2)
        self.get_element_by_id("id_login", "username")
        self.write("username", "ameerShah@gmail.com", enter=self.false)
        self.get_element_by_id("id_password", "password")
        self.write("password", "helloameer", enter=self.false)
        self.get_element_by_class("primaryAction", "submit")
        self.click("submit")
        self.sleep(2)
