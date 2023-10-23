import logging
import json
from websocket_server import WebsocketServer
import initLogging
import functions
from urllib.parse import unquote
import os

def new_client(client, server):
  logging.debug("New client connected and was given id %d" % client['id'])
  hello = "Hi," + str(client['id'])
  server.send_message(client, hello)

# Called for every client disconnecting
def client_left(client, server):
  logging.debug("Client (%d) disconnected." % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
  logging.debug("Received message: {0}".format(message))
  logging.debug(type(message))
  message = unquote(message)
  logging.debug("Received message 1: {0}".format(message))
  try:
    try:
      obj = json.loads(message)
    except:
      resstr = "no JSON: {0}".format(message)
      return		
    funcName = obj["funcName"]
    func = getattr(functions, funcName)
    if func:
      funcParameters = obj["funcParameters"]
      res = func(funcParameters)
      res["funcName"] = funcName
      resstr = json.dumps(res)
      return
    else:
      resstr = 'Function "{0}" not found'.format(funcName)
      return
  finally:
    logging.debug("Sended message: {0}".format(resstr))
    server.send_message(client, resstr)
    

def start_server(port):
  server = WebsocketServer(port)
  logging.debug("Server listening on port: %d" % port)
  server.set_fn_new_client(new_client)
  server.set_fn_client_left(client_left)
  server.set_fn_message_received(message_received)
  server.run_forever()

initLogging.initLogging()
logging.debug("CALL httpserver.py")

port = 7767
start_server(port)
