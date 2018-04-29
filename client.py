class Message:
    def __init__(self, id, senderId, senderName, text):
        self.senderName = senderName
        self.senderId = senderId
        self.id = id
        self.text = text

class Reply:
    def __init__(self, recipentId, text):
        self.recipentId = recipentId
        self.text = text