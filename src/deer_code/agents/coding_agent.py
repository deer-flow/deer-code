import os

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langgraph.checkpoint.base import RunnableConfig

from deer_code.models import init_chat_model
from deer_code.project import project
from deer_code.prompts import apply_prompt_template
from deer_code.tools import (
    bash_tool,
    grep_tool,
    ls_tool,
    text_editor_tool,
    todo_write_tool,
    tree_tool,
)


def create_coding_agent(plugin_tools: list[BaseTool] = [], **kwargs):
    """Create a coding agent.

    Args:
        plugin_tools: Additional tools to add to the agent.
        **kwargs: Additional keyword arguments to pass to the agent.

    Returns:
        The coding agent.
    """
    return create_agent(
        model=init_chat_model(),
        tools=[
            bash_tool,
            grep_tool,
            ls_tool,
            text_editor_tool,
            todo_write_tool,
            tree_tool,
            *plugin_tools,
        ],
        system_prompt=apply_prompt_template(
            "coding_agent", PROJECT_ROOT=project.root_dir
        ),
        name="coding_agent",
        **kwargs,
    )


def create_coding_agent_for_debug(config: RunnableConfig):
    project.root_dir = os.getenv("PROJECT_ROOT", os.getcwd())
    return create_coding_agent(debug=True)
