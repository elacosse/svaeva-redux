import logging

import dotenv
import numpy as np
from redis_om import Migrator
from redis_om.model.model import NotFoundError

from svaeva_redux.prompts.consonancia import lm_system_prompt as lm_system_prompt_consonancia
from svaeva_redux.prompts.consonancia import vlm_system_prompt as vlm_system_prompt_consonancia
from svaeva_redux.schemas.redis import ConversationModel, UserImageModel, UserModel

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
dotenv.load_dotenv(dotenv.find_dotenv())


def initialize_redis():
    default_0 = {
        "name": "default_0",
        "chain_type": "chain_with_history",
        "chat_history_length": 30,
        "lm_system_prompt": "You are a helpful assistant.",
        "vlm_system_prompt": "Tell me what this image is.",
        "engine": "gpt-4",
        "engine_type": "openai",
        "temperature": 0.5,
        "max_tokens": 150,
        "model_token_limit": 8192,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "author": "master",
    }

    default_1 = {
        "name": "default_1",
        "chain_type": "chain_with_history",
        "chat_history_length": 30,
        "lm_system_prompt": "You are a helpful assistant.",
        "vlm_system_prompt": "Tell me what this image isn't is.",
        "engine": "gpt-4",
        "engine_type": "openai",
        "temperature": 0.5,
        "max_tokens": 150,
        "model_token_limit": 8192,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "author": "master",
    }

    consonancia = {
        "name": "consonancia",
        "chain_type": "chain_with_history",
        "chat_history_length": 30,
        "lm_system_prompt": lm_system_prompt_consonancia,
        "vlm_system_prompt": vlm_system_prompt_consonancia,
        "engine": "gpt-4",
        "engine_type": "openai",
        "temperature": 0.5,
        "max_tokens": 150,
        "model_token_limit": 8192,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "author": "master",
    }
    # Create a RediSearch index
    Migrator().run()
    ConversationModel(**default_0).save()
    ConversationModel(**default_1).save()
    ConversationModel(**consonancia).save()

    # Find All ConversationRedisModels
    models = ConversationModel.find((ConversationModel.chain_type == "chain_with_history")).all()
    models = sorted(models, key=lambda x: x.date_created_timestamp)
    logger.info("Initialized ConversationRedisModels: ", [model.name for model in models])


def update_user_avatar(user_id: str, image_bytes: bytes, image_prompt: str = ""):
    # Update user avatars
    try:
        user = UserImageModel.get(user_id)
    except Exception as e:
        if isinstance(e, NotFoundError):
            user = UserImageModel(id=user_id)
            user.save()
    try:
        if user.avatar_image_bytes is not None and user.avatar_image_prompt is not None:
            user.avatar_image_bytes_history.append(user.avatar_image_bytes)
            user.avatar_image_prompt_history.append(user.avatar_image_prompt)
        user.avatar_image_bytes = image_bytes
        user.avatar_image_prompt = image_prompt
        user.save()
        logger.info(f"Updated UserImageModel image id: {user_id}")
    except Exception as e:
        logger.error(f"Failed to update user avatar: {e}")


async def async_update_user_avatar(user_id: str, image_bytes: bytes, image_prompt: str = ""):
    # Update user avatars
    try:
        user = UserImageModel.get(user_id)
    except Exception as e:
        if isinstance(e, NotFoundError):
            user = UserImageModel(id=user_id)
            user.save()
    try:
        user.avatar_image_bytes = image_bytes
        user.avatar_image_prompt = image_prompt
        if user.avatar_image_bytes is not None and user.avatar_image_prompt is not None:
            user.avatar_image_bytes_history.append(image_bytes)
            user.avatar_image_prompt_history.append(image_prompt)
        user.save()
        logger.info(f"Updated UserImageModel image id: {user_id}")
    except Exception as e:
        logger.error(f"Failed to update user avatar: {e}")


def update_user_conversation_embedding(user_id: str, embedding_array: np.ndarray) -> None:
    """Update the conversation embedding for a user.

    Args:
        user_id (str): The user ID.
        embedding_array (np.ndarray): The conversation embedding array.

    Returns:
        None
    """

    try:
        user = UserModel.get(user_id)
        user.conversation_embedding = embedding_array
        user.save()
        logger.info(f"Updated UserModel embedding id: {user_id}")
    except Exception as e:
        logger.error(f"Failed to update user conversation embedding: {e}")


async def async_update_user_conversation_embedding(user_id: str, embedding_array: np.ndarray) -> None:
    """Asyncio update the conversation embedding for a user.

    Args:
        user_id (str): The user ID.
        embedding_array (np.ndarray): The conversation embedding array.

    Returns:
        None
    """
    try:
        user = UserModel.get(user_id)
        user.conversation_embedding = embedding_array
        user.save()
        logger.info(f"Updated UserModel embedding id: {user_id}")
    except Exception as e:
        logger.error(f"Failed to update user avatar: {e}")
