import json
from typing import List, Dict

class ChatMemory:
    def __init__(self, redis_client):
        self.r = redis_client
        self.ttl = 86400  # 24 hours in seconds

    def get_history(self, user_id: int) -> List[Dict]:
        # Get all messages from the Redis list
        raw_history = self.r.lrange(f"chat:{user_id}", 0, -1)
        if not raw_history:
            return []
        # Convert JSON strings back to Python dicts
        return [json.loads(m) for m in raw_history]

    def add_message(self, user_id: int, role: str, content: str):
        message = json.dumps({"role": role, "content": content})
        # Push to the end of the list
        self.r.rpush(f"chat:{user_id}", message)
        # Refresh the expiration timer
        self.r.expire(f"chat:{user_id}", self.ttl)
        
    def clear_history(self, user_id: int):
        self.r.delete(f"chat:{user_id}")

