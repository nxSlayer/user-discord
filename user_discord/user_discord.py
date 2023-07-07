from user_discord.utils.objects import MessageContent, MessageSend, AuthorProfile
from requests.structures import CaseInsensitiveDict
from user_discord.utils import payloads
from .utils import Thread
import websocket
import requests
import logging
import base64
import random
import time
import json



_log = logging.getLogger(__name__)

global_variables = {}

class ClientDiscord:

  def __init__(self, prefix: str = '', no_warns: bool = False):
    self.no_warns = no_warns
    
    self.token = None
    self.prefix = prefix

    self.Username = None
    self.email = None
    self.id = None
    self.telephone = None

    #Guild parameters
    self.online_members = []
    
    #Reqs
    self.headers = CaseInsensitiveDict()
    self.var_ = "(user_discord)"
    self.commands = {}
    

  def command(self, name):
        """Register function for events
        -> name: The name of event
        """
        def decorator(func):
            self.commands[self.prefix+name] = func
            return func
        return decorator

  def wait(self):
    while True:
      time.sleep(5)
  
  def emit_command(self, command, mc, *args):
    try:
        if command in self.commands:
            return self.commands[command](mc, *args)
        else:
            return "not found"
    except Exception as g:
      _log.critical(g)
          
  def generate_nonce(self):
    return str(random.randint(int("1"+"0"*18), int("21"+"0"*17)))

  def login_token(self, token):
    # "Login" in account with token
    global requests
    global global_variables
    api = "https://discord.com/api/users/@me"
    temp_headers = CaseInsensitiveDict()
    temp_headers['Authorization'] = token
    res = requests.get(api, headers=temp_headers)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      data = res.json()
      self.headers['Authorization'] = token
      self.web = requests.Session()
      self.web.headers = self.headers
      self.username = data['username']
      self.id = data['id']
      self.email = data['email']
      self.telephone = data['phone']
      self.token = token
      global_variables = self
      if not self.no_warns:
        print(f'{self.var_} - Logged as: {self.username}')
      return data

  def send_message(self, channelId, message):
    #Send message in channel
    api = f"https://discord.com/api/v9/channels/{channelId}/messages"
    payload = {
      "content": message,
      "flags": 0,
      "nonce": self.generate_nonce(),
      "tts": False
    }
    res = self.web.post(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return MessageSend(res.json(), self).MessageSend

  def reply_message(self, channelId, messageId, content):
    #Reply Message
    api = f"https://discord.com/api/v9/channels/{channelId}/messages"
    payload = payloads.ReplyMessage(channelId, messageId, content, self.generate_nonce())
    res = self.web.post(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return MessageSend(res.json(), self).MessageSend

  def edit_message(self, channelId, messageId, content):
    #Edit Message
    api = f"https://discord.com/api/v9/channels/{channelId}/messages/{messageId}"
    res = self.web.patch(api, json={"content": content})
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return MessageSend(res.json(), self).MessageSend
    
      
  def delete_message(self,channelId, messageId):
    #Delete a message by channel and message id
    api = f"https://discord.com/api/v9/channels/{channelId}/messages/{messageId}"
    res = self.web.delete(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.status_code

  def get_dms(self):
    #Get a list of users in DM
    api = "https://discordapp.com/api/users/@me/channels"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_servers(self):
    # Get a list of your servers
    api = "https://discord.com/api/users/@me/guilds"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_friends(self):
    # Get a list of your friends
    api = "https://discord.com/api/users/@me/relationships"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def get_channel_messages(self, channelId, limit: int = 50):
    #Get a list of messages in channel
    api = f"https://discord.com/api/v9/channels/{channelId}/messages?limit={limit}"
    res = self.web.get(api)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_status(self, status, content: str = None, emoji: str = None):
    #Set user status
    api = "https://discord.com/api/v9/users/@me/settings"
    payload = {"status": status, "custom_status":{"text":content,"emoji_name":emoji}}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_bio(self, content):
    #Set user bio
    api = "https://discord.com/api/v9/users/@me/profile"
    payload = {"bio": content}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()

  def set_avatar(self, url):
    #Change user avatar by url
    image_data = requests.get(url).content
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    data = f"data:image/png;base64,{image_b64}"

    api = "https://discord.com/api/v9/users/@me"
    payload = {"avatar": data}
    res = self.web.patch(api, json=payload)
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()
      
  def get_members(self, socket, guild_id, channel_id):
    #Get members from channel
    socket.send_json({"op":14,"d":{"guild_id":guild_id,"channels":{channel_id:[[0,99]]}}})
    time.sleep(2)
    return self.online_members

  def get_user(self, user_id):
    #Get user from id
    api = "https://discord.com/api/v9/users/@me/channels"
    res = self.web.post(api, json={"recipients": [str(user_id)]})
    if res.status_code != 200:
      return Exception(res.text)
    else:
      return res.json()