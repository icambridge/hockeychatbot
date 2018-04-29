import client
import logging

class TwitterClient:
    def __init__(self, api):
        self.api = api

    def getMessages(self, lastMessage = None):
        if lastMessage == None:
            sinceId = None
        else:
            sinceId = lastMessage.id
        dms = self.api.GetDirectMessages(since_id=sinceId)
        return self.groupMessages(dms)

    def parseMessage(self, message):
        return client.Message(message.id, message.sender_id, message.sender.screen_name, message.text)

    def groupMessages(self, messages):
        output = {}
        for orgMsg in messages:
            msg = self.parseMessage(orgMsg)
            if msg.senderName in output.keys():
                output[msg.senderName].append(msg)
            else:
                output[msg.senderName] = [msg]
        for key, list in output.items():
            output[key] = sorted(list, key=lambda x: x.id, reverse=False)

        return output

    def sendReply(self, reply):
        logging.info("Sending message '%s' to %s" % (reply.text, reply.recipentId))
        self.api.PostDirectMessage(reply.text, reply.recipentId)