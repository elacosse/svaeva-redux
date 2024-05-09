import os
import uuid
from datetime import datetime
from typing import List, Optional

import dotenv
import redis
from redis_om import (
    Field,
    JsonModel,
)

dotenv.load_dotenv(dotenv.find_dotenv())
redis_connection = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB_INDEX")),
)


class ConversationModel(JsonModel):
    name: str = Field(index=True, primary_key=True)
    chain_type: str = Field("chain_with_history", index=True)
    lm_system_prompt: str = Field("", index=True)
    vlm_system_prompt: str = Field("", index=True)
    chat_history_length: int = Field(10)
    engine: str = Field(index=True)
    engine_type: str = Field(index=True)
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(150, gt=0)
    model_token_limit: int = Field(8192, gt=0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, ge=0.0)
    presence_penalty: float = Field(0.0, ge=0.0)
    author: str = Field(index=True)
    api_key: Optional[str] = None
    date_created_timestamp: Optional[float] = Field(index=True)

    def save(self) -> None:
        self.date_created_timestamp = datetime.now().timestamp()
        super().save()

    class Meta:
        database = redis_connection


class UserModel(JsonModel):
    version: str = "1.0"
    commit: str = "commit"
    id: Optional[str] = Field(index=True, primary_key=True)
    group_id: str = Field(index=True)
    platform_id: str = Field(index=True)
    interaction_count: int = Field(0, ge=0, index=True)
    flagged: bool = Field(False, index=True)
    first_name: Optional[str] = Field(index=True)
    last_name: Optional[str] = Field(index=True)
    username: Optional[str] = Field(index=True)
    description: Optional[str] = Field(index=True)
    phone_number: Optional[str] = Field(
        index=True, regex=r"^\+?[0-9]{7,15}$", description="Phone number including country code (if applicable)"
    )
    email: Optional[str] = Field(index=True)
    register_method: Optional[str] = Field(index=True)  # typeform, CLI
    country: Optional[str] = Field(
        index=True,
        regex="^(AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BQ|BA|BW|BV|BR|IO|BN|BG|BF|BI|CV|KH|CM|CA|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CW|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|SZ|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SX|SK|SI|SB|SO|ZA|GS|SS|ES|LK|SD|SR|SJ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW)$",
        description="ISO 3166-1 alpha-2 country code",
    )
    age: Optional[int] = Field(index=True, ge=0, le=120)
    gender: Optional[str] = Field(
        regex="^(male|female|other)$",
    )
    language_code: Optional[str] = Field(index=True, description="ISO 3166-1 alpha-2 country code")
    english_proficiency: Optional[str] = Field(regex="^(A1|A2|B1|B2|C1|C2)$", description="CEFR level")
    conversation_embedding: Optional[List[float]] = Field([], index=False, description="Conversation Embedding")
    date_created_timestamp: Optional[float] = Field(index=True)
    date_updated_timestamp: Optional[float] = Field(index=True)
    date_accessed_timestamp: Optional[float] = Field(index=True)

    def save(self) -> None:
        now = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date_created_timestamp is None:
            self.date_created_timestamp = now.timestamp()
        if self.date_updated_timestamp is None:
            self.date_updated_timestamp = now.timestamp()
        if self.date_accessed_timestamp is None:
            self.date_accessed_timestamp = now.timestamp()
        super().save()

    def increment_interaction_count(self, **kwargs) -> None:
        self.interaction_count += 1
        self.date_accessed_timestamp = datetime.now().timestamp()
        super().save()

    def __getattribute__(self, name):
        object.__setattr__(self, "date_accessed", datetime.now())
        object.__setattr__(self, "date_accessed_timestamp", datetime.now().timestamp())
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value) -> None:
        object.__setattr__(self, "date_updated", datetime.now())
        object.__setattr__(self, "date_updated_timestamp", datetime.now().timestamp())
        object.__setattr__(self, name, value)

    def __str__(self):
        attributes = []
        for attribute, value in vars(self).items():
            attributes.append(f"{attribute}: {value}")
        return "\n".join(attributes)

    def __eq__(self, other) -> bool:
        for attribute, value in vars(self).items():
            if attribute == "password" or attribute == "date_accessed":
                continue
            if value != getattr(other, attribute):
                return False
        return True

    class Meta:
        database = redis_connection


class UserImageModel(JsonModel):
    version: str = "1.0"
    commit: str = "commit"
    id: Optional[str] = Field(index=True, primary_key=True)
    group_id: Optional[str] = Field(index=True)
    platform_id: Optional[str] = Field(index=True)
    avatar_image_bytes: Optional[bytes] = Field(index=False, description="Avatar Image")
    avatar_image_prompt: Optional[str] = Field(index=False, description="Avatar Image Prompt")
    avatar_image_bytes_history: Optional[List[bytes]] = Field([], index=False, description="Avatar Image History")
    avatar_image_prompt_history: Optional[List[str]] = Field([], index=False, description="Avatar Image Prompt History")
    date_created_timestamp: Optional[float] = Field(index=True)
    date_updated_timestamp: Optional[float] = Field(index=True)
    date_accessed_timestamp: Optional[float] = Field(index=True)

    def save(self) -> None:
        now = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date_created_timestamp is None:
            self.date_created_timestamp = now.timestamp()
        if self.date_updated_timestamp is None:
            self.date_updated_timestamp = now.timestamp()
        if self.date_accessed_timestamp is None:
            self.date_accessed_timestamp = now.timestamp()
        super().save()

    def __getattribute__(self, name):
        object.__setattr__(self, "date_accessed", datetime.now())
        object.__setattr__(self, "date_accessed_timestamp", datetime.now().timestamp())
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value) -> None:
        object.__setattr__(self, "date_updated", datetime.now())
        object.__setattr__(self, "date_updated_timestamp", datetime.now().timestamp())
        object.__setattr__(self, name, value)

    def __str__(self):
        attributes = []
        for attribute, value in vars(self).items():
            attributes.append(f"{attribute}: {value}")
        return "\n".join(attributes)

    def __eq__(self, other) -> bool:
        for attribute, value in vars(self).items():
            if attribute == "password" or attribute == "date_accessed":
                continue
            if value != getattr(other, attribute):
                return False
        return True

    class Meta:
        database = redis_connection


class UserVideoModel(JsonModel):
    version: str = "1.0"
    commit: str = "commit"
    id: Optional[str] = Field(index=True, primary_key=True)
    group_id: Optional[str] = Field(index=True)
    platform_id: Optional[str] = Field(index=True)
    avatar_video_bytes: Optional[List[bytes]] = Field(index=False, description="Avatar Video")
    date_created_timestamp: Optional[float] = Field(index=True)
    date_updated_timestamp: Optional[float] = Field(index=True)
    date_accessed_timestamp: Optional[float] = Field(index=True)

    def save(self) -> None:
        now = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date_created_timestamp is None:
            self.date_created_timestamp = now.timestamp()
        if self.date_updated_timestamp is None:
            self.date_updated_timestamp = now.timestamp()
        if self.date_accessed_timestamp is None:
            self.date_accessed_timestamp = now.timestamp()
        super().save()

    def __getattribute__(self, name):
        object.__setattr__(self, "date_accessed", datetime.now())
        object.__setattr__(self, "date_accessed_timestamp", datetime.now().timestamp())
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value) -> None:
        object.__setattr__(self, "date_updated", datetime.now())
        object.__setattr__(self, "date_updated_timestamp", datetime.now().timestamp())
        object.__setattr__(self, name, value)

    def __str__(self):
        attributes = []
        for attribute, value in vars(self).items():
            attributes.append(f"{attribute}: {value}")
        return "\n".join(attributes)

    def __eq__(self, other) -> bool:
        for attribute, value in vars(self).items():
            if attribute == "password" or attribute == "date_accessed":
                continue
            if value != getattr(other, attribute):
                return False
        return True

    class Meta:
        database = redis_connection
