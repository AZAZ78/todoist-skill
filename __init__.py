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
          self.speak_dialog('todoist.error.configuration')
          return
        self.api = todoist.TodoistAPI(self.token)
        self.api.sync()
        self.log.info("Initialized todoist api for {}".format(self.api.state['user']['full_name']))
        return

    @intent_file_handler('todoist.intent')
    def handle_todoist(self, message):
        self.log.debug("handle_todoist")
        if not self.api:
          self.speak_dialog('todoist.error.connect')
          return
        # Get item and list name
        item = message.data["item"].capitalize()
        if "listname" in message.data:
          listname = message.data["listname"]
        else:
          self.speak_dialog('todoist.error.list_not_specified')
          return
        
        self.gui["listName"] = listname
        self.gui["itemToAdd"] = item
        self.gui.show_page("display.qml")
        self.log.debug("item: {}, list: {}".format(item, listname))
        
        self.api.sync()
        projects = self.api.state['projects']
        id = None
        for proj in projects:
            if proj['name'].lower() == listname:
                id = proj['id']
        if id is None:
            self.log.info("list not found")
            self.speak_dialog('todoist.error.list_not_found', data={"listname": listname})
            return
        
        new_item = self.api.items.add(item)
        self.api.commit()
        new_item.move(project_id=id)
        self.api.commit()
        
        self.speak_dialog('todoist.success', data={"item": item, "listname": listname})

def create_skill():
    return Todoist()

