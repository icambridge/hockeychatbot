import time
import client
import coloredlogs
import logging

class MainEngine:
    def __init__(self, client, parser, intents):
        self.intents = intents
        self.parser = parser
        self.client = client

    def run(self):

        dms = self.client.getMessages(None)
        lastMsg = self.getLastMessage(dms, None)
        conversations = {}
        while True:
            dms = self.client.getMessages(lastMsg)
            for username, rawConversation in dms.items():
                if username in conversations.keys():
                    lastConversation = conversations[username]
                else:
                    lastConversation = None
                parsedConverstation = self.parser.parseConversation(rawConversation, lastConversation)
                logging.info("Intent:%s - Entintes : %s" % (parsedConverstation.intent, parsedConverstation.proEntities) )
                response, conversationToStore = self.intents[parsedConverstation.intent].execute(parsedConverstation)
                reply = self.createReply(response, parsedConverstation.lastMsg)
                self.client.sendReply(reply)
                conversations[username] = conversationToStore
            lastMsg = self.getLastMessage(dms, lastMsg)
            time.sleep(6)

    def createReply(self, text, lastMsg):
        return client.Reply(lastMsg.senderId, text)

    def getLastMessage(self, dms, lastMsg):
        lastMsgs = []
        for username, rawConversation in dms.items():
            rawConversation = sorted(rawConversation, key=lambda x: x.id, reverse=True)
            lastMsgs.append(rawConversation[0])

        if (len(lastMsgs) > 0):
            lastMsg = sorted(lastMsgs, key=lambda x: x.id, reverse=True)[0]
        return lastMsg