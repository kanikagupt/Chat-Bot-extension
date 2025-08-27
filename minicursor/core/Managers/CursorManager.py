from core.Tools.CursorGraph import create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = "mongodb://admin:admin@localhost:27017"
client = MongoClient(
    "mongodb+srv://ayushnimiwal47:aayushnimiwal@cluster0.cknvjfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tls=True,
    tlsAllowInvalidCertificates=True
)

class CursorManager:
    def chat_with_cursor(self,thread_id,query):
        last_message = None
        config = {"configurable": {"thread_id": f"{thread_id}"}}
        with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
            graph = create_chat_graph(checkpointer)
            messages = [{"role": "user", "content": query}]
            for event in graph.stream({ "messages": messages }, config, stream_mode="values"):
                if "messages" in event:
                    # event["messages"][-1].pretty_print()
                    last_message = event["messages"][-1]
                    ai_message = {
                        "role": "ai",
                        "content": last_message.content if last_message else ""
                    }
                    messages.append(ai_message)
                    self.store_message_in_db(thread_id, messages)
        return last_message.content if last_message else None
    
    def store_message_in_db(self, thread_id, messages):
        """Store or update the messages for a particular thread_id in MongoDB."""
        db = client["user_chats"] 
        collection = db["messages"]

        collection.update_one(
            {"thread_id": thread_id},
            {
                "$set": {"thread_id": thread_id},
                "$push": {"messages": {"$each": messages}}
            },
            upsert=True
        )

    def get_chats(self, thread_id):

        db = client["user_chats"]
        collection = db["messages"]

        document = collection.find_one({"thread_id": thread_id})

        if not document or "messages" not in document:
            return [] 

        formatted_messages = [
            {"sender": msg["role"], "text": msg["content"]}
            for msg in document["messages"]
            if "role" in msg and "content" in msg
        ]

        return formatted_messages
    
    def get_chat_ids(self):
        db = client["user_chats"]
        collection = db["messages"]

        # Fetch only thread_id fields from all documents
        thread_ids = collection.distinct("thread_id")

        return thread_ids
