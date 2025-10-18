from langchain.agents import create_agent

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


def create_coding_agent():
    return create_agent(
        model=init_chat_model(),
        tools=[
            bash_tool,
            grep_tool,
            ls_tool,
            text_editor_tool,
            todo_write_tool,
            tree_tool,
        ],
        system_prompt=apply_prompt_template(
            "coding_agent", PROJECT_ROOT=project.root_dir
        ),
        name="coding_agent",
    )


coding_agent = create_coding_agent()
