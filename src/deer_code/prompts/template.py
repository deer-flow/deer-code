import os

from jinja2 import Environment, FileSystemLoader


def apply_prompt_template(template: str, **kwargs) -> str:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    loader = FileSystemLoader(template_dir)
    env = Environment(loader=loader)
    template = env.get_template(f"{template}.md")
    return template.render(
        **kwargs,
    )
