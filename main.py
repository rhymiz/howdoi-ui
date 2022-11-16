import asyncio

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Static
from textual_forms import Form


async def query(text: str) -> str:
    cmd = ['howdoi', text]
    proc = await asyncio.create_subprocess_shell(
        cmd=' '.join(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()
    return stdout.decode("utf-8")


class Results(Static):
    DEFAULT_CSS = """
    Results {
        padding: 1;
    }
    """


class HowDoIApp(App):
    DEFAULT_CSS = """
    Form {
        height: 25%;
    }
    """
    result = reactive(None)

    async def on_form_event(self, message: Form.Event):
        if message.event != 'search':
            return

        parts = message.data['query'].split('|')
        show_line_numbers = False
        language = "text"
        if len(parts) > 1:
            show_line_numbers = True
            language, question = parts
        else:
            question = parts[0]
        result = await query(question)
        self.query_one(Results).update(
            Syntax(
                result,
                language,
                word_wrap=True,
                line_numbers=show_line_numbers,
            )
        )

    def compose(self) -> ComposeResult:
        yield Form(
            fields=[
                {
                    "id": "query",
                    "value": "python|how to use python lru_cache decorator",
                    "required": True,
                    "placeholder": "How do I...",
                    "rules": {
                        "min_length": 3
                    }
                }
            ],
            buttons=[
                {
                    "id": "search",
                    "label": "Search",
                    "watch_form_valid": True
                }
            ]
        )
        yield Results()


if __name__ == '__main__':
    HowDoIApp().run()
