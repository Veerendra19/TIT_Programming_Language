# shell.py — Polished TIT REPL

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import main  # Your TIT interpreter logic

# TIT built-in command keywords (add more if needed)
tit_completer = WordCompleter([
    "GEN_TEXT", "GEN_IMAGE", "SUMMARIZE", "exit", "help"
], ignore_case=True)

# Custom color style for the shell
style = Style.from_dict({
    'prompt': '#00ffff bold',
    '': '#ffffff'
})

# Create an interactive prompt session with history and autocompletion
session = PromptSession(
    message=[('class:prompt', 'TIT (v.0.1.0) >>>> ')],
    history=FileHistory('.tit_history'),
    completer=tit_completer,
    style=style
)

def start_repl():
    print("Welcome to TIT Language Shell v.0.1.0")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            with patch_stdout():
                text = session.prompt()
            if text.strip() == "":
                continue
            if text.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            result, error = main.run('<stdin>', text)

            if error:
                print(error.as_string())
            elif result:
                if hasattr(result, "elements") and len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt. Type 'exit' to quit.")
            continue
        except EOFError:
            print("\nEOF received. Exiting.")
            break
        except Exception as e:
            print(f"[REPL Error] {e}")

if __name__ == "__main__":
    start_repl()
