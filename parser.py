import logging

class Conversation:
    def __init__(self, intent, proEntites, negEntities, msgs, affirmations, denials):
        self.denials = denials
        self.affirmations = affirmations
        msgs = sorted(msgs, key=lambda x: x.id, reverse=True)
        self.msgs = msgs
        self.negEntities = negEntities
        self.proEntities = proEntites
        self.intent = intent
        self.lastMsg = msgs[-1]

class Parser():
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def parseConversation(self, receivedMessages, conversation):
        if len(receivedMessages) == 0:
            return None


        if conversation != None:
            print(conversation)
            receivedMessages.extend(conversation.msgs)
        else:
            # If there is no conversation we don't want to start at the begining
            receivedMessages.reverse()
        lastIntent = None
        proEntities = {}
        negEntities = {}
        msgs = []
        affirmations = []
        denials = []
        for msg in receivedMessages:
            logging.info("ID %s: @%s - %s" % (msg.id, msg.senderName, msg.text))
            intData = self.interpreter.parse(msg.text)
            intent = intData["intent"]["name"]
            if intent == "affirm":
                print("J:" + msg.text)
                affirmations.append(msg)
                continue
            if intent == "deny":
                print("N:" + msg.text)
                denials.append(msg)
                continue
            # Handle extend intents
            intent = intent.split("_")[0]
            if lastIntent != None and lastIntent != intent:
                logging.info("lastIntent: %s and intent: %s" % (lastIntent, intent))
                break
            proEntities = self.parseEntites(proEntities, intData["entities"])
            lastIntent = intent
            msgs.append(msg)
        return Conversation(lastIntent, proEntities, negEntities, msgs, affirmations, denials)

    def parseEntites(self, current, new):
        for ent in new:
            name = ent["entity"]
            value = ent["value"]
            print("%s:%s" % (name, value))
            current[name] = value
        return current