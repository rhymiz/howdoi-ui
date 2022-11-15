import asyncio

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Static
from textual_forms import TextualForm


async def query(text: str):
    cmd = ['howdoi', text]
    proc = await asyncio.create_subprocess_shell(
        cmd=' '.join(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    return stdout


class ResultStatic(Static):
    DEFAULT_CSS = """
    ResultStatic {
        padding: 1;
    }
    """
    pass


class HowDoIApp(App):
    DEFAULT_CSS = """
    TextualForm {
        height: 25%;
    }
    """
    result = reactive(None)

    async def on_textual_form_submit(self, message: TextualForm.Submit):
        parts = message.data['query'].split('|')
        show_line_numbers = False
        language = "text"
        if len(parts) > 1:
            show_line_numbers = True
            language, question = parts
        else:
            question = parts[0]
        result = await query(question)
        self.query_one(ResultStatic).update(
            Syntax(
                result.decode("utf-8"),
                language,
                line_numbers=show_line_numbers
            )
        )

    def compose(self) -> ComposeResult:
        yield TextualForm(
            form_data=[{
                "id": "query",
                "required": True,
                "placeholder": "How do I...",
                "rules": {
                    "min_length": 3
                }
            }]
        )
        yield ResultStatic()


if __name__ == '__main__':
    HowDoIApp().run()
