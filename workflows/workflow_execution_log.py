from pathlib import Path
from datetime import datetime
import re
import sys

# Matches ANSI escape sequences (color codes like \x1b[36m) emitted by `rich`
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Matches Unicode Box-Drawing characters (e.g., │, ╭, ─, ╰) used for UI borders
BOX_DRAWING_PATTERN = re.compile(r'[\u2500-\u257F]+')

def clean_log_text(text: str) -> str:
    """Remove ANSI escape sequences and box-drawing characters from text."""
    # Strip color codes and formatting
    text_no_ansi = ANSI_ESCAPE_PATTERN.sub("", text)
    # Strip the vertical/horizontal lines and corners
    clean_text = BOX_DRAWING_PATTERN.sub("", text_no_ansi)
    return clean_text

class TeeStream:
    def __init__(self, terminal, file):
        self.terminal = terminal
        self.file = file

    def write(self, message):
        self.terminal.write(message)
        # Apply the updated clean_log_text function to the file output
        self.file.write(clean_log_text(message))
        self.file.flush()

    def flush(self):
        self.terminal.flush()
        self.file.flush()

class WorkflowExecutionLogger:
    def __init__(self, workflow_id: str):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.path = (
            self.log_dir
            / f"workflow_{workflow_id}_{timestamp}.log"
        )

        self.file = None
        self.original_stdout = None
        self.original_stderr = None

    def start_capture(self):
        self.file = self.path.open(
            "a",
            encoding="utf-8",
        )

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        sys.stdout = TeeStream(
            self.original_stdout,
            self.file,
        )

        sys.stderr = TeeStream(
            self.original_stderr,
            self.file,
        )

    def stop_capture(self):
        if self.original_stdout is not None:
            sys.stdout = self.original_stdout

        if self.original_stderr is not None:
            sys.stderr = self.original_stderr

        if self.file is not None:
            self.file.close()
            self.file = None

    def log(self, message: str):
        print(message)

    def separator(self):
        self.log(
            "\n" + "-" * 70
        )