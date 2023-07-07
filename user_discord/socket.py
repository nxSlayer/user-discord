from .utils.objects import MessageContent, AuthorProfile
from .utils.payloads import StartSocket
from threading import Thread
from .utils import payloads
import websocket
import logging
import inspect
import json
import time
import os



_log = logging.getLogger(__name__)


class SocketDiscord:
    def __init__(self, client):
        self.events = {}
        self.ws = None
        self.token = client.token
        self.client = client
        
        self.session_id = None
        

    def on(self, event):
        if payloads.FormatEvent(event):
          event = payloads.FormatEvent(event)
        def event_ready(handler):
            if event not in self.events:
                self.events[event] = []
            self.events[event].append(handler)
            return handler
        return event_ready

    def trig(self, event, *args, **kwargs):
        if event in self.events:
            for handler in self.events[event]:
                try:
                  if len(inspect.signature(handler).parameters) == 0:
                    handler()
                  else:
                     handler(*args, **kwargs)
                except Exception as g:
                   _log.critical(str(g))

    def send_json(self, payload):
        self.ws.send(json.dumps(payload))


    def receive_json(self):
      response = self.ws.recv()
      if response:
        return json.loads(response)
        
    def send_and_receive_json(self, payload):
      self.ws.send(json.dumps(payload))
      res = json.loads(self.ws.recv())
      return res

    def heartbeat(self):
      timer = 40
      payload = {
      "op": 1,
      "d": None
    }
      while True:
        time.sleep(timer)
        self.send_json(payload)

    def start_ws(self):
      self.ws = websocket.WebSocket()
      self.ws.connect('wss://gateway.discord.gg/?encoding=json')
      self.send_json(StartSocket(self.token))
      Thread(target=self.event_manager).start()

    def get_object(self, data):
      if data['t'] == "READY":
        self.session_id = data.get('d').get('session_id')
        if not self.client.no_warns:
          print(f"{self.client.var_} - Session ID: {self.session_id}")
        
      if data['t'] == 'MESSAGE_CREATE':
        if data['d']['content'].split()[0] in self.client.commands:
          try:
              arg = data['d']['content'].split()[1:]
              require_params = len(inspect.signature(self.client.commands[data['d']['content'].split()[0]]).parameters)-1
          except Exception as g:
            print(g)
          if len(arg) < require_params:
            while len(arg) < require_params:
              arg.append(None)
              
          return self.client.emit_command(data['d']['content'].split()[0], MessageContent(data, self.client).MessageContent, *arg[:require_params])
        return MessageContent(data, self.client).MessageContent

      if data['t'] == 'GUILD_MEMBER_LIST_UPDATE':
        if data['s'] == 3:
          try:
            for item in data['d']['ops'][0]['items']:
              if item.get('member'):
                self.client.online_members.append(AuthorProfile(item['member']['user']).AuthorProfile)
          except:self.client.online_members = []
      
      return data
      
    def event_manager(self):
      while True:
        event = self.receive_json()
        try:
            self.trig('all', event)
            self.trig(event['t'], self.get_object(event))

        except:
            self.trig('others', event)