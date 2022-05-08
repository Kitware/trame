import os
from trame import state
from trame.layouts import SinglePageWithDrawer
from trame.html import simput, vuetify

from simput.core import ProxyManager, UIManager
from simput.ui.web import VuetifyResolver

# -----------------------------------------------------------------------------
# SimPut initialization
# -----------------------------------------------------------------------------

pxm = ProxyManager()
ui_resolver = VuetifyResolver()
ui_manager = UIManager(pxm, ui_resolver)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
pxm.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))


@state.change("lang")
def update_lang(lang, **kwargs):
    file_path = os.path.join(BASE_DIR, f"model/lang/{lang}.yaml")
    ui_manager.load_language(yaml_file=file_path)


def update_list():
    ids = list(map(lambda p: p.id, pxm.get_instances_of_type("Person")))
    state.person_ids = ids


def create_person():
    person = pxm.create("Person")
    state.active_id = person.id
    update_list()


def delete_person():
    pxm.delete(state.active_id)
    state.active_id = None
    update_list()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_simput = simput.Simput(ui_manager, prefix="ab")

layout = SinglePageWithDrawer("Simput", on_ready=update_lang)
layout.logo.children = [vuetify.VIcon("mdi-database")]
layout.title.set_text("SimPut Address Book")
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

with layout.toolbar:
    vuetify.VSpacer()
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
    )
    vuetify.VSwitch(
        classes="mx-2",
        v_model="abAutoApply",
        label="Apply",
        **compact_styles,
    )
    with vuetify.VBtn(
        **btn_styles,
        disabled=["!abChangeSet"],
        click=html_simput.apply,
    ):
        with vuetify.VBadge(
            content=["abChangeSet"],
            offset_x=8,
            offset_y=8,
            value=["abChangeSet"],
        ):
            vuetify.VIcon("mdi-database-import")

    with vuetify.VBtn(
        **btn_styles,
        disabled=["!abChangeSet"],
        click=html_simput.reset,
    ):
        vuetify.VIcon("mdi-undo-variant")

    vuetify.VDivider(vertical=True, classes="mx-2")
    with vuetify.VBtn(
        **btn_styles,
        disabled=("!active_id",),
        click=delete_person,
    ):
        vuetify.VIcon("mdi-minus")

    with vuetify.VBtn(click=create_person, **btn_styles):
        vuetify.VIcon("mdi-plus")

with layout.drawer:
    with vuetify.VList(**compact_styles):
        with vuetify.VListItemGroup(v_model="active_id", color="primary"):
            with vuetify.VListItem(
                v_for="(id, i) in person_ids",
                key="i",
                value=["id"],
            ):
                with vuetify.VListItemContent():
                    with vuetify.VListItemTitle():
                        simput.SimputItem(
                            "{{FirstName}} {{LastName}}",
                            itemId="id",
                            no_ui=True,
                            extract=["FirstName", "LastName"],
                        )

with layout.content:
    with vuetify.VContainer(fluid=True):
        simput.SimputItem(itemId=("active_id", None))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    update_list()
    layout.start()
