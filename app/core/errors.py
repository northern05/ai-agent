class ChatErrors:
    GOOGLE_API_RESOURCE_EXHAUSTED = "Google API quota limits reached"
    CHAT_NOT_FOUND = "Chat not found!"
    USER_NOT_OWNER = "That's not your chat!"



class Errors:
    chats = ChatErrors()


errors = Errors()