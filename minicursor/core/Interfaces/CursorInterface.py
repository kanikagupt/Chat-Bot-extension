from core.Managers.CursorManager import CursorManager
class CursorInterface:
    def __init__(self):
        self.mgr = CursorManager()

    def chat_cursor(self,thread_id, query):
        return self.mgr.chat_with_cursor(thread_id,query)
    
    def get_chats(self,thread_id):
        return self.mgr.get_chats(thread_id)
    
    def get_chat_ids(self):
        return self.mgr.get_chat_ids()