#
# Todoist skill for Mycroft
#   - Adds an item to a Project list for todoist (https://todoist.com)
#
import requests
import json
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG

class Todoist(MycroftSkill):
    def __init__(self):
        LOG.debug("Todoist: __init__.")
        MycroftSkill.__init__(self)

    @intent_file_handler('todoist.intent')
    def handle_todoist(self, message):
        # Get API token
        token = self.settings.get('token')
        if token == "":
          self.speak_dialog('No A P I token provided in the configuration.')
          return;

        # Get item and list name
        item = message.data["item"]
        if "listname" in message.data:
          listname = message.data["listname"]
        else:
          self.speak_dialog('No list name specified')
          return

        LOG.debug("Todoist: token: "+token)
        LOG.debug("Todoist: item: "+item)
        LOG.debug("Todoist: list: "+listname)

        resp = requests.get('https://api.todoist.com/rest/v1/projects', headers={'Authorization':'Bearer '+token})
        LOG.debug("JsonResponseCode: "+str(resp.status_code))
        if resp.status_code != 200:
          self.speak_dialog('There was an error calling the todoist A P I.  '+resp.text)
          return;
          
        content=resp.json()
        listid = -1
        for currentitem in content:
          lowercaseItem = currentitem['name'].lower()
          lowercaseListname = listname.lower()
          LOG.debug("test: "+lowercaseItem+" contains "+lowercaseListname)
          if lowercaseListname in lowercaseItem:
              listid = currentitem['id']
              LOG.debug("Found: "+str(listid))

        if listid < 0:
          self.speak_dialog('Unable to find list, '+listname)
          return;
        else:
          data = { "comment_count": 0, "completed": "false", "content": item, "project_id": listid}
          resp = requests.post('https://api.todoist.com/rest/v1/tasks', headers={'Content-Type': 'application/json','Authorization':'Bearer '+token}, data=json.dumps(data))
          if resp.status_code != 200:
            self.speak_dialog('There was an error calling the todoist A P I.  '+resp.text)
            return;
          LOG.debug("POST JsonResponseCode: "+str(resp.status_code))
          self.speak_dialog("todoist" , data={"item" : item, "listname" : listname})

    def initialize(self):
        LOG.debug("Todoist: initialize.")

def create_skill():
    return Todoist()

