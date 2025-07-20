import json
from typing import Any, Type
from abc import ABC, abstractmethod
try:
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - fallback when pydantic is missing
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

from lib.messages import AIMessage


class OutputParser(BaseModel, ABC):
    @abstractmethod
    def parse(self, ai_message: AIMessage) -> Any:
        pass


class StrOutputParser(OutputParser):
    def parse(self, ai_message: AIMessage) -> str:
        return ai_message.content


class ToolOutputParser(BaseModel):
    def parse(self, ai_message: AIMessage) -> list[dict]:
        return [{
            "tool_call_id":call.id,
            "args":json.loads(call.function.arguments),
            "function_name": call.function.name,
        } for call in ai_message.tool_calls]


class JsonOutputParser(OutputParser):
    def parse(self, ai_message: AIMessage) -> Any:
        return json.loads(ai_message.content)


class PydanticOutputParser(OutputParser):
    model_class: Type[BaseModel]

    def parse(self, ai_message: AIMessage) -> BaseModel:
        return self.model_class.model_validate_json(ai_message.content)
    