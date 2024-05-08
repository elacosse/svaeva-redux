def retrieve_redis_windowed_chat_history_as_text(
    session_id: str, url: str, key_prefix: str, chat_history_length: int = 30
) -> str:
    """
    Retrieve the chat history from Redis and return it as a string formatted for ingestion

    Args:
        session_id (str): The session id.
        url (str): The url of the Redis server.
        key_prefix (str): The key prefix for the chat history.
        chat_history_length (int): The length of the chat history.

    Returns:
        str: The chat history as a string.
    """

    history = RedisChatMessageHistoryWindowed(
        session_id=session_id,
        url=url,
        key_prefix=key_prefix,
        chat_history_length=chat_history_length,
    )
    conversation = ""
    for message in history.messages:
        if message.type == "human":
            text = "Human: " + message.content
        elif message.type == "ai":
            text = "AI: " + message.content
        conversation += text + "\n"
    return conversation
