# BWTest
BWTest is the successor of [BA-Test](https://github.com/ameerwasi001/BA-Test) a framework used for testing browser based applications

This time BA-Test has been improved to include an actual parser, interpreter, and Lexer that interface directly with python preserving it's strength of modulability. It can also be compiled to Python with [BWTst Compiler](https://github.com/ameerwasi001/BWTst-Compiler).

# Supported Browsers
It supports every browser that selenium supports meaning Firefox, Chrome, Safari, Edge and Internet Explorer 3 and drivers for all of them will be required.

# The knowledge required beforehand
There's very little knowledge required beforehand for starting working with this DSL because the only things you need to know are CSS selectors and xpath which is directly accessible in this language but it's totally not for someone who hasn't done any testing before because it has the exact same workflow of selecting elements in a variable and writing or clicking on them.

# Selectors
There are many methods with which elements can be selected and here are the mthods that are currently supported.\n
```
get_element_by_name
get_element_by_id
get_element_by_xpath
get_element_by_class
get_element_by_tag
get_element_by_link_text
get_element_by_css_selector
```
In future there are plans for more selectors that just use xpath under the hood.

# Syntax
This language has very few syntax gotcha's but it still has some and here's the basic syntax that you would need to know to start doing browser testing in this language.

## Starting a web browser
```start => ("chrome", "C:/Browserdriver/chromedriver.exe")```

So, yeah you say start, then assign arguments using this sign `=>` and the only two arguments seprated by `,` are the browser you are going to use and the path to the driver. 

## Visiting a website
```visit => ("https://www.google.com/")```

Yep, it's that simple you just go ahead and say visit, then assign arguments using this sign `=>` and the only required argument here is the URL of the website you want to visit but make sure to add `http://www.`, because BA-Test at least for now doesn't recognize URLs without this beginning.

## Selecting an element
Similar to what we had done above we will just

```get_element_by_name => ("q", "google_search")```

but in this particular instance we assign two arguments seprated by `,` and the first argument asks for the name that you want it to search for, in a page while the second one asks for the name that you want to store it with so that you can use it later in rest of your test.

Other methods can be used in a similar manner, by just providing name, id or xpath respectively.

## Writing on an element
```write => ("google_search", "PyCon is big")```

You might write on an element by first calling the name you used to store the found element which may or may not be more than one which in our case it's not so we don't need to pass any optional arguments so, the next argument here is and string because it contains spaces but if it didn't then we could have just typed `PyCon is big` instead of `'PyCon is big'` which requires either double or single quotes.
The write method presses enters unless you pass an optional argument `enter->false` in the same line.

## Action Chains
### Action initialization
Action chains need to be intialized before using and it can be done by simply saying something along the lines of what follows

```action_initialize => ()```

### Action Methods
#### Text Action
This function command named ```text_action``` sends some text over to the currently focused field, it takes two arguments but one of them is required and it is, ```text_args``` and it as you have probably guessed takes text arguments that you want to be typed and the second one which is optional is named enter and is by default true and if you don't want to hit enter after sending the text then you should make it False. Some Sample code it's usage is what follows.

```
visit => ("https://www.google.com/")
action_initialize => ()
text_action => ("That's true")
action_perform => ()
sleep => (10)
close => ()
```

#### Perform
Perhaps the simplest to use yet the most important in the entire action chain section is this one because it makes you be able to perform actions when you are done linking them up and it's used something like what follows

```action_perform => ()```

## Switching between windows
In web applications, it's common to have multiple windows and in order to switch between them you should use `switch_to`, and in order  to do that you must be able to provide the name of the window as an argument to this command. Following is a way of using this command.

```switch_to => ("myWin")```

## Wait
In the process of testing you may want to wait for certain things to happen, even though going to website by either clicking or visiting through the methods alredy does so but, you now can wait by sleeping, meaning using sleep method.

```sleep => (10)```

The above as you might have guessed asks system to wait for 10 seconds before doing anything else.

## Comments
```$ Hey, this part finds search results```

Some times you might want to write some arbitrary text for someone reading your code and to do so you can do what's done above and start your line by `$` symbol.

## Indexed elements
If we ask for an element where multiple search results are found this stores them in a list by index starting from 0 so that you can call it with index whenever required. What follows is an example for you to find search results through xpath and store all of them in a list.
```
get_element_by_xpath => (("//h3[@class='LC20lb']"), ("results"))
click => ("results", index->1)
```

While the first one is quite self explanatory the second one needs an explanation about the optional argument `index` being passed, it says that click the second index of the found results because results start from 0, so what it'll do is click the second index meaning the index number one which correlates to the second search result.

## Close
`close => ()`

If you decide to close your browser window after a certain test is done, then you can use the `close` method with no arguments passed whatsoever.

## Variables
This language can help you store, read and re-evaluate certain variables namely strings, floats, booleans, null and integers.
### Setting a variable
Setting a variable is quite simple, you can just state
```
wait = 2
```
Setting a variable is as simple as that and we can do the same for setting every other type.
### Getting a variable
Getting a variable is just as simple, you can just state
```
wait
```
anywhere in the program so you might be thinking about how you can assign a variables value to an argument.
```
sleep => (wait->3)
```
and the same thing can be done with optional arguments.

### Basic math with a variable
All basic math can be done with variables in BWTest like this,
```
wait + 4-2/4
```
thanks, for reading through and we'll hope you'll continue to use BWTest.

# Development
Wait, were you a developer looking for a test writing DSL for your testers or business people to use and for you to extend we got you. This language has a file named `Extensions.py` where you can write methods and they will be directly accessible in this language and what follows is a plethora of things you would need to know before you can start extending this DSL to meet your needs.

## Class variables
There are a few class variables used as memory for BA-Test, the first one is **driver** which is the driver we want to use for browser automation, **ActionChain** which is initialized by action_initialize and is responsible for all actions in action chain, the second one is **string** that turns python string into a BWTest String, the second one is **string** that turns python float or int into a BWTest Number, then there is **false**, that is BWTest's false and the same can be said about true and nil, the last one is **elements** which ofcourse is the memory used to store elements.

## Conviniensizer
There's a tool in tools folder for name conviniencizer, it takes your python file and wraps ```self.string``` around every string and ```self.number``` around every number. You can use it to ease writing BWTest functions in pythoon for instance this,

```
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
```
becomes this, 

```
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
 ```
 ## findElement
You would have to use this function to find an element and whenever you'd have to find an element from class element you must have an element and an index argument which by default should be `None`, and what follows is an example extension of this file where I make another function to click a button.
```
def testClicker(element, index=None):
  self.findElement(element, index).click()
```
## listOrNot
This is used to check the given element appropriately and to convert list to an element if nessecary and to raise appropriate errors if required and what follows is an example for a `find_element_by_class` method in extensions.
```
def find_element_by_class(elem_class, index):
  self.elements[index.value] = driver.find_elements_by_class_name(elem_class.value)
  self.listOrNot(index)
```
## Boolean2bool
Everything given by the language is a value class with no exceptions whatsoever.
```
if self.Boolean2bool(enter):
  print("we are going to press enter")
```
# What's to come
Some of the examples such as the "class" one is implemented in the core language now, more optimizations will be done for this language and more functions for developers' convenience will also be avalible.

# Thanks
This time for real, thanks for reading through and we hope to thank you for using this language for test writing purposes.
