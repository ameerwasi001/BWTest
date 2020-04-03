from Helpers import HelpCycle


class Helper(HelpCycle):

    def __init__(self):
        super().__init__()

    def vispy(self):
        self.visit(self.string('http://www.python.org'))
        self.get_element_by_link_text(self.string('absolute'), self.string(
            'Become a Member'), index=self.string('button'))
        self.click(self.string('button'))
        self.sleep(self.number(2))
        self.get_element_by_id(self.string('id_login'), self.string('username')
            )
        self.write(self.string('username'), self.string(
            'ameerShah@gmail.com'), enter=self.false)
        self.get_element_by_id(self.string('id_password'), self.string(
            'password'))
        self.write(self.string('password'), self.string('helloameer'),
            enter=self.false)
        self.get_element_by_class(self.string('primaryAction'), self.string
            ('submit'))
        self.click(self.string('submit'))
        self.sleep(self.number(2))
