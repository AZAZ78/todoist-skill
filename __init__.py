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

    @intent_file_handler('todoist.create.list.intent')
    def handle_todoist_list(self, message):
        self.log.debug("handle_todoist_item_list")
        if not self.api:
          self.speak_dialog('todoist.error.connect')
          return

        if "listname" in message.data:
          listname = message.data["listname"]
        else:
          self.speak_dialog('todoist.error.list_not_specified')
          return
        self.log.debug("list: {}".format(listname))

        self.api.sync()
        self.api.projects.add(listname)
        try:
            self.api.commit()
        except todoist.api.SyncError as err:
            self.speak("Error during commit: {}".format(err.args[1]['error']))
            return

        self.speak_dialog('todoist.success.list', data={"listname": listname})

    @intent_file_handler('todoist.create.item.intent')
    def handle_todoist_item(self, message):
        self.log.debug("handle_todoist_item_list")
        if not self.api:
          self.speak_dialog('todoist.error.connect')
          return
        # Get item and list name
        if "item" in message.data:
          item = message.data["item"].capitalize()
        else:
          self.speak_dialog('todoist.error.item_not_specified')
          return

        self.gui["listName"] = 'None'
        self.gui["itemToAdd"] = item
        self.gui.show_page("display.qml")
        self.log.debug("item: {}".format(item))
        
        self.api.sync()
        new_item = self.api.items.add(item)
        try:
            self.api.commit()
        except todoist.api.SyncError as err:
            self.speak("Error during commit: {}".format(err.args[1]['error']))
            return
        
        self.speak_dialog('todoist.success.item', data={"item": item})

    @intent_file_handler('todoist.create.item.list.intent')
    def handle_todoist_item_list(self, message):
        self.log.debug("handle_todoist_item_list")
        if not self.api:
          self.speak_dialog('todoist.error.connect')
          return
        # Get item and list name
        if "item" in message.data:
          item = message.data["item"].capitalize()
        else:
          self.speak_dialog('todoist.error.item_not_specified')
          return

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
        
        new_item = self.api.items.add(item, project_id=id)
        try:
            self.api.commit()
        except todoist.api.SyncError as err:
            self.speak("Error during commit: {}".format(err.args[1]['error']))
            return
        
        self.speak_dialog('todoist.success.item.list', data={"item": item, "listname": listname})

def create_skill():
    return Todoist()

