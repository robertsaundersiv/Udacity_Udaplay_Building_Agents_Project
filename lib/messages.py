from pydantic import BaseModel
from typing import Any, Optional, Union, List, Dict, Literal

from lib.tooling import ToolCall


class BaseMessage(BaseModel):
    # Each subclass declares its own `role` literal
    content: Optional[str] = ""

    def to_dict(self) -> Dict[str, Any]:
        return dict(self)


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: str


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
