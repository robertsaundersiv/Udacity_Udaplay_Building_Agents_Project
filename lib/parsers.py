import json
from typing import Any, Generic, Type, TypeVar
from abc import ABC, abstractmethod
from pydantic import BaseModel

from lib.messages import AIMessage


ModelT = TypeVar("ModelT", bound=BaseModel)


def _require_content(ai_message: AIMessage) -> str:
    if ai_message.content is None:
        raise ValueError("AI message has no content to parse.")
    return ai_message.content


class OutputParser(BaseModel, ABC):
    @abstractmethod
    def parse(self, ai_message: AIMessage) -> Any:
        pass


class StrOutputParser(OutputParser):
    def parse(self, ai_message: AIMessage) -> str:
        return ai_message.content or ""


class ToolOutputParser(BaseModel):
    def parse(self, ai_message: AIMessage) -> list[dict]:
        return [{
            "tool_call_id":call.id,
            "args":json.loads(call.function.arguments),
            "function_name": call.function.name,
        } for call in ai_message.tool_calls or []]


class JsonOutputParser(OutputParser):
    def parse(self, ai_message: AIMessage) -> Any:
        return json.loads(_require_content(ai_message))


class PydanticOutputParser(OutputParser, Generic[ModelT]):
    model_class: Type[ModelT]

    def parse(self, ai_message: AIMessage) -> ModelT:
        return self.model_class.model_validate_json(_require_content(ai_message))
