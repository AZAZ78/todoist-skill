#
# Todoist skill for Mycroft
#   - Adds an item to a Project list for todoist (https://todoist.com)
#
import requests
import json
from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

class Todoist(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.log.debug("__init__")
        self.token = None

    def initialize(self):
        self.log.debug("initialize")
        self.settings_change_callback = self.on_websettings_changed
        self.setup()

    def on_websettings_changed(self):
        self.setup()

    def setup(self):
        # Get API token
        self.token = self.settings.get('token',"")
        if not self.token:
          self.speak('No A P I token provided in the configuration.')
        return

    @intent_file_handler('todoist.intent')
    def handle_todoist(self, message):
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
        self.log.debug("Todoist: token: "+self.token)
        self.log.debug("Todoist: item: "+item)
        self.log.debug("Todoist: list: "+listname)

        resp = requests.get('https://api.todoist.com/rest/v1/projects', headers={'Authorization':'Bearer '+self.token})
        self.log.debug("JsonResponseCode: "+str(resp.status_code))
        if resp.status_code != 200:
          self.speak('There was an error calling the todoist A P I.  '+resp.text)
          return
          
        content=resp.json()
        listid = -1
        for currentitem in content:
          lowercaseItem = currentitem['name'].lower()
          lowercaseListname = listname.lower()
          LOG.debug("test: "+lowercaseItem+" contains "+lowercaseListname)
          if lowercaseListname in lowercaseItem:
              listid = currentitem['id']
              self.log.debug("Found: "+str(listid))

        if listid < 0:
          self.speak('Unable to find list, '+listname)
          return
        else:
          data = { "comment_count": 0, "completed": "false", "content": item, "project_id": listid}
          resp = requests.post('https://api.todoist.com/rest/v1/tasks', headers={'Content-Type': 'application/json','Authorization':'Bearer '+token}, data=json.dumps(data))
          if resp.status_code != 200:
            self.speak('There was an error calling the todoist A P I.  '+resp.text)
            return;
          self.log.debug("POST JsonResponseCode: "+str(resp.status_code))
          self.speak_dialog("todoist" , data={"item" : item, "listname" : listname})

def create_skill():
    return Todoist()

