import os
from trame import start, change, update_state, get_state
from trame.layouts import SinglePageWithDrawer
from trame.html import simput, vuetify

from simput.core import ObjectManager, UIManager
from simput.ui.web import VuetifyResolver
from simput.pywebvue.modules import SimPut

# -----------------------------------------------------------------------------
# SimPut initialization
# -----------------------------------------------------------------------------

obj_manager = ObjectManager()
ui_resolver = VuetifyResolver()
ui_manager = UIManager(obj_manager, ui_resolver)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
obj_manager.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))


@change("lang")
def update_lang(lang, **kwargs):
    file_path = os.path.join(BASE_DIR, f"model/lang/{lang}.yaml")
    ui_manager.load_language(yaml_file=file_path)


def update_list():
    ids = list(map(lambda p: p.get("id"), obj_manager.get_type("Person")))
    update_state("person_ids", ids)


def create_person():
    person = obj_manager.create("Person")
    update_state("active_id", person.get("id"))
    update_list()


def delete_person():
    (id_to_delete,) = get_state("active_id")
    obj_manager.delete(id_to_delete)
    update_state("active_id", None)
    update_list()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_simput = simput.Simput(ui_manager, prefix="ab")

layout = SinglePageWithDrawer("Trame/Simput")
layout.logo.content = "mdi-database"
layout.title.content = "SimPut Address Book"
layout.root = html_simput

btn_styles = {
    "classes": "mx-2",
    "small": True,
    "outlined": True,
    "icon": True,
}

compact_styles = {
    "hide_details": True,
    "dense": True,
}

layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VSelect(
        v_model=("lang", "en"),
        items=(
            "options",
            [
                {"text": "English", "value": "en"},
                {"text": "Francais", "value": "fr"},
            ],
        ),
        **compact_styles,
    ),
    vuetify.VSwitch(
        classes="mx-2",
        v_model="abAutoApply",
        label="Apply",
        **compact_styles,
    ),
    vuetify.VBtn(
        **btn_styles,
        disabled=["!abChangeSet"],
        click=html_simput.apply,
        children=[
            vuetify.VBadge(
                content=["abChangeSet"],
                offset_x=8,
                offset_y=8,
                value=["abChangeSet"],
                children=[vuetify.VIcon("mdi-database-import")],
            )
        ],
    ),
    vuetify.VBtn(
        **btn_styles,
        disabled=["!abChangeSet"],
        click=html_simput.reset,
        children=[vuetify.VIcon("mdi-undo-variant")],
    ),
    vuetify.VDivider(vertical=True, classes="mx-2"),
    vuetify.VBtn(
        **btn_styles,
        disabled=["!active_id"],
        click=delete_person,
        children=[vuetify.VIcon("mdi-minus")],
    ),
    vuetify.VBtn(
        **btn_styles,
        click=create_person,
        children=[vuetify.VIcon("mdi-plus")],
    ),
]
layout.drawer.children += [
    vuetify.VList(
        **compact_styles,
        children=[
            vuetify.VListItemGroup(
                v_model="active_id",
                color="primary",
                children=[
                    vuetify.VListItem(
                        v_for="(id, i) in person_ids",
                        key="i",
                        value=["id"],
                        children=[
                            vuetify.VListItemContent(
                                vuetify.VListItemTitle(
                                    simput.SimputItem(
                                        "{{FirstName}} {{LastName}}",
                                        itemId="id",
                                        no_ui=True,
                                        extract=["FirstName", "LastName"],
                                    )
                                )
                            )
                        ],
                    )
                ],
            )
        ],
    )
]
layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        children=[
            simput.SimputItem(itemId="active_id"),
        ],
    )
]

layout.state = {
    "active_id": None,
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    update_list()
    start(layout, on_ready=update_lang)
