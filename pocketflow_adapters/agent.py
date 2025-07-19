"""PocketFlow adapter exposing SmolaAgents MultiStepAgent with WE tools."""

from smolagents import MultiStepAgent
from smolagents.models import LiteLLMModel

from we_we_we.agent_tools import (
    VibeSensorTool,
    SecuritySigilTool,
    MeshPingTool,
    GreetingTool,
)

# initialise on module import so skill is warm
_llm = LiteLLMModel(model_id="gpt-3.5-turbo")
_tools = [VibeSensorTool(), SecuritySigilTool(), MeshPingTool(), GreetingTool()]
_agent = MultiStepAgent(model=_llm, tools=_tools)


def invoke(payload: dict | None = None):
    task = (payload or {}).get("task", "")
    return _agent.run(task)