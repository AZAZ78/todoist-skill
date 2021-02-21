#
# Todoist skill for Mycroft
#   - Adds an item to a Project list for todoist (https://todoist.com)
#
import todoist

from mycroft import MycroftSkill, intent_file_handler

class Todoist(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.token = None
        self.api = None

    def initialize(self):
        self.log.debug("initialize")
        self.settings_change_callback = self.on_websettings_changed
        self.setup()

    def on_websettings_changed(self):
        self.log.debug("on_websettings_changed")
        self.setup()

    def setup(self):
        # Get API token
        self.token = self.settings.get('token',"")
        if not self.token:
          self.speak('No A P I token provided in the configuration.')
          return
        self.api = todoist.TodoistAPI(self.token)
        self.api.sync()
        self.log.info("Initialized todoist api for {}".format(self.api.state['user']['full_name']))
        return

    @intent_file_handler('todoist.intent')
    def handle_todoist(self, message):
        self.log.debug("handle_todoist")
        if not self.api:
          self.speak('Todoist A P I not initialized.')
          return
        self.api.sync()
        # Get item and list name
        item = message.data["item"].capitalize()
        if "listname" in message.data:
          listname = message.data["listname"].capitalize()
        else:
          self.speak('No list name specified.')
          return

        self.gui["listName"] = listname
        self.gui["itemToAdd"] = item
        self.gui.show_page("display.qml")
        self.log.debug("item: {}".format(item))
        self.log.debug("list: {}".format(listname))

def create_skill():
    return Todoist()

