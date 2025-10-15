from langgraph.prebuilt import create_react_agent

from deer_code import project
from deer_code.models import create_chat_model
from deer_code.prompts.template import apply_prompt_template
from deer_code.tools import bash_tool, text_editor_tool


def create_coding_agent():
    return create_react_agent(
        model=create_chat_model(),
        tools=[bash_tool, text_editor_tool],
        prompt=apply_prompt_template("coding_agent", PROJECT_ROOT=project.root_dir),
    )


coding_agent = create_coding_agent()
