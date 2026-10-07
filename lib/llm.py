from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel
from openai import OpenAI
from lib.messages import (
    TokenUsage,
    AIMessage,
    BaseMessage,
    UserMessage,
)
from lib.tooling import Tool, ToolCall


class LLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        tools: Optional[List[Tool]] = None,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in (tools or [])
        }

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [m.to_dict() for m in messages],
        }

        if self.tools:
            payload["tools"] = [tool.dict() for tool in self.tools.values()]
            payload["tool_choice"] = "auto"
            # One tool call per turn, so each tool can use the previous tool's result
            payload["parallel_tool_calls"] = False

        return payload

    def _convert_input(self, input: Any) -> List[BaseMessage]:
        if isinstance(input, str):
            return [UserMessage(content=input)]
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            return input
        else:
            raise ValueError(f"Invalid input type {type(input)}.")

    def invoke(self, 
               input: str | BaseMessage | List[BaseMessage],
               response_format: Optional[Type[BaseModel]] = None,) -> AIMessage:
        messages = self._convert_input(input)
        payload = self._build_payload(messages)
        if response_format:
            payload.update({"response_format": response_format})
            response = self.client.beta.chat.completions.parse(**payload)
        else:
            response = self.client.chat.completions.create(**payload)
        choice = response.choices[0]
        message = choice.message

        token_usage = None
        if response.usage:
            token_usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            )

        # Only function tools are registered, so keep just the function tool calls
        tool_calls = None
        if message.tool_calls is not None:
            tool_calls = [call for call in message.tool_calls if isinstance(call, ToolCall)]

        return AIMessage(
            content=message.content,
            tool_calls=tool_calls,
            token_usage=token_usage
        )
