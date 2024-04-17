import json
from typing import List, Optional

from langchain_community.chat_message_histories import (
    RedisChatMessageHistory,
)
from langchain_community.utilities.redis import get_client
from langchain_core.messages import (
    BaseMessage,
    messages_from_dict,
)


class RedisChatMessageHistoryWindowed(RedisChatMessageHistory):
    """Chat message history stored in a Redis database."""

    def __init__(
        self,
        session_id: str,
        url: str = "redis://localhost:6379/0",
        key_prefix: str = "message_store:",
        ttl: Optional[int] = None,
        chat_history_length: int = 20,
    ):
        try:
            import redis
        except ImportError:
            raise ImportError("Could not import redis python package. " "Please install it with `pip install redis`.")

        try:
            self.redis_client = get_client(redis_url=url)
        except redis.exceptions.ConnectionError as error:
            raise ConnectionError(f"Could not connect to Redis at {url}.") from error

        self.session_id = session_id
        self.key_prefix = key_prefix
        self.ttl = ttl
        self.chat_history_length = chat_history_length

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from Redis"""
        _items = self.redis_client.lrange(self.key, 0, -1)
        # items = [json.loads(m.decode("utf-8")) for m in _items[::-1]]
        _items = _items[0 : self.chat_history_length]
        items = [json.loads(m.decode("utf-8")) for m in _items[::-1]]
        messages = messages_from_dict(items)
        return messages
