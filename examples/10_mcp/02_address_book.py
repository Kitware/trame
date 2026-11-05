"""An address book of trame-dataclass models, driven by agents.

Run:  python examples/10_mcp/02_address_book.py --server
Deps: pip install trame-dataclass

An agent can then:
    object_types()
    object_get("address_book")
    object_call("address_book", "add_contact", {"name": "Grace", "age": 36})
    object_update("<person id>", {"age": 37})
    object_batch([
        {"new": "Person", "args": {"name": "Alan", "age": 41}, "as": "alan"},
        {"call": "address_book", "method": "add", "args": {"person": "@alan"}},
    ])
"""

from trame.app import TrameApp
from trame.decorators import mcp
from trame.ui.html import DivLayout
from trame.widgets import html
from trame_dataclass.v2 import ServerOnly, StateDataModel, Sync


class Person(StateDataModel):
    """A contact in the address book."""

    name = Sync(str, "", mcp={"description": "Full name", "schema": {"minLength": 1}})
    age = Sync(
        int,
        0,
        mcp={"description": "Age in years", "schema": {"minimum": 0, "maximum": 150}},
    )
    notes = ServerOnly(str)  # not marked: agents never see it

    @mcp.constructor(description="A new person, in no address book yet")
    @classmethod
    def new(cls, server, name: str, age: int = 0) -> "Person":
        return cls(server, name=name, age=age)

    @mcp.method
    def celebrate_birthday(self) -> str:
        """Increment this person's age by one year."""
        self.age += 1
        return f"{self.name} is now {self.age}"

    @mcp.method(read_only=True)
    def summary(self) -> str:
        """One-line description of this contact."""
        return f"{self.name}, {self.age}"


class AddressBook(StateDataModel, mcp=True):  # every field, by mode
    title = Sync(str, "My contacts", mcp="Title shown above the list")
    contacts = Sync(list[Person], list, has_dataclass=True)

    @mcp.method
    def add_contact(self, name: str, age: int = 0) -> Person:
        """Create a new contact and add it to the book."""
        person = Person(self.server, name=name, age=age)
        self.contacts = [*self.contacts, person]
        return person

    @mcp.method
    def add(self, person: Person) -> None:
        """Add an existing person to the book."""
        self.contacts = [*self.contacts, person]

    @mcp.method
    def remove(self, person: Person) -> None:
        """Remove a contact from the book."""
        self.contacts = [p for p in self.contacts if p is not person]


class ContactsApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.mcp.configure(name="address-book", enabled=True)
        self.book = AddressBook(self.server)
        self.book.contacts = [Person(self.server, name="Ada", age=36)]
        self.book.mcp_expose("address_book")
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server):
            with self.book.provide_as("book"):
                html.H1("{{ book.title }}")
                html.Div(
                    "{{ contact.name }} ({{ contact.age }})",
                    v_for="contact in book.contacts",
                    key="contact._id",
                )


def main():
    app = ContactsApp()
    app.server.start()


if __name__ == "__main__":
    main()
