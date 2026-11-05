"""Permissions: the people running the app decide what agents may do.

Run:  python examples/10_mcp/03_permissions.py --server
      python examples/10_mcp/03_permissions.py --server --mcp-deny files

The app edits notes kept in a temporary folder. It declares two permissions,
"files" (read the notes) and "save" (write them, which requires reading), and
each tool, method or property setter that needs one says so with requires=.
While a permission is off, what needs it is left out of what agents are
offered and calls to it are refused. The checkboxes switch permissions while
the app runs; --mcp-deny (or TRAME_MCP_DENY) withholds them for the whole run.

An agent can then:
    list_notes()                                           # needs "files"
    object_call("editor", "open", {"name": "todo.txt"})    # needs "files"
    object_update("editor", {"text": "Buy milk"})
    object_update("editor", {"note": "shopping.txt"})      # needs "save"
    object_call("editor", "save")                          # needs "save"
    object_call("editor", "clear")                         # marked destructive
"""

import tempfile
from pathlib import Path

from trame.app import TrameApp
from trame.decorators import change, mcp_method, mcp_property, mcp_tool
from trame.ui.html import DivLayout
from trame.widgets import html


class NotesApp(TrameApp):
    """A text editor over a folder of notes."""

    def __init__(self, server=None):
        super().__init__(server)
        self.folder = Path(tempfile.mkdtemp(prefix="trame-notes-"))
        (self.folder / "todo.txt").write_text("Write the docs\nTry the examples\n")
        (self.folder / "ideas.txt").write_text("An agent that tidies notes\n")

        permissions = self.mcp.permissions
        permissions.declare("files", f"Read the notes in {self.folder}")
        permissions.declare(
            "save", f"Write notes in {self.folder}", requires="files", allowed=False
        )
        self.mcp.configure(name="notes", enabled=True)
        self.mcp_expose("editor")

        self.state.note = "untitled.txt"
        self.state.text = ""
        self.state.locked = []
        self._show_permissions()
        self.ctrl.on_server_ready.add(self._on_ready)
        self._build_ui()

    # -------------------------------------------------------------------------
    # What agents may use
    # -------------------------------------------------------------------------

    @mcp_tool(read_only=True, requires="files")
    def list_notes(self) -> list[str]:
        """The notes in the folder, by file name."""
        return sorted(path.name for path in self.folder.glob("*.txt"))

    @mcp_method(requires="files")
    def open(self, name: str) -> str:
        """Show a note in the editor."""
        path = self._path(name)
        if not path.exists():
            msg = f"No note {name!r}; list_notes() lists them"
            raise ValueError(msg)
        self.state.update({"note": path.name, "text": path.read_text()})
        return f"Opened {path.name}"

    @mcp_method(requires="save")
    def save(self) -> str:
        """Write the editor's text to its note."""
        self._path(self.state.note).write_text(self.state.text)
        return f"Saved {self.state.note}"

    @mcp_method(annotations={"destructiveHint": True})
    def clear(self) -> None:
        """Empty the editor. The note keeps its text until it is saved."""
        self.state.text = ""

    @mcp_property
    def text(self) -> str:
        """The text in the editor."""
        return self.state.text

    @text.setter
    def text(self, value: str):
        self.state.text = value

    @mcp_property
    def note(self) -> str:
        """The file name the editor saves to. Changing it needs "save"."""
        return self.state.note

    @note.setter(requires="save")
    def note(self, value: str):
        self.state.note = self._path(value).name

    # -------------------------------------------------------------------------
    # The app
    # -------------------------------------------------------------------------

    def _path(self, name):
        path = (self.folder / name).resolve()
        if path.parent != self.folder.resolve() or path.suffix != ".txt":
            msg = f"A note is a .txt file name, without a folder: got {name!r}"
            raise ValueError(msg)
        return path

    def _show_permissions(self):
        permissions = self.mcp.permissions
        self.state.update(
            {"allow_files": permissions["files"], "allow_save": permissions["save"]}
        )

    def _on_ready(self, **_):
        # --mcp-deny is known once the server starts: those switches stay off
        self.state.locked = list(self.mcp.permissions.locked)
        self._show_permissions()

    # "save" requires "files": switching files off switches save off too
    @change("allow_files")
    def _on_allow_files(self, allow_files, **_):
        self.mcp.permissions["files"] = allow_files
        self._show_permissions()

    @change("allow_save")
    def _on_allow_save(self, allow_save, **_):
        self.mcp.permissions["save"] = allow_save
        self._show_permissions()

    def _build_ui(self):
        with DivLayout(self.server):
            html.P(f"Notes in {self.folder}")
            # "save" can only be switched on while "files" is
            for name, label, disabled in (
                ("files", "read notes", "locked.includes('files')"),
                ("save", "save notes", "locked.includes('save') || !allow_files"),
            ):
                with html.Label(style="margin-right: 1rem"):
                    html.Input(
                        type="checkbox",
                        v_model=(f"allow_{name}",),
                        disabled=(disabled,),
                    )
                    html.Span(f"Agents may {label}")
            html.H3("{{ note }}")
            html.Textarea(v_model=("text",), rows=10, style="width: 100%")


def main():
    app = NotesApp()
    app.server.start()


if __name__ == "__main__":
    main()
