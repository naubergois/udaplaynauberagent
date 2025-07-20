try:
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - fallback for environments without pydantic
    import json

    class BaseModel:
        """Minimal pydantic BaseModel fallback used for tests."""

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

        @classmethod
        def model_validate_json(cls, json_str: str):
            return cls(**json.loads(json_str))

        def dict(self):
            return self.__dict__
from typing import Optional, Union, List, Dict, Literal

from lib.tooling import ToolCall


class BaseMessage(BaseModel):
    role: str
    content: Optional[str] = ""

    def dict(self) -> Dict:
        return self.__dict__


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: str
    content: str = ""


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class AIMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"
    content: Optional[str] = ""
    tool_calls: Optional[List[ToolCall]] = None
    token_usage: Optional[TokenUsage] = None


AnyMessage = Union[
    SystemMessage,
    UserMessage,
    AIMessage,
    ToolMessage,
]
