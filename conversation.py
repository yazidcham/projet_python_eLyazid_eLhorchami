from hashlib import new
from .menu import MenuGenerator
from .user import User

class ConversationMessage:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message


class Conversation:
    def __init__(self, user1, user2, messages: list[ConversationMessage]) -> None:
        self.user1 = user1
        self.user2 = user2
        self.messages = messages

class ConversationManager:
    def __init__(self, databaseConnector) -> None:
        self.databaseConnector = databaseConnector

    def show(self, user: User, listOfConversations: list[Conversation]):
        menu = MenuGenerator("--- Choisir la conversation à continuer:", user.friendsList)
        usernameToTalkWith = user.friendsList[menu.getChoice() - 1]
        conversation = [x for x in listOfConversations 
            if x.user1 == usernameToTalkWith or x.user2 == usernameToTalkWith]

        if not conversation:
            conversation = Conversation(user.username, usernameToTalkWith, [])
        else:
            conversation = conversation[0]
        
        self._showConversation(user, usernameToTalkWith, conversation)

    def _showConversation(self, user: User, usernameToTalkWith, conversation: Conversation):
        print(("*" * 10) + f"Conversation avec {usernameToTalkWith}")
        for convMessage in conversation.messages:
            print(f"-> {convMessage.sender}: {convMessage.message}")
        
        print("!!! Pour sortir de la conversation, Tapez FIN !!!")

        newMessage = ""
        while newMessage != "FIN":
            newMessage = input("Votre message: ")
            if newMessage != "FIN":
                conversation.messages.append(ConversationMessage(user.username, newMessage))
            if newMessage == "":
                continue
            if newMessage == "FIN":
                return

        conversation.messages.append(ConversationMessage(user.username, newMessage))
        conversations = self.databaseConnector.readConversations()
        conversationObject = [x for x in conversations 
            if (x.user1 == conversation.user1 and x.user2 == conversation.user2)]
        if conversationObject:
            index = conversations.index(conversationObject[0])
            conversations[index] = conversation
        else:
            conversations.append(conversation)

        self.databaseConnector.writeConversations(conversations)
        self._showConversation(user, usernameToTalkWith, conversation)