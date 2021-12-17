from trame.internal.app import get_app_instance
from trame.html import AbstractElement, Template

try:
    import numpy as np
    from numbers import Number
except:
    # dataframe_to_grid won't work
    pass

# Make sure used module is available
_app = get_app_instance()
if "vuetify" not in _app.vue_use:
    _app.vue_use += ["vuetify"]

type_mapper = {
    "b": ["textColumn"],
    "i": [],  # ["numericColumn", "numberColumnFilter"],
    "u": [],  # ["numericColumn", "numberColumnFilter"],
    "f": [],  # ["numericColumn", "numberColumnFilter"],
    "c": [],
    "m": [],  # ['timedeltaFormat'],
    "M": [],  # ["dateColumnFilter", "shortDateTimeFormat"],
    "O": [],
    "S": [],
    "U": [],
    "V": [],
}


def cast_to_serializable(value):
    isoformat = getattr(value, "isoformat", None)
    if (isoformat) and callable(isoformat):
        return isoformat()
    elif isinstance(value, Number):
        if np.isnan(value) or np.isinf(value):
            return value.__str__()
        return value

    return value.__str__()


def dataframe_to_grid(dataframe, options={}):
    """
    Transform a dataframe for use with a VDataTable

    :param dataframe: A pandas dataframe
    :param options: Control which columns are sortable, filterable, grouped, aligned, etc. A dictionary where keys are the columns from the dataframe and values are Vuetify DataTableHeader objects. See more info |header_doc_link|.

    .. |header_doc_link| raw:: html

        <a href="https://vuetifyjs.com/en/api/v-data-table/#props-headers" target="_blank">here</a>

    >>> headers, rows = vuetify.dataframe_to_grid(dataframe)
    >>> VDataTable(
    ...     headers=("table_headers", headers),
    ...     items=("table_rows", rows))
    """
    headers = {}
    for col_name in dataframe.columns:
        headers[col_name] = {"text": col_name, "value": col_name}
        if options.get(col_name):
            headers[col_name].update(options.get(col_name))

    return list(headers.values()), dataframe.applymap(cast_to_serializable).to_dict(
        orient="records"
    )


slot_names = [
    "counter",
    "day-body",
    "body",
    "placeholder",
    "divider",
    "input",
    "item",
    "thumb-label",
    "item.data-table-expand",
    "prepend",
    "append-outer",
    "day-month",
    "footer",
    "footer.prepend",
    "badge",
    "loading",
    "prev",
    "header.<name>",
    "group",
    "close",
    "group.header",
    "group.summary",
    "foot",
    "progress",
    "append",
    "message",
    "expanded-item",
    "no-data",
    "default",
    "loader",
    "item.<name>",
    "header",
    "day-header",
    "event",
    "prependIcon",
    "interval",
    "img",
    "appendIcon",
    "header.data-table-select",
    "footer.page-text",
    "day",
    "day-label-header",
    "selection",
    "append-item",
    "day-label",
    "next",
    "body.append",
    "opposite",
    "prepend-item",
    "category",
    "action",
    "extension",
    "prepend-inner",
    "body.prepend",
    "actions",
    "label",
    "activator",
    "no-results",
    "item.data-table-select",
    "top",
    "page-text",
    "icon",
]
Template.slot_names.update(slot_names)


class VApp(AbstractElement):

    """
    Vuetify's VApp component. See more info and examples |VApp_vuetify_link|.

    .. |VApp_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app" target="_blank">here</a>


    :param id: Sets the DOM id on the component
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-app", children, **kwargs)
        self._attr_names += [
            "id",
        ]


class VAppBar(AbstractElement):

    """
    Vuetify's VAppBar component. See more info and examples |VAppBar_vuetify_link|.

    .. |VAppBar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app-bar" target="_blank">here</a>


    :param absolute: Applies position: absolute to the component.
    :type boolean:
    :param app: See description |VAppBar_vuetify_link|.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param clipped_left: Designates that the application's `v-navigation-drawer` that is positioned on the left is below the app-bar.
    :type boolean:
    :param clipped_right: Designates that the application's `v-navigation-drawer` that is positioned on the right is below the app-bar.
    :type boolean:
    :param collapse: Puts the toolbar into a collapsed state reducing its maximum width.
    :type boolean:
    :param collapse_on_scroll: Puts the app-bar into a collapsed state when scrolling.
    :type boolean:
    :param color: See description |VAppBar_vuetify_link|.
    :type string:
    :param dark: See description |VAppBar_vuetify_link|.
    :type boolean:
    :param dense: Reduces the height of the toolbar content to 48px (96px when using the **prominent** prop).
    :type boolean:
    :param elevate_on_scroll: Elevates the app-bar when scrolling.
    :type boolean:
    :param elevation: See description |VAppBar_vuetify_link|.
    :type ['number', 'string']:
    :param extended: Use this prop to increase the height of the toolbar _without_ using the `extension` slot for adding content. May be used in conjunction with the **extension-height** prop, and any of the other props that affect the height of the toolbar, e.g. **prominent**, **dense**, etc., **WITH THE EXCEPTION** of **height**.
    :type boolean:
    :param extension_height: Specify an explicit height for the `extension` slot.
    :type ['number', 'string']:
    :param fade_img_on_scroll: When using the **src** prop or `img` slot, will fade the image when scrolling.
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param flat: Removes the toolbar's box-shadow.
    :type boolean:
    :param floating: Applies **display: inline-flex** to the component.
    :type boolean:
    :param height: Designates a specific height for the toolbar. Overrides the heights imposed by other props, e.g. **prominent**, **dense**, **extended**, etc.
    :type ['number', 'string']:
    :param hide_on_scroll: Hides the app-bar when scrolling. Will still show the `extension` slot.
    :type boolean:
    :param inverted_scroll: Hides the app-bar when scrolling down and displays it when scrolling up.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param prominent: Increases the height of the toolbar content to 128px.
    :type boolean:
    :param rounded: See description |VAppBar_vuetify_link|.
    :type ['boolean', 'string']:
    :param scroll_off_screen: Hides the app-bar when scrolling. Will **NOT** show the `extension` slot.
    :type boolean:
    :param scroll_target: Designates the element to target for scrolling events. Uses `window` by default.
    :type string:
    :param scroll_threshold: The amount of scroll distance down before **hide-on-scroll** activates.
    :type ['string', 'number']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param short: Reduce the height of the toolbar content to 56px (112px when using the **prominent** prop).
    :type boolean:
    :param shrink_on_scroll: Shrinks a **prominent** toolbar to a **dense** or **short** (default) one when scrolling.
    :type boolean:
    :param src: Image source. See `v-img` for details
    :type ['string', 'object']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param value: Controls whether the component is visible or hidden.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-app-bar", children, **kwargs)
        self._attr_names += [
            "absolute",
            "app",
            "bottom",
            "clipped_left",
            "clipped_right",
            "collapse",
            "collapse_on_scroll",
            "color",
            "dark",
            "dense",
            "elevate_on_scroll",
            "elevation",
            "extended",
            "extension_height",
            "fade_img_on_scroll",
            "fixed",
            "flat",
            "floating",
            "height",
            "hide_on_scroll",
            "inverted_scroll",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "outlined",
            "prominent",
            "rounded",
            "scroll_off_screen",
            "scroll_target",
            "scroll_threshold",
            "shaped",
            "short",
            "shrink_on_scroll",
            "src",
            "tag",
            "tile",
            "value",
            "width",
        ]


class VAppBarNavIcon(AbstractElement):

    """
    Vuetify's VAppBarNavIcon component. See more info and examples |VAppBarNavIcon_vuetify_link|.

    .. |VAppBarNavIcon_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app-bar-nav-icon" target="_blank">here</a>



    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-app-bar-nav-icon", children, **kwargs)


class VAppBarTitle(AbstractElement):

    """
    Vuetify's VAppBarTitle component. See more info and examples |VAppBarTitle_vuetify_link|.

    .. |VAppBarTitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app-bar-title" target="_blank">here</a>



    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-app-bar-title", children, **kwargs)


class VAlert(AbstractElement):

    """
    Vuetify's VAlert component. See more info and examples |VAlert_vuetify_link|.

    .. |VAlert_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-alert" target="_blank">here</a>


    :param border: Puts a border on the alert. Accepts **top** \| **right** \| **bottom** \| **left**.
    :type string:
    :param close_icon: Change the default icon used for **dismissible** alerts.
    :type string:
    :param close_label: See description |VAlert_vuetify_link|.
    :type string:
    :param color: See description |VAlert_vuetify_link|.
    :type string:
    :param colored_border: Applies the defined **color** to the alert's border.
    :type boolean:
    :param dark: See description |VAlert_vuetify_link|.
    :type boolean:
    :param dense: Decreases component's height.
    :type boolean:
    :param dismissible: Adds a close icon that can hide the alert.
    :type boolean:
    :param elevation: See description |VAlert_vuetify_link|.
    :type ['number', 'string']:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param icon: Designates a specific icon.
    :type ['boolean', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param mode: See description |VAlert_vuetify_link|.
    :type string:
    :param origin: See description |VAlert_vuetify_link|.
    :type string:
    :param outlined: Makes the background transparent and applies a thin border.
    :type boolean:
    :param prominent: Displays a larger vertically centered icon to draw more attention.
    :type boolean:
    :param rounded: See description |VAlert_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param text: Applies the defined **color** to text and a low opacity background of the same.
    :type boolean:
    :param tile: Removes the component's border-radius.
    :type boolean:
    :param transition: See description |VAlert_vuetify_link|.
    :type string:
    :param type: Specify a **success**, **info**, **warning** or **error** alert. Uses the contextual color and has a pre-defined icon.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param input: The updated bound model
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-alert", children, **kwargs)
        self._attr_names += [
            "border",
            "close_icon",
            "close_label",
            "color",
            "colored_border",
            "dark",
            "dense",
            "dismissible",
            "elevation",
            "height",
            "icon",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "mode",
            "origin",
            "outlined",
            "prominent",
            "rounded",
            "shaped",
            "tag",
            "text",
            "tile",
            "transition",
            "type",
            "value",
            "width",
        ]
        self._event_names += [
            "input",
        ]


class VAutocomplete(AbstractElement):

    """
    Vuetify's VAutocomplete component. See more info and examples |VAutocomplete_vuetify_link|.

    .. |VAutocomplete_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-autocomplete" target="_blank">here</a>


    :param allow_overflow: Allow the menu to overflow off the screen
    :type boolean:
    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param auto_select_first: When searching, will always highlight the first option
    :type boolean:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param cache_items: Keeps a local _unique_ copy of all items that have been passed through the **items** prop.
    :type boolean:
    :param chips: Changes display of selections to chips
    :type boolean:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VAutocomplete_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VAutocomplete_vuetify_link|.
    :type boolean:
    :param deletable_chips: Adds a remove icon to selected chips
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disable_lookup: Disables keyboard lookup
    :type boolean:
    :param disabled: Disables the input
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param filter: See description |VAutocomplete_vuetify_link|.
    :type function:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_no_data: Hides the menu when there are no options to show.  Useful for preventing the menu from opening before results are fetched asynchronously.  Also has the effect of opening the menu when the `items` array changes if not already open.
    :type boolean:
    :param hide_selected: Do not display in the select menu items that are already selected
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param item_color: Sets color of selected items
    :type string:
    :param item_disabled: Set property of **items**'s disabled value
    :type ['string', 'array', 'function']:
    :param item_text: Set property of **items**'s text value
    :type ['string', 'array', 'function']:
    :param item_value: See description |VAutocomplete_vuetify_link|.
    :type ['string', 'array', 'function']:
    :param items: Can be an array of objects or array of strings. When using objects, will look for a text, value and disabled keys. This can be changed using the **item-text**, **item-value** and **item-disabled** props.  Objects that have a **header** or **divider** property are considered special cases and generate a list header or divider; these items are not selectable.
    :type array:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param menu_props: Pass props through to the `v-menu` component. Accepts either a string for boolean props `menu-props="auto, overflowY"`, or an object `:menu-props="{ auto: true, overflowY: true }"`
    :type ['string', 'array', 'object']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes select to multiple. Accepts array for value
    :type boolean:
    :param no_data_text: Display text when there is no data
    :type string:
    :param no_filter: Do not apply filtering when searching. Useful when data is being filtered server side
    :type boolean:
    :param open_on_clear: When using the **clearable** prop, once cleared, the select menu will either open or stay open, depending on the current state
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param return_object: Changes the selection behavior to return the object directly rather than the value specified with **item-value**
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param search_input: Search value. Can be used with `.sync` modifier.
    :type string:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param small_chips: Changes display of selections to chips with the **small** property
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: See description |VAutocomplete_vuetify_link|.
    :type function:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    :param update_list_index: Emitted when menu item is selected using keyboard arrows
    :param update_search_input: The `search-input.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-autocomplete", children, **kwargs)
        self._attr_names += [
            "allow_overflow",
            "append_icon",
            "append_outer_icon",
            "attach",
            "auto_select_first",
            "autofocus",
            "background_color",
            "cache_items",
            "chips",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "deletable_chips",
            "dense",
            "disable_lookup",
            "disabled",
            "eager",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "filter",  # JS functions unimplemented
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_no_data",
            "hide_selected",
            "hide_spin_buttons",
            "hint",
            "id",
            "item_color",
            "item_disabled",  # JS functions unimplemented
            "item_text",  # JS functions unimplemented
            "item_value",  # JS functions unimplemented
            "items",
            "label",
            "light",
            "loader_height",
            "loading",
            "menu_props",
            "messages",
            "multiple",
            "no_data_text",
            "no_filter",
            "open_on_clear",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "return_object",
            "reverse",
            "rounded",
            "rules",
            "search_input",
            "shaped",
            "single_line",
            "small_chips",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
            ("update_list_index", "update:list-index"),
            ("update_search_input", "update:search-input"),
        ]


class VAvatar(AbstractElement):

    """
    Vuetify's VAvatar component. See more info and examples |VAvatar_vuetify_link|.

    .. |VAvatar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-avatar" target="_blank">here</a>


    :param color: See description |VAvatar_vuetify_link|.
    :type string:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param left: See description |VAvatar_vuetify_link|.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param right: See description |VAvatar_vuetify_link|.
    :type boolean:
    :param rounded: See description |VAvatar_vuetify_link|.
    :type ['boolean', 'string']:
    :param size: Sets the height and width of the component.
    :type ['number', 'string']:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-avatar", children, **kwargs)
        self._attr_names += [
            "color",
            "height",
            "left",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "right",
            "rounded",
            "size",
            "tile",
            "width",
        ]


class VBadge(AbstractElement):

    """
    Vuetify's VBadge component. See more info and examples |VBadge_vuetify_link|.

    .. |VBadge_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-badge" target="_blank">here</a>


    :param avatar: Removes badge padding for the use of the `v-avatar` in the **badge** slot.
    :type boolean:
    :param bordered: Applies a **2px** by default and **1.5px** border around the badge when using the **dot** property.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param color: See description |VBadge_vuetify_link|.
    :type string:
    :param content: Any content you want injected as text into the badge.
    :type any:
    :param dark: See description |VBadge_vuetify_link|.
    :type boolean:
    :param dot: Reduce the size of the badge and hide its contents
    :type boolean:
    :param icon: Designates a specific icon used in the badge.
    :type string:
    :param inline: Moves the badge to be inline with the wrapping element. Supports the usage of the **left** prop.
    :type boolean:
    :param label: The **aria-label** used for the badge
    :type string:
    :param left: Aligns the component towards the left.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mode: See description |VBadge_vuetify_link|.
    :type string:
    :param offset_x: Offset the badge on the x-axis.
    :type ['number', 'string']:
    :param offset_y: Offset the badge on the y-axis.
    :type ['number', 'string']:
    :param origin: See description |VBadge_vuetify_link|.
    :type string:
    :param overlap: Overlaps the slotted content on top of the component.
    :type boolean:
    :param tile: Removes the component's border-radius.
    :type boolean:
    :param transition: See description |VBadge_vuetify_link|.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-badge", children, **kwargs)
        self._attr_names += [
            "avatar",
            "bordered",
            "bottom",
            "color",
            "content",
            "dark",
            "dot",
            "icon",
            "inline",
            "label",
            "left",
            "light",
            "mode",
            "offset_x",
            "offset_y",
            "origin",
            "overlap",
            "tile",
            "transition",
            "value",
        ]


class VBanner(AbstractElement):

    """
    Vuetify's VBanner component. See more info and examples |VBanner_vuetify_link|.

    .. |VBanner_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-banner" target="_blank">here</a>


    :param app: When used inside of `v-main`, will calculate top based upon application `v-toolbar` and `v-system-bar`.
    :type boolean:
    :param color: See description |VBanner_vuetify_link|.
    :type string:
    :param dark: See description |VBanner_vuetify_link|.
    :type boolean:
    :param elevation: See description |VBanner_vuetify_link|.
    :type ['number', 'string']:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param icon: Designates a specific icon.
    :type string:
    :param icon_color: Designates a specific icon color.
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param mobile_breakpoint: Sets the designated mobile breakpoint for the component.
    :type ['number', 'string']:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param rounded: See description |VBanner_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param single_line: Forces the banner onto a single line.
    :type boolean:
    :param sticky: See description |VBanner_vuetify_link|.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param value: Controls whether the component is visible or hidden.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-banner", children, **kwargs)
        self._attr_names += [
            "app",
            "color",
            "dark",
            "elevation",
            "height",
            "icon",
            "icon_color",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "mobile_breakpoint",
            "outlined",
            "rounded",
            "shaped",
            "single_line",
            "sticky",
            "tag",
            "tile",
            "value",
            "width",
        ]


class VBottomNavigation(AbstractElement):

    """
    Vuetify's VBottomNavigation component. See more info and examples |VBottomNavigation_vuetify_link|.

    .. |VBottomNavigation_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-bottom-navigation" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param active_class: See description |VBottomNavigation_vuetify_link|.
    :type string:
    :param app: See description |VBottomNavigation_vuetify_link|.
    :type boolean:
    :param background_color: Changes the background-color for the component.
    :type string:
    :param color: See description |VBottomNavigation_vuetify_link|.
    :type string:
    :param dark: See description |VBottomNavigation_vuetify_link|.
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param grow: See description |VBottomNavigation_vuetify_link|.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param hide_on_scroll: Will transition the navigation off screen when scrolling up.
    :type boolean:
    :param horizontal: See description |VBottomNavigation_vuetify_link|.
    :type boolean:
    :param input_value: Controls whether the component is visible or hidden. Supports the **.sync** modifier.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param scroll_target: Designates the element to target for scrolling events. Uses `window` by default.
    :type string:
    :param scroll_threshold: The amount of scroll distance down before **hide-on-scroll** activates.
    :type ['string', 'number']:
    :param shift: See description |VBottomNavigation_vuetify_link|.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param value: See description |VBottomNavigation_vuetify_link|.
    :type any:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param change: The value of currently selected button. If no value is assigned, will be the current index of the button.
    :param update_input_value: The event used for `input-value.sync`.
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-bottom-navigation", children, **kwargs)
        self._attr_names += [
            "absolute",
            "active_class",
            "app",
            "background_color",
            "color",
            "dark",
            "fixed",
            "grow",
            "height",
            "hide_on_scroll",
            "horizontal",
            "input_value",
            "light",
            "mandatory",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "scroll_target",
            "scroll_threshold",
            "shift",
            "tag",
            "value",
            "width",
        ]
        self._event_names += [
            "change",
            ("update_input_value", "update:input-value"),
        ]


class VBottomSheet(AbstractElement):

    """
    Vuetify's VBottomSheet component. See more info and examples |VBottomSheet_vuetify_link|.

    .. |VBottomSheet_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-bottom-sheet" target="_blank">here</a>


    :param activator: Designate a custom activator when the `activator` slot is not used. String can be any valid querySelector and Object can be any valid Node.
    :type any:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param close_delay: Milliseconds to wait before closing component.
    :type ['number', 'string']:
    :param content_class: Applies a custom class to the detached element. This is useful because the content is moved to the beginning of the `v-app` component (unless the **attach** prop is provided) and is not targetable by classes passed directly on the component.
    :type string:
    :param dark: See description |VBottomSheet_vuetify_link|.
    :type boolean:
    :param disabled: Disables the ability to open the component.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param fullscreen: Changes layout for fullscreen display.
    :type boolean:
    :param hide_overlay: Hides the display of the overlay.
    :type boolean:
    :param inset: Reduces the sheet content maximum width to 70%.
    :type boolean:
    :param internal_activator: Detaches the menu content inside of the component as opposed to the document.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_width: Sets the maximum width for the component.
    :type ['string', 'number']:
    :param no_click_animation: Disables the bounce effect when clicking outside of a `v-dialog`'s content when using the **persistent** prop.
    :type boolean:
    :param open_delay: Milliseconds to wait before opening component.
    :type ['number', 'string']:
    :param open_on_focus:
    :type boolean:
    :param open_on_hover: Designates whether component should activate when its activator is hovered.
    :type boolean:
    :param origin: See description |VBottomSheet_vuetify_link|.
    :type string:
    :param overlay_color: Sets the overlay color.
    :type string:
    :param overlay_opacity: Sets the overlay opacity.
    :type ['number', 'string']:
    :param persistent: Clicking outside of the element or pressing **esc** key will not deactivate it.
    :type boolean:
    :param retain_focus: Tab focus will return to the first child of the dialog by default. Disable this when using external tools that require focus such as TinyMCE or vue-clipboard.
    :type boolean:
    :param return_value:
    :type any:
    :param scrollable: See description |VBottomSheet_vuetify_link|.
    :type boolean:
    :param transition: See description |VBottomSheet_vuetify_link|.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param width: Sets the width for the component.
    :type ['string', 'number']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-bottom-sheet", children, **kwargs)
        self._attr_names += [
            "activator",
            "attach",
            "close_delay",
            "content_class",
            "dark",
            "disabled",
            "eager",
            "fullscreen",
            "hide_overlay",
            "inset",
            "internal_activator",
            "light",
            "max_width",
            "no_click_animation",
            "open_delay",
            "open_on_focus",
            "open_on_hover",
            "origin",
            "overlay_color",
            "overlay_opacity",
            "persistent",
            "retain_focus",
            "return_value",
            "scrollable",
            "transition",
            "value",
            "width",
        ]


class VBreadcrumbs(AbstractElement):

    """
    Vuetify's VBreadcrumbs component. See more info and examples |VBreadcrumbs_vuetify_link|.

    .. |VBreadcrumbs_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-breadcrumbs" target="_blank">here</a>


    :param dark: See description |VBreadcrumbs_vuetify_link|.
    :type boolean:
    :param divider: Specifies the dividing character between items.
    :type string:
    :param items: An array of objects for each breadcrumb.
    :type array:
    :param large: Increase the font-size of the breadcrumb item text to 16px (14px default).
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-breadcrumbs", children, **kwargs)
        self._attr_names += [
            "dark",
            "divider",
            "items",
            "large",
            "light",
        ]


class VBreadcrumbsItem(AbstractElement):

    """
    Vuetify's VBreadcrumbsItem component. See more info and examples |VBreadcrumbsItem_vuetify_link|.

    .. |VBreadcrumbsItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-breadcrumbs-item" target="_blank">here</a>


    :param active_class: See description |VBreadcrumbsItem_vuetify_link|.
    :type string:
    :param append: See description |VBreadcrumbsItem_vuetify_link|.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param exact: See description |VBreadcrumbsItem_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VBreadcrumbsItem_vuetify_link|.
    :type string:
    :param exact_path: See description |VBreadcrumbsItem_vuetify_link|.
    :type boolean:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param nuxt: See description |VBreadcrumbsItem_vuetify_link|.
    :type boolean:
    :param replace: See description |VBreadcrumbsItem_vuetify_link|.
    :type boolean:
    :param ripple: See description |VBreadcrumbsItem_vuetify_link|.
    :type ['boolean', 'object']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param to: See description |VBreadcrumbsItem_vuetify_link|.
    :type ['string', 'object']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-breadcrumbs-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append",
            "disabled",
            "exact",
            "exact_active_class",
            "exact_path",
            "href",
            "link",
            "nuxt",
            "replace",
            "ripple",
            "tag",
            "target",
            "to",
        ]


class VBreadcrumbsDivider(AbstractElement):

    """
    Vuetify's VBreadcrumbsDivider component. See more info and examples |VBreadcrumbsDivider_vuetify_link|.

    .. |VBreadcrumbsDivider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-breadcrumbs-divider" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-breadcrumbs-divider", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VBtn(AbstractElement):

    """
    Vuetify's VBtn component. See more info and examples |VBtn_vuetify_link|.

    .. |VBtn_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-btn" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param active_class: See description |VBtn_vuetify_link|.
    :type string:
    :param append: See description |VBtn_vuetify_link|.
    :type boolean:
    :param block: Expands the button to 100% of available space.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param color: See description |VBtn_vuetify_link|.
    :type string:
    :param dark: See description |VBtn_vuetify_link|.
    :type boolean:
    :param depressed: Removes the button box shadow.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param elevation: See description |VBtn_vuetify_link|.
    :type ['number', 'string']:
    :param exact: See description |VBtn_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VBtn_vuetify_link|.
    :type string:
    :param exact_path: See description |VBtn_vuetify_link|.
    :type boolean:
    :param fab: Designates the button as a floating-action-button. Button will become _round_.
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param icon: Designates the button as icon. Button will become _round_ and applies the **text** prop.
    :type boolean:
    :param input_value: Controls the button's active state.
    :type any:
    :param large: Makes the component large.
    :type boolean:
    :param left: Aligns the component towards the left. This should be used with the **absolute** or **fixed** props.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param loading: Adds a loading icon animation.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param nuxt: See description |VBtn_vuetify_link|.
    :type boolean:
    :param outlined: Makes the background transparent and applies a thin border.
    :type boolean:
    :param plain: Removes the default background change applied when hovering over the button.
    :type boolean:
    :param replace: See description |VBtn_vuetify_link|.
    :type boolean:
    :param retain_focus_on_click: Don't blur on click.
    :type boolean:
    :param right: Aligns the component towards the right. This should be used with the **absolute** or **fixed** props.
    :type boolean:
    :param ripple: See description |VBtn_vuetify_link|.
    :type ['boolean', 'object']:
    :param rounded: Applies a large border radius on the button.
    :type boolean:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param small: Makes the component small.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param text: Makes the background transparent. When using the **color** prop, the color will be applied to the button text instead of the background.
    :type boolean:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param to: See description |VBtn_vuetify_link|.
    :type ['string', 'object']:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param type: Set the button's **type** attribute.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param width: Sets the width for the component.
    :type ['number', 'string']:
    :param x_large: Makes the component extra large.
    :type boolean:
    :param x_small: Makes the component extra small.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-btn", children, **kwargs)
        self._attr_names += [
            "absolute",
            "active_class",
            "append",
            "block",
            "bottom",
            "color",
            "dark",
            "depressed",
            "disabled",
            "elevation",
            "exact",
            "exact_active_class",
            "exact_path",
            "fab",
            "fixed",
            "height",
            "href",
            "icon",
            "input_value",
            "large",
            "left",
            "light",
            "link",
            "loading",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "nuxt",
            "outlined",
            "plain",
            "replace",
            "retain_focus_on_click",
            "right",
            "ripple",
            "rounded",
            "shaped",
            "small",
            "tag",
            "target",
            "text",
            "tile",
            "to",
            "top",
            "type",
            "value",
            "width",
            "x_large",
            "x_small",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
        ]


class VBtnToggle(AbstractElement):

    """
    Vuetify's VBtnToggle component. See more info and examples |VBtnToggle_vuetify_link|.

    .. |VBtnToggle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-btn-toggle" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param background_color: Changes the background-color for the component.
    :type string:
    :param borderless: Removes the group's border.
    :type boolean:
    :param color: See description |VBtnToggle_vuetify_link|.
    :type string:
    :param dark: See description |VBtnToggle_vuetify_link|.
    :type boolean:
    :param dense: Reduces the button size and padding.
    :type boolean:
    :param group: See description |VBtnToggle_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param rounded: Round edge buttons
    :type boolean:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's border-radius.
    :type boolean:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the input is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-btn-toggle", children, **kwargs)
        self._attr_names += [
            "active_class",
            "background_color",
            "borderless",
            "color",
            "dark",
            "dense",
            "group",
            "light",
            "mandatory",
            "max",
            "multiple",
            "rounded",
            "shaped",
            "tag",
            "tile",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
        ]


class VCalendar(AbstractElement):

    """
    Vuetify's VCalendar component. See more info and examples |VCalendar_vuetify_link|.

    .. |VCalendar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-calendar" target="_blank">here</a>


    :param categories: Specifies what categories to display in the `category` view. This controls the order of the categories as well. If the calendar uses events any categories specified in those events not specified in this value are dynamically rendered in the view unless `category-hide-dynamic` is true.
    :type ['array', 'string']:
    :param category_days: The number of days to render in the `category` view.
    :type ['number', 'string']:
    :param category_for_invalid: The category to place events in that have invalid categories. A category is invalid when it is not a string. By default events without a category are not displayed until this value is specified.
    :type string:
    :param category_hide_dynamic: Sets whether categories specified in an event should be hidden if it's not defined in `categories`.
    :type boolean:
    :param category_show_all: Set whether the `category` view should show all defined `categories` even if there are no events for a category.
    :type boolean:
    :param category_text: If categories is a list of objects, you can use this to determine what property to print out as the category text on the calendar. You can provide a function to do some logic or just define the prop name. It's similar to item-text on v-select
    :type ['string', 'function']:
    :param color: See description |VCalendar_vuetify_link|.
    :type string:
    :param dark: See description |VCalendar_vuetify_link|.
    :type boolean:
    :param day_format: Formats day of the month string that appears in a day to a specified locale
    :type function:
    :param end: The ending date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param event_category: Set property of *event*'s category. Instead of a property a function can be given which takes an event and returns the category.
    :type ['string', 'function']:
    :param event_color: A background color for all events or a function which accepts an event object passed to the calendar to return a color.
    :type ['string', 'function']:
    :param event_end: Set property of *event*'s end timestamp.
    :type string:
    :param event_height: The height of an event in pixels in the `month` view and at the top of the `day` views.
    :type number:
    :param event_margin_bottom: Margin bottom for event
    :type number:
    :param event_more: Whether the more 'button' is displayed on a calendar with too many events in a given day. It will say something like '5 more' and when clicked generates a `click:more` event.
    :type boolean:
    :param event_more_text: The text to display in the more 'button' given the number of hidden events.
    :type string:
    :param event_name: Set property of *event*'s displayed name, or a function which accepts an event object passed to the calendar as the first argument and a flag signalling whether the name is for a timed event (true) or an event over a day.
    :type ['string', 'function']:
    :param event_overlap_mode: One of `stack`, `column`, or a custom render function
    :type ['string', 'function']:
    :param event_overlap_threshold: A value in minutes that's used to determine whether two timed events should be placed in column beside each other or should be treated as slightly overlapping events.
    :type ['string', 'number']:
    :param event_ripple: Applies the `v-ripple` directive.
    :type ['boolean', 'object']:
    :param event_start: Set property of *event*'s start timestamp.
    :type string:
    :param event_text_color: A text color for all events or a function which accepts an event object passed to the calendar to return a color.
    :type ['string', 'function']:
    :param event_timed: If Dates or milliseconds are used as the start or end timestamp of an event, this prop can be a string to a property on the event that is truthy if the event is a timed event or a function which takes the event and returns a truthy value if the event is a timed event.
    :type ['string', 'function']:
    :param events: An array of event objects with a property for a start timestamp and optionally a name and end timestamp. If an end timestamp is not given, the value of start will be used. If no name is given, you must provide an implementation for the `event` slot.
    :type array:
    :param first_interval: The first interval to display in the `day` view. If `intervalMinutes` is set to 60 and this is set to 9 the first time in the view is 9am.
    :type ['number', 'string']:
    :param first_time: The first time to display in the `day` view. If specified, this overwrites any `firstInterval` value specified. This can be the number of minutes since midnight, a string in the format of `HH:mm`, or an object with number properties hour and minute.
    :type ['number', 'string', 'object']:
    :param hide_header: If the header at the top of the `day` view should be visible.
    :type boolean:
    :param interval_count: The number of intervals to display in the `day` view.
    :type ['number', 'string']:
    :param interval_format: Formats time of day string that appears in the interval gutter of the `day` and `week` view to specified locale
    :type function:
    :param interval_height: The height of an interval in pixels in the `day` view.
    :type ['number', 'string']:
    :param interval_minutes: The number of minutes the intervals are in the `day` view. A common interval is 60 minutes so the intervals are an hour.
    :type ['number', 'string']:
    :param interval_style: Returns CSS styling to apply to the interval.
    :type function:
    :param interval_width: The width of the interval gutter on the left side in the `day` view.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param locale: The locale of the calendar.
    :type string:
    :param locale_first_day_of_year: Sets the day that determines the first week of the year, starting with 0 for **Sunday**. For ISO 8601 this should be 4.
    :type ['string', 'number']:
    :param max_days: The maximum number of days to display in the custom calendar if an `end` day is not set.
    :type number:
    :param min_weeks: The minimum number of weeks to display in the `month` or `week` view.
    :type any:
    :param month_format: Formats month string that appears in a day to specified locale
    :type function:
    :param now: Override the day & time which is considered now. This is in the format of `YYYY-MM-DD hh:mm:ss`. The calendar is styled according to now.
    :type string:
    :param short_intervals: If true, the intervals in the `day` view will be 9 AM as opposed to 09:00 AM
    :type boolean:
    :param short_months: Whether the short versions of a month should be used (Jan vs January).
    :type boolean:
    :param short_weekdays: Whether the short versions of a weekday should be used (Mon vs Monday).
    :type boolean:
    :param show_interval_label: Checks if a given day and time should be displayed in the interval gutter of the `day` view.
    :type function:
    :param show_month_on_first: Whether the name of the month should be displayed on the first day of the month.
    :type boolean:
    :param show_week: Whether week numbers should be displayed when using the `month` view.
    :type boolean:
    :param start: The starting date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param type: A string which is one of `month`, `week`, `day`, `4day`, `custom-weekly`, `custom-daily`, and `category`. The custom types look at the `start` and `end` dates passed to the component as opposed to the `value`.
    :type string:
    :param value: A date in the format of `YYYY-MM-DD` which determines what span of time for the calendar.
    :type ['string', 'number', 'date']:
    :param weekday_format: Formats day of the week string that appears in the header to specified locale
    :type function:
    :param weekdays: Specifies which days of the week to display. To display Monday through Friday only, a value of `[1, 2, 3, 4, 5]` can be used. To display a week starting on Monday a value of `[1, 2, 3, 4, 5, 6, 0]` can be used.
    :type ['array', 'string']:

    Events

    :param change: The range of days displayed on the calendar changed. This is triggered on initialization. The event passed is an object with start and end date objects.
    :param click_date: The click event on the day of the month link. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param click_day: The click event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param click_day_category: The click event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param click_event: The click event on a specific event. The event passed is the day & time object.
    :param click_interval: The click event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param click_more: The click event on the `X more` button on views with too many events in a day. Native mouse event is passed as a second argument.
    :param click_time: The click event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param click_time_category: The click event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param contextmenu_date: The right-click event on the day of the month link. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param contextmenu_day: The right-click event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param contextmenu_day_category: The right-click event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param contextmenu_event: The right-click event on an event. The event passed is the day & time object.
    :param contextmenu_interval: The right-click event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param contextmenu_time: The right-click event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param contextmenu_time_category: The right-click event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param input: An alias to the `click:date` event used to support v-model.
    :param mousedown_day: The mousedown event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mousedown_day_category: The mousedown event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mousedown_event: The mousedown event on an event. The event passed is the day & time object.
    :param mousedown_interval: The mousedown event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mousedown_time: The mousedown event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mousedown_time_category: The mousedown event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseenter_day: The mouseenter event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseenter_day_category: The mouseenter event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseenter_event: The mouseenter event on an event. The event passed is the day & time object.
    :param mouseenter_interval: The mouseenter event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseenter_time: The mouseenter event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseenter_time_category: The mouseenter event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseleave_day: The mouseleave event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseleave_day_category: The mouseleave event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseleave_event: The mouseleave event on an event. The event passed is the day & time object.
    :param mouseleave_interval: The mouseleave event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseleave_time: The mouseleave event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseleave_time_category: The mouseleave event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mousemove_day: The mousemove event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mousemove_day_category: The mousemove event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mousemove_event: The mousemove event on an event. The event passed is the day & time object.
    :param mousemove_interval: The mousemove event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mousemove_time: The mousemove event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mousemove_time_category: The mousemove event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseup_day: The mouseup event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseup_day_category: The mouseup event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param mouseup_event: The mouseup event on an event. The event passed is the day & time object.
    :param mouseup_interval: The mouseup event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseup_time: The mouseup event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param mouseup_time_category: The mouseup event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param moved: One of the functions `next`, `prev`, and `move` was called. The event passed is the day object calculated for the movement.
    :param touchend_day: The touchend event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchend_day_category: The touchend event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchend_event: The touchend event on am view. The event passed is the day & time object.
    :param touchend_interval: The touchend event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchend_time: The touchend event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchend_time_category: The touchend event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchmove_day: The touchmove event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchmove_day_category: The touchmove event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchmove_event: The touchmove event on an `event` view. The event passed is the day & time object.
    :param touchmove_interval: The touchmove event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchmove_time: The touchmove event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchmove_time_category: The touchmove event at a specific time in the `category` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchstart_day: The touchstart event on a day. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchstart_day_category: The touchstart event on a day in the `category` view. The event passed is the day object. Native mouse event is passed as a second argument.
    :param touchstart_event: The touchstart event on an event` view. The event passed is the day & time object.
    :param touchstart_interval: The touchstart event at a specific interval label in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchstart_time: The touchstart event at a specific time in the `day` view. The event passed is the day & time object. Native mouse event is passed as a second argument.
    :param touchstart_time_category: The touchstart event at a specific time in the `category` view. The event passed is the day & time object Native mouse event is passed as a second argument..
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-calendar", children, **kwargs)
        self._attr_names += [
            "categories",
            "category_days",
            "category_for_invalid",
            "category_hide_dynamic",
            "category_show_all",
            "category_text",  # JS functions unimplemented
            "color",
            "dark",
            "day_format",  # JS functions unimplemented
            "end",
            "event_category",  # JS functions unimplemented
            "event_color",  # JS functions unimplemented
            "event_end",
            "event_height",
            "event_margin_bottom",
            "event_more",
            "event_more_text",
            "event_name",  # JS functions unimplemented
            "event_overlap_mode",  # JS functions unimplemented
            "event_overlap_threshold",
            "event_ripple",
            "event_start",
            "event_text_color",  # JS functions unimplemented
            "event_timed",  # JS functions unimplemented
            "events",
            "first_interval",
            "first_time",
            "hide_header",
            "interval_count",
            "interval_format",  # JS functions unimplemented
            "interval_height",
            "interval_minutes",
            "interval_style",  # JS functions unimplemented
            "interval_width",
            "light",
            "locale",
            "locale_first_day_of_year",
            "max_days",
            "min_weeks",
            "month_format",  # JS functions unimplemented
            "now",
            "short_intervals",
            "short_months",
            "short_weekdays",
            "show_interval_label",  # JS functions unimplemented
            "show_month_on_first",
            "show_week",
            "start",
            "type",
            "value",
            "weekday_format",  # JS functions unimplemented
            "weekdays",
        ]
        self._event_names += [
            "change",
            ("click_date", "click:date"),
            ("click_day", "click:day"),
            ("click_day_category", "click:day-category"),
            ("click_event", "click:event"),
            ("click_interval", "click:interval"),
            ("click_more", "click:more"),
            ("click_time", "click:time"),
            ("click_time_category", "click:time-category"),
            ("contextmenu_date", "contextmenu:date"),
            ("contextmenu_day", "contextmenu:day"),
            ("contextmenu_day_category", "contextmenu:day-category"),
            ("contextmenu_event", "contextmenu:event"),
            ("contextmenu_interval", "contextmenu:interval"),
            ("contextmenu_time", "contextmenu:time"),
            ("contextmenu_time_category", "contextmenu:time-category"),
            "input",
            ("mousedown_day", "mousedown:day"),
            ("mousedown_day_category", "mousedown:day-category"),
            ("mousedown_event", "mousedown:event"),
            ("mousedown_interval", "mousedown:interval"),
            ("mousedown_time", "mousedown:time"),
            ("mousedown_time_category", "mousedown:time-category"),
            ("mouseenter_day", "mouseenter:day"),
            ("mouseenter_day_category", "mouseenter:day-category"),
            ("mouseenter_event", "mouseenter:event"),
            ("mouseenter_interval", "mouseenter:interval"),
            ("mouseenter_time", "mouseenter:time"),
            ("mouseenter_time_category", "mouseenter:time-category"),
            ("mouseleave_day", "mouseleave:day"),
            ("mouseleave_day_category", "mouseleave:day-category"),
            ("mouseleave_event", "mouseleave:event"),
            ("mouseleave_interval", "mouseleave:interval"),
            ("mouseleave_time", "mouseleave:time"),
            ("mouseleave_time_category", "mouseleave:time-category"),
            ("mousemove_day", "mousemove:day"),
            ("mousemove_day_category", "mousemove:day-category"),
            ("mousemove_event", "mousemove:event"),
            ("mousemove_interval", "mousemove:interval"),
            ("mousemove_time", "mousemove:time"),
            ("mousemove_time_category", "mousemove:time-category"),
            ("mouseup_day", "mouseup:day"),
            ("mouseup_day_category", "mouseup:day-category"),
            ("mouseup_event", "mouseup:event"),
            ("mouseup_interval", "mouseup:interval"),
            ("mouseup_time", "mouseup:time"),
            ("mouseup_time_category", "mouseup:time-category"),
            "moved",
            ("touchend_day", "touchend:day"),
            ("touchend_day_category", "touchend:day-category"),
            ("touchend_event", "touchend:event"),
            ("touchend_interval", "touchend:interval"),
            ("touchend_time", "touchend:time"),
            ("touchend_time_category", "touchend:time-category"),
            ("touchmove_day", "touchmove:day"),
            ("touchmove_day_category", "touchmove:day-category"),
            ("touchmove_event", "touchmove:event"),
            ("touchmove_interval", "touchmove:interval"),
            ("touchmove_time", "touchmove:time"),
            ("touchmove_time_category", "touchmove:time-category"),
            ("touchstart_day", "touchstart:day"),
            ("touchstart_day_category", "touchstart:day-category"),
            ("touchstart_event", "touchstart:event"),
            ("touchstart_interval", "touchstart:interval"),
            ("touchstart_time", "touchstart:time"),
            ("touchstart_time_category", "touchstart:time-category"),
        ]


class VCalendarDaily(AbstractElement):

    """
    Vuetify's VCalendarDaily component. See more info and examples |VCalendarDaily_vuetify_link|.

    .. |VCalendarDaily_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-calendar-daily" target="_blank">here</a>


    :param color: See description |VCalendarDaily_vuetify_link|.
    :type string:
    :param dark: See description |VCalendarDaily_vuetify_link|.
    :type boolean:
    :param day_format: Formats day of the month string that appears in a day to a specified locale
    :type function:
    :param end: The ending date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param first_interval: The first interval to display in the `day` view. If `intervalMinutes` is set to 60 and this is set to 9 the first time in the view is 9am.
    :type ['number', 'string']:
    :param first_time: The first time to display in the `day` view. If specified, this overwrites any `firstInterval` value specified. This can be the number of minutes since midnight, a string in the format of `HH:mm`, or an object with number properties hour and minute.
    :type ['number', 'string', 'object']:
    :param hide_header: If the header at the top of the `day` view should be visible.
    :type boolean:
    :param interval_count: The number of intervals to display in the `day` view.
    :type ['number', 'string']:
    :param interval_format: Formats time of day string that appears in the interval gutter of the `day` and `week` view to specified locale
    :type function:
    :param interval_height: The height of an interval in pixels in the `day` view.
    :type ['number', 'string']:
    :param interval_minutes: The number of minutes the intervals are in the `day` view. A common interval is 60 minutes so the intervals are an hour.
    :type ['number', 'string']:
    :param interval_style: Returns CSS styling to apply to the interval.
    :type function:
    :param interval_width: The width of the interval gutter on the left side in the `day` view.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param locale: The locale of the calendar.
    :type string:
    :param max_days: The maximum number of days to display in the custom calendar if an `end` day is not set.
    :type number:
    :param now: Override the day & time which is considered now. This is in the format of `YYYY-MM-DD hh:mm:ss`. The calendar is styled according to now.
    :type string:
    :param short_intervals: If true, the intervals in the `day` view will be 9 AM as opposed to 09:00 AM
    :type boolean:
    :param short_weekdays: Whether the short versions of a weekday should be used (Mon vs Monday).
    :type boolean:
    :param show_interval_label: Checks if a given day and time should be displayed in the interval gutter of the `day` view.
    :type function:
    :param start: The starting date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param weekday_format: Formats day of the week string that appears in the header to specified locale
    :type function:
    :param weekdays: Specifies which days of the week to display. To display Monday through Friday only, a value of `[1, 2, 3, 4, 5]` can be used. To display a week starting on Monday a value of `[1, 2, 3, 4, 5, 6, 0]` can be used.
    :type ['array', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-calendar-daily", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "day_format",  # JS functions unimplemented
            "end",
            "first_interval",
            "first_time",
            "hide_header",
            "interval_count",
            "interval_format",  # JS functions unimplemented
            "interval_height",
            "interval_minutes",
            "interval_style",  # JS functions unimplemented
            "interval_width",
            "light",
            "locale",
            "max_days",
            "now",
            "short_intervals",
            "short_weekdays",
            "show_interval_label",  # JS functions unimplemented
            "start",
            "weekday_format",  # JS functions unimplemented
            "weekdays",
        ]


class VCalendarWeekly(AbstractElement):

    """
    Vuetify's VCalendarWeekly component. See more info and examples |VCalendarWeekly_vuetify_link|.

    .. |VCalendarWeekly_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-calendar-weekly" target="_blank">here</a>


    :param color: See description |VCalendarWeekly_vuetify_link|.
    :type string:
    :param dark: See description |VCalendarWeekly_vuetify_link|.
    :type boolean:
    :param day_format: Formats day of the month string that appears in a day to a specified locale
    :type function:
    :param end: The ending date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param hide_header: If the header at the top of the `day` view should be visible.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param locale: The locale of the calendar.
    :type string:
    :param locale_first_day_of_year: Sets the day that determines the first week of the year, starting with 0 for **Sunday**. For ISO 8601 this should be 4.
    :type ['string', 'number']:
    :param min_weeks: The minimum number of weeks to display in the `month` or `week` view.
    :type any:
    :param month_format: Formats month string that appears in a day to specified locale
    :type function:
    :param now: Override the day & time which is considered now. This is in the format of `YYYY-MM-DD hh:mm:ss`. The calendar is styled according to now.
    :type string:
    :param short_months: Whether the short versions of a month should be used (Jan vs January).
    :type boolean:
    :param short_weekdays: Whether the short versions of a weekday should be used (Mon vs Monday).
    :type boolean:
    :param show_month_on_first: Whether the name of the month should be displayed on the first day of the month.
    :type boolean:
    :param show_week: Whether week numbers should be displayed when using the `month` view.
    :type boolean:
    :param start: The starting date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param weekday_format: Formats day of the week string that appears in the header to specified locale
    :type function:
    :param weekdays: Specifies which days of the week to display. To display Monday through Friday only, a value of `[1, 2, 3, 4, 5]` can be used. To display a week starting on Monday a value of `[1, 2, 3, 4, 5, 6, 0]` can be used.
    :type ['array', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-calendar-weekly", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "day_format",  # JS functions unimplemented
            "end",
            "hide_header",
            "light",
            "locale",
            "locale_first_day_of_year",
            "min_weeks",
            "month_format",  # JS functions unimplemented
            "now",
            "short_months",
            "short_weekdays",
            "show_month_on_first",
            "show_week",
            "start",
            "weekday_format",  # JS functions unimplemented
            "weekdays",
        ]


class VCalendarMonthly(AbstractElement):

    """
    Vuetify's VCalendarMonthly component. See more info and examples |VCalendarMonthly_vuetify_link|.

    .. |VCalendarMonthly_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-calendar-monthly" target="_blank">here</a>


    :param color: See description |VCalendarMonthly_vuetify_link|.
    :type string:
    :param dark: See description |VCalendarMonthly_vuetify_link|.
    :type boolean:
    :param day_format: Formats day of the month string that appears in a day to a specified locale
    :type function:
    :param end: The ending date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param hide_header: If the header at the top of the `day` view should be visible.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param locale: The locale of the calendar.
    :type string:
    :param locale_first_day_of_year: Sets the day that determines the first week of the year, starting with 0 for **Sunday**. For ISO 8601 this should be 4.
    :type ['string', 'number']:
    :param min_weeks: The minimum number of weeks to display in the `month` or `week` view.
    :type any:
    :param month_format: Formats month string that appears in a day to specified locale
    :type function:
    :param now: Override the day & time which is considered now. This is in the format of `YYYY-MM-DD hh:mm:ss`. The calendar is styled according to now.
    :type string:
    :param short_months: Whether the short versions of a month should be used (Jan vs January).
    :type boolean:
    :param short_weekdays: Whether the short versions of a weekday should be used (Mon vs Monday).
    :type boolean:
    :param show_month_on_first: Whether the name of the month should be displayed on the first day of the month.
    :type boolean:
    :param show_week: Whether week numbers should be displayed when using the `month` view.
    :type boolean:
    :param start: The starting date on the calendar (inclusive) in the format of `YYYY-MM-DD`. This may be ignored depending on the `type` of the calendar.
    :type ['string', 'number', 'date']:
    :param weekday_format: Formats day of the week string that appears in the header to specified locale
    :type function:
    :param weekdays: Specifies which days of the week to display. To display Monday through Friday only, a value of `[1, 2, 3, 4, 5]` can be used. To display a week starting on Monday a value of `[1, 2, 3, 4, 5, 6, 0]` can be used.
    :type ['array', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-calendar-monthly", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "day_format",  # JS functions unimplemented
            "end",
            "hide_header",
            "light",
            "locale",
            "locale_first_day_of_year",
            "min_weeks",
            "month_format",  # JS functions unimplemented
            "now",
            "short_months",
            "short_weekdays",
            "show_month_on_first",
            "show_week",
            "start",
            "weekday_format",  # JS functions unimplemented
            "weekdays",
        ]


class VCard(AbstractElement):

    """
    Vuetify's VCard component. See more info and examples |VCard_vuetify_link|.

    .. |VCard_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card" target="_blank">here</a>


    :param active_class: See description |VCard_vuetify_link|.
    :type string:
    :param append: See description |VCard_vuetify_link|.
    :type boolean:
    :param color: See description |VCard_vuetify_link|.
    :type string:
    :param dark: See description |VCard_vuetify_link|.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param elevation: See description |VCard_vuetify_link|.
    :type ['number', 'string']:
    :param exact: See description |VCard_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VCard_vuetify_link|.
    :type string:
    :param exact_path: See description |VCard_vuetify_link|.
    :type boolean:
    :param flat: Removes the card's elevation.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param hover: See description |VCard_vuetify_link|.
    :type boolean:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param img: See description |VCard_vuetify_link|.
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param nuxt: See description |VCard_vuetify_link|.
    :type boolean:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param raised: See description |VCard_vuetify_link|.
    :type boolean:
    :param replace: See description |VCard_vuetify_link|.
    :type boolean:
    :param ripple: See description |VCard_vuetify_link|.
    :type ['boolean', 'object']:
    :param rounded: See description |VCard_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param to: See description |VCard_vuetify_link|.
    :type ['string', 'object']:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-card", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append",
            "color",
            "dark",
            "disabled",
            "elevation",
            "exact",
            "exact_active_class",
            "exact_path",
            "flat",
            "height",
            "hover",
            "href",
            "img",
            "light",
            "link",
            "loader_height",
            "loading",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "nuxt",
            "outlined",
            "raised",
            "replace",
            "ripple",
            "rounded",
            "shaped",
            "tag",
            "target",
            "tile",
            "to",
            "width",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
        ]


class VCardActions(AbstractElement):

    """
    Vuetify's VCardActions component. See more info and examples |VCardActions_vuetify_link|.

    .. |VCardActions_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card-actions" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-card-actions", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCardSubtitle(AbstractElement):

    """
    Vuetify's VCardSubtitle component. See more info and examples |VCardSubtitle_vuetify_link|.

    .. |VCardSubtitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card-subtitle" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-card-subtitle", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCardText(AbstractElement):

    """
    Vuetify's VCardText component. See more info and examples |VCardText_vuetify_link|.

    .. |VCardText_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card-text" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-card-text", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCardTitle(AbstractElement):

    """
    Vuetify's VCardTitle component. See more info and examples |VCardTitle_vuetify_link|.

    .. |VCardTitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card-title" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-card-title", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCarousel(AbstractElement):

    """
    Vuetify's VCarousel component. See more info and examples |VCarousel_vuetify_link|.

    .. |VCarousel_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-carousel" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param continuous: Determines whether carousel is continuous
    :type boolean:
    :param cycle: Determines if the carousel should cycle through images.
    :type boolean:
    :param dark: See description |VCarousel_vuetify_link|.
    :type boolean:
    :param delimiter_icon: Sets icon for carousel delimiter
    :type string:
    :param height: Sets the height for the component
    :type ['number', 'string']:
    :param hide_delimiter_background: Hides the bottom delimiter background.
    :type boolean:
    :param hide_delimiters: Hides the carousel's bottom delimiters.
    :type boolean:
    :param interval: The duration between image cycles. Requires the **cycle** prop.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param next_icon: The displayed icon for forcing pagination to the next item.
    :type ['boolean', 'string']:
    :param prev_icon: The displayed icon for forcing pagination to the previous item.
    :type ['boolean', 'string']:
    :param progress: Displays a carousel progress bar. Requires the **cycle** prop and **interval**.
    :type boolean:
    :param progress_color: Applies specified color to progress bar.
    :type string:
    :param reverse: Reverse the normal transition direction.
    :type boolean:
    :param show_arrows: Displays arrows for next/previous navigation.
    :type boolean:
    :param show_arrows_on_hover: Displays navigation arrows only when the carousel is hovered over.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param touch: Provide a custom **left** and **right** function when swiped left or right.
    :type object:
    :param touchless: Disable touch support.
    :type boolean:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:
    :param vertical: Uses a vertical transition when changing windows.
    :type boolean:
    :param vertical_delimiters: Displays carousel delimiters vertically.
    :type string:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-carousel", children, **kwargs)
        self._attr_names += [
            "active_class",
            "continuous",
            "cycle",
            "dark",
            "delimiter_icon",
            "height",
            "hide_delimiter_background",
            "hide_delimiters",
            "interval",
            "light",
            "mandatory",
            "max",
            "multiple",
            "next_icon",
            "prev_icon",
            "progress",
            "progress_color",
            "reverse",
            "show_arrows",
            "show_arrows_on_hover",
            "tag",
            "touch",
            "touchless",
            "value",
            "value_comparator",  # JS functions unimplemented
            "vertical",
            "vertical_delimiters",
        ]
        self._event_names += [
            "change",
        ]


class VCarouselItem(AbstractElement):

    """
    Vuetify's VCarouselItem component. See more info and examples |VCarouselItem_vuetify_link|.

    .. |VCarouselItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-carousel-item" target="_blank">here</a>


    :param active_class: See description |VCarouselItem_vuetify_link|.
    :type string:
    :param append: See description |VCarouselItem_vuetify_link|.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param exact: See description |VCarouselItem_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VCarouselItem_vuetify_link|.
    :type string:
    :param exact_path: See description |VCarouselItem_vuetify_link|.
    :type boolean:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param nuxt: See description |VCarouselItem_vuetify_link|.
    :type boolean:
    :param replace: See description |VCarouselItem_vuetify_link|.
    :type boolean:
    :param reverse_transition: Sets the reverse transition
    :type ['boolean', 'string']:
    :param ripple: See description |VCarouselItem_vuetify_link|.
    :type ['boolean', 'object']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param to: See description |VCarouselItem_vuetify_link|.
    :type ['string', 'object']:
    :param transition: See description |VCarouselItem_vuetify_link|.
    :type ['boolean', 'string']:
    :param value: The value used when the component is selected in a group. If not provided, the index will be used.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-carousel-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append",
            "disabled",
            "eager",
            "exact",
            "exact_active_class",
            "exact_path",
            "href",
            "link",
            "nuxt",
            "replace",
            "reverse_transition",
            "ripple",
            "tag",
            "target",
            "to",
            "transition",
            "value",
        ]


class VCheckbox(AbstractElement):

    """
    Vuetify's VCheckbox component. See more info and examples |VCheckbox_vuetify_link|.

    .. |VCheckbox_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-checkbox" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param color: See description |VCheckbox_vuetify_link|.
    :type string:
    :param dark: See description |VCheckbox_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param false_value: Sets value for falsy state
    :type any:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param indeterminate: Sets an indeterminate state for the checkbox
    :type boolean:
    :param indeterminate_icon: The icon used when in an indeterminate state
    :type string:
    :param input_value: The **v-model** bound value
    :type any:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes expected model to an array
    :type boolean:
    :param off_icon: The icon used when inactive
    :type string:
    :param on_icon: The icon used when active
    :type string:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param ripple: See description |VCheckbox_vuetify_link|.
    :type ['boolean', 'object']:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param true_value: Sets value for truthy state
    :type any:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param update_error: The `error.sync` event
    :param update_indeterminate: The **indeterminate.sync** event.
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-checkbox", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "background_color",
            "color",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "false_value",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "indeterminate",
            "indeterminate_icon",
            "input_value",
            "label",
            "light",
            "messages",
            "multiple",
            "off_icon",
            "on_icon",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "ripple",
            "rules",
            "success",
            "success_messages",
            "true_value",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
            ("update_indeterminate", "update:indeterminate"),
        ]


class VSimpleCheckbox(AbstractElement):

    """
    Vuetify's VSimpleCheckbox component. See more info and examples |VSimpleCheckbox_vuetify_link|.

    .. |VSimpleCheckbox_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-simple-checkbox" target="_blank">here</a>


    :param color: See description |VSimpleCheckbox_vuetify_link|.
    :type string:
    :param dark: See description |VSimpleCheckbox_vuetify_link|.
    :type boolean:
    :param disabled: Disables simple checkbox.
    :type boolean:
    :param indeterminate: Sets an indeterminate state for the simple checkbox.
    :type boolean:
    :param indeterminate_icon: The icon used when in an indeterminate state.
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param off_icon: The icon used when inactive.
    :type string:
    :param on_icon: The icon used when active.
    :type string:
    :param ripple: See description |VSimpleCheckbox_vuetify_link|.
    :type boolean:
    :param value: A boolean value that represents whether the simple checkbox is checked.
    :type boolean:

    Events

    :param input: The updated bound model
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-simple-checkbox", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "disabled",
            "indeterminate",
            "indeterminate_icon",
            "light",
            "off_icon",
            "on_icon",
            "ripple",
            "value",
        ]
        self._event_names += [
            "input",
        ]


class VChip(AbstractElement):

    """
    Vuetify's VChip component. See more info and examples |VChip_vuetify_link|.

    .. |VChip_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-chip" target="_blank">here</a>


    :param active: Determines whether the chip is visible or not.
    :type boolean:
    :param active_class: See description |VChip_vuetify_link|.
    :type string:
    :param append: See description |VChip_vuetify_link|.
    :type boolean:
    :param close: Adds remove button
    :type boolean:
    :param close_icon: Change the default icon used for **close** chips
    :type string:
    :param close_label: See description |VChip_vuetify_link|.
    :type string:
    :param color: See description |VChip_vuetify_link|.
    :type string:
    :param dark: See description |VChip_vuetify_link|.
    :type boolean:
    :param disabled: Disables the chip, making it un-selectable
    :type boolean:
    :param draggable: Makes the chip draggable
    :type boolean:
    :param exact: See description |VChip_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VChip_vuetify_link|.
    :type string:
    :param exact_path: See description |VChip_vuetify_link|.
    :type boolean:
    :param filter: Displays a selection icon when selected
    :type boolean:
    :param filter_icon: Change the default icon used for **filter** chips
    :type string:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param input_value: Controls the **active** state of the item. This is typically used to highlight the component.
    :type any:
    :param label: Removes circle edges
    :type boolean:
    :param large: Makes the component large.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param link: Explicitly define the chip as a link
    :type boolean:
    :param nuxt: See description |VChip_vuetify_link|.
    :type boolean:
    :param outlined: Removes background and applies border and text color
    :type boolean:
    :param pill: Remove `v-avatar` padding
    :type boolean:
    :param replace: See description |VChip_vuetify_link|.
    :type boolean:
    :param ripple: See description |VChip_vuetify_link|.
    :type ['boolean', 'object']:
    :param small: Makes the component small.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param text_color: Applies a specified color to the control text
    :type string:
    :param to: See description |VChip_vuetify_link|.
    :type ['string', 'object']:
    :param value: See description |VChip_vuetify_link|.
    :type any:
    :param x_large: Makes the component extra large.
    :type boolean:
    :param x_small: Makes the component extra small.
    :type boolean:

    Events

    :param click_close: Emitted when close icon is clicked
    :param input: The updated bound model
    :param update_active: Emitted when close icon is clicked, sets active to `false`
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-chip", children, **kwargs)
        self._attr_names += [
            "active",
            "active_class",
            "append",
            "close",
            "close_icon",
            "close_label",
            "color",
            "dark",
            "disabled",
            "draggable",
            "exact",
            "exact_active_class",
            "exact_path",
            "filter",
            "filter_icon",
            "href",
            "input_value",
            "label",
            "large",
            "light",
            "link",
            "nuxt",
            "outlined",
            "pill",
            "replace",
            "ripple",
            "small",
            "tag",
            "target",
            "text_color",
            "to",
            "value",
            "x_large",
            "x_small",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
            ("click_close", "click:close"),
            "input",
            ("update_active", "update:active"),
        ]


class VChipGroup(AbstractElement):

    """
    Vuetify's VChipGroup component. See more info and examples |VChipGroup_vuetify_link|.

    .. |VChipGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-chip-group" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param center_active: Forces the selected chip to be centered
    :type boolean:
    :param color: See description |VChipGroup_vuetify_link|.
    :type string:
    :param column: Remove horizontal pagination and wrap items as needed
    :type boolean:
    :param dark: See description |VChipGroup_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param mobile_breakpoint: Sets the designated mobile breakpoint for the component.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param next_icon: Specify the icon to use for the next icon
    :type string:
    :param prev_icon: Specify the icon to use for the prev icon
    :type string:
    :param show_arrows: Force the display of the pagination arrows
    :type ['boolean', 'string']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-chip-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "center_active",
            "color",
            "column",
            "dark",
            "light",
            "mandatory",
            "max",
            "mobile_breakpoint",
            "multiple",
            "next_icon",
            "prev_icon",
            "show_arrows",
            "tag",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
        ]


class VColorPicker(AbstractElement):

    """
    Vuetify's VColorPicker component. See more info and examples |VColorPicker_vuetify_link|.

    .. |VColorPicker_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-color-picker" target="_blank">here</a>


    :param canvas_height: Height of canvas
    :type ['string', 'number']:
    :param dark: See description |VColorPicker_vuetify_link|.
    :type boolean:
    :param disabled: Disables picker
    :type boolean:
    :param dot_size: Changes the size of the selection dot on the canvas
    :type ['number', 'string']:
    :param elevation: See description |VColorPicker_vuetify_link|.
    :type ['number', 'string']:
    :param flat: Removes elevation
    :type boolean:
    :param hide_canvas: Hides canvas
    :type boolean:
    :param hide_inputs: Hides inputs
    :type boolean:
    :param hide_mode_switch: Hides mode switch
    :type boolean:
    :param hide_sliders: Hides sliders
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mode: Sets mode of inputs. Available modes are 'rgba', 'hsla', and 'hexa'. Can be synced with the `.sync` modifier.
    :type string:
    :param show_swatches: Displays color swatches
    :type boolean:
    :param swatches: Sets the available color swatches to select from - This prop only accepts rgba hex strings
    :type array:
    :param swatches_max_height: Sets the maximum height of the swatches section
    :type ['number', 'string']:
    :param value: Current color. This can be either a string representing a hex color, or an object representing a RGBA, HSLA, or HSVA value
    :type ['object', 'string']:
    :param width: Sets the width of the color picker
    :type ['number', 'string']:

    Events

    :param input: Selected color. Depending on what you passed to the `value` prop this is either a string or an object
    :param update_color: Selected color. This is the internal representation of the color, containing all values.
    :param update_mode: Selected mode
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-color-picker", children, **kwargs)
        self._attr_names += [
            "canvas_height",
            "dark",
            "disabled",
            "dot_size",
            "elevation",
            "flat",
            "hide_canvas",
            "hide_inputs",
            "hide_mode_switch",
            "hide_sliders",
            "light",
            "mode",
            "show_swatches",
            "swatches",
            "swatches_max_height",
            "value",
            "width",
        ]
        self._event_names += [
            "input",
            ("update_color", "update:color"),
            ("update_mode", "update:mode"),
        ]


class VContent(AbstractElement):

    """
    Vuetify's VContent component. See more info and examples |VContent_vuetify_link|.

    .. |VContent_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-content" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-content", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCombobox(AbstractElement):

    """
    Vuetify's VCombobox component. See more info and examples |VCombobox_vuetify_link|.

    .. |VCombobox_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-combobox" target="_blank">here</a>


    :param allow_overflow: Allow the menu to overflow off the screen
    :type boolean:
    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param auto_select_first: When searching, will always highlight the first option
    :type boolean:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param cache_items: Keeps a local _unique_ copy of all items that have been passed through the **items** prop.
    :type boolean:
    :param chips: Changes display of selections to chips
    :type boolean:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VCombobox_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VCombobox_vuetify_link|.
    :type boolean:
    :param deletable_chips: Adds a remove icon to selected chips
    :type boolean:
    :param delimiters: Accepts an array of strings that will trigger a new tag when typing. Does not replace the normal Tab and Enter keys.
    :type array:
    :param dense: Reduces the input height
    :type boolean:
    :param disable_lookup: Disables keyboard lookup
    :type boolean:
    :param disabled: Disables the input
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param filter: See description |VCombobox_vuetify_link|.
    :type function:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_no_data: Hides the menu when there are no options to show.  Useful for preventing the menu from opening before results are fetched asynchronously.  Also has the effect of opening the menu when the `items` array changes if not already open.
    :type boolean:
    :param hide_selected: Do not display in the select menu items that are already selected
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param item_color: Sets color of selected items
    :type string:
    :param item_disabled: Set property of **items**'s disabled value
    :type ['string', 'array', 'function']:
    :param item_text: Set property of **items**'s text value
    :type ['string', 'array', 'function']:
    :param item_value: See description |VCombobox_vuetify_link|.
    :type ['string', 'array', 'function']:
    :param items: Can be an array of objects or array of strings. When using objects, will look for a text, value and disabled keys. This can be changed using the **item-text**, **item-value** and **item-disabled** props.  Objects that have a **header** or **divider** property are considered special cases and generate a list header or divider; these items are not selectable.
    :type array:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param menu_props: Pass props through to the `v-menu` component. Accepts either a string for boolean props `menu-props="auto, overflowY"`, or an object `:menu-props="{ auto: true, overflowY: true }"`
    :type ['string', 'array', 'object']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes select to multiple. Accepts array for value
    :type boolean:
    :param no_data_text: Display text when there is no data
    :type string:
    :param no_filter: Do not apply filtering when searching. Useful when data is being filtered server side
    :type boolean:
    :param open_on_clear: When using the **clearable** prop, once cleared, the select menu will either open or stay open, depending on the current state
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param return_object: Changes the selection behavior to return the object directly rather than the value specified with **item-value**
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param search_input: Search value. Can be used with `.sync` modifier.
    :type string:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param small_chips: Changes display of selections to chips with the **small** property
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: See description |VCombobox_vuetify_link|.
    :type function:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    :param update_list_index: Emitted when menu item is selected using keyboard arrows
    :param update_search_input: The `search-input.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-combobox", children, **kwargs)
        self._attr_names += [
            "allow_overflow",
            "append_icon",
            "append_outer_icon",
            "attach",
            "auto_select_first",
            "autofocus",
            "background_color",
            "cache_items",
            "chips",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "deletable_chips",
            "delimiters",
            "dense",
            "disable_lookup",
            "disabled",
            "eager",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "filter",  # JS functions unimplemented
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_no_data",
            "hide_selected",
            "hide_spin_buttons",
            "hint",
            "id",
            "item_color",
            "item_disabled",  # JS functions unimplemented
            "item_text",  # JS functions unimplemented
            "item_value",  # JS functions unimplemented
            "items",
            "label",
            "light",
            "loader_height",
            "loading",
            "menu_props",
            "messages",
            "multiple",
            "no_data_text",
            "no_filter",
            "open_on_clear",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "return_object",
            "reverse",
            "rounded",
            "rules",
            "search_input",
            "shaped",
            "single_line",
            "small_chips",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
            ("update_list_index", "update:list-index"),
            ("update_search_input", "update:search-input"),
        ]


class VDataIterator(AbstractElement):

    """
    Vuetify's VDataIterator component. See more info and examples |VDataIterator_vuetify_link|.

    .. |VDataIterator_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-data-iterator" target="_blank">here</a>


    :param checkbox_color:
    :type string:
    :param custom_filter: Function to filter items
    :type function:
    :param custom_group: Function used to group items
    :type function:
    :param custom_sort: Function used to sort items
    :type function:
    :param dark: See description |VDataIterator_vuetify_link|.
    :type boolean:
    :param disable_filtering: Disables filtering completely
    :type boolean:
    :param disable_pagination: Disables pagination completely
    :type boolean:
    :param disable_sort: Disables sorting completely
    :type boolean:
    :param expanded: Array of expanded items. Can be used with `.sync` modifier
    :type array:
    :param footer_props: See description |VDataIterator_vuetify_link|.
    :type object:
    :param group_by: Changes which item property should be used for grouping items. Currently only supports a single grouping in the format: `group` or `['group']`. When using an array, only the first element is considered. Can be used with `.sync` modifier
    :type ['string', 'array']:
    :param group_desc: Changes which direction grouping is done. Can be used with `.sync` modifier
    :type ['boolean', 'array']:
    :param hide_default_footer: Hides default footer
    :type boolean:
    :param item_key: The property on each item that is used as a unique key
    :type string:
    :param items: The array of items to display
    :type array:
    :param items_per_page: Changes how many items per page should be visible. Can be used with `.sync` modifier. Setting this prop to `-1` will display all items on the page
    :type number:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loading: If `true` and no items are provided, then a loading text will be shown
    :type ['boolean', 'string']:
    :param loading_text: Text shown when `loading` is true and no items are provided
    :type string:
    :param locale: See description |VDataIterator_vuetify_link|.
    :type string:
    :param mobile_breakpoint: Used to set when to toggle between regular table and mobile view
    :type ['number', 'string']:
    :param multi_sort: If `true` then one can sort on multiple properties
    :type boolean:
    :param must_sort: If `true` then one can not disable sorting, it will always switch between ascending and descending
    :type boolean:
    :param no_data_text: Text shown when no items are provided to the component
    :type string:
    :param no_results_text: Text shown when `search` prop is used and there are no results
    :type string:
    :param options:
    :type DataOptions:
    :param page:
    :type number:
    :param search: Text input used to filter items
    :type string:
    :param selectable_key: The property on each item that is used to determine if it is selectable or not
    :type string:
    :param server_items_length: Used only when data is provided by a server. Should be set to the total amount of items available on server so that pagination works correctly
    :type number:
    :param single_expand: Changes expansion mode to single expand
    :type boolean:
    :param single_select: Changes selection mode to single select
    :type boolean:
    :param sort_by: Changes which item property (or properties) should be used for sort order. Can be used with `.sync` modifier
    :type ['string', 'array']:
    :param sort_desc: Changes which direction sorting is done. Can be used with `.sync` modifier
    :type ['boolean', 'array']:
    :param value: Used for controlling selected rows
    :type array:

    Events

    :param current_items: Emits the items provided via the **items** prop, every time the internal **computedItems** is changed.
    :param input: Array of selected items
    :param item_expanded: Event emitted when an item is expanded or closed
    :param item_selected: Event emitted when an item is selected or deselected
    :param page_count: Emits when the **pageCount** property of the **pagination** prop is updated
    :param pagination: Emits when something changed to the `pagination` which can be provided via the `pagination` prop
    :param toggle_select_all: Emits when the `select-all` checkbox in table header is clicked. This checkbox is enabled by the **show-select** prop
    :param update_expanded: The `.sync` event for `expanded` prop
    :param update_group_by: Emits when the **group-by** property of the **options** property is updated
    :param update_group_desc: Emits when the **group-desc** property of the **options** prop is updated
    :param update_items_per_page: Emits when the **items-per-page** property of the **options** prop is updated
    :param update_multi_sort: Emits when the **multi-sort** property of the **options** prop is updated
    :param update_must_sort: Emits when the **must-sort** property of the **options** prop is updated
    :param update_options: Emits when one of the **options** properties is updated
    :param update_page: Emits when the **page** property of the **options** prop is updated
    :param update_sort_by: Emits when the **sort-by** property of the **options** prop is updated
    :param update_sort_desc: Emits when the **sort-desc** property of the **options** prop is updated
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-data-iterator", children, **kwargs)
        self._attr_names += [
            "checkbox_color",
            "custom_filter",  # JS functions unimplemented
            "custom_group",  # JS functions unimplemented
            "custom_sort",  # JS functions unimplemented
            "dark",
            "disable_filtering",
            "disable_pagination",
            "disable_sort",
            "expanded",
            "footer_props",
            "group_by",
            "group_desc",
            "hide_default_footer",
            "item_key",
            "items",
            "items_per_page",
            "light",
            "loading",
            "loading_text",
            "locale",
            "mobile_breakpoint",
            "multi_sort",
            "must_sort",
            "no_data_text",
            "no_results_text",
            "options",
            "page",
            "search",
            "selectable_key",
            "server_items_length",
            "single_expand",
            "single_select",
            "sort_by",
            "sort_desc",
            "value",
        ]
        self._event_names += [
            ("current_items", "current-items"),
            "input",
            ("item_expanded", "item-expanded"),
            ("item_selected", "item-selected"),
            ("page_count", "page-count"),
            "pagination",
            ("toggle_select_all", "toggle-select-all"),
            ("update_expanded", "update:expanded"),
            ("update_group_by", "update:group-by"),
            ("update_group_desc", "update:group-desc"),
            ("update_items_per_page", "update:items-per-page"),
            ("update_multi_sort", "update:multi-sort"),
            ("update_must_sort", "update:must-sort"),
            ("update_options", "update:options"),
            ("update_page", "update:page"),
            ("update_sort_by", "update:sort-by"),
            ("update_sort_desc", "update:sort-desc"),
        ]


class VDataFooter(AbstractElement):

    """
    Vuetify's VDataFooter component. See more info and examples |VDataFooter_vuetify_link|.

    .. |VDataFooter_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-data-footer" target="_blank">here</a>


    :param disable_items_per_page: Disables items-per-page dropdown
    :type boolean:
    :param disable_pagination: Disables pagination buttons
    :type boolean:
    :param first_icon: First icon
    :type string:
    :param items_per_page_all_text: Text for 'All' option in items-per-page dropdown
    :type string:
    :param items_per_page_options: Array of options to show in the items-per-page dropdown
    :type array:
    :param items_per_page_text: Text for items-per-page dropdown
    :type string:
    :param last_icon: Last icon
    :type string:
    :param next_icon: Next icon
    :type string:
    :param options: DataOptions
    :type object:
    :param page_text:
    :type string:
    :param pagination: DataPagination
    :type object:
    :param prev_icon: Previous icon
    :type string:
    :param show_current_page: Show current page number between prev/next icons
    :type boolean:
    :param show_first_last_page: Show first/last icons
    :type boolean:

    Events

    :param update_options: The `.sync` event for `options` prop
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-data-footer", children, **kwargs)
        self._attr_names += [
            "disable_items_per_page",
            "disable_pagination",
            "first_icon",
            "items_per_page_all_text",
            "items_per_page_options",
            "items_per_page_text",
            "last_icon",
            "next_icon",
            "options",
            "page_text",
            "pagination",
            "prev_icon",
            "show_current_page",
            "show_first_last_page",
        ]
        self._event_names += [
            ("update_options", "update:options"),
        ]


class VDataTable(AbstractElement):

    """
    Vuetify's VDataTable component. See more info and examples |VDataTable_vuetify_link|.

    .. |VDataTable_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-data-table" target="_blank">here</a>


    :param calculate_widths: Enables calculation of column widths. `widths` property will be available in select scoped slots
    :type boolean:
    :param caption: Set the caption (using `<caption>`)
    :type string:
    :param checkbox_color: Set the color of the checkboxes (showSelect must be used)
    :type string:
    :param custom_filter: Function to filter items
    :type function:
    :param custom_group: Function used to group items
    :type function:
    :param custom_sort: Function used to sort items
    :type function:
    :param dark: See description |VDataTable_vuetify_link|.
    :type boolean:
    :param dense: Decreases the height of rows
    :type boolean:
    :param disable_filtering: Disables filtering completely
    :type boolean:
    :param disable_pagination: Disables pagination completely
    :type boolean:
    :param disable_sort: Disables sorting completely
    :type boolean:
    :param expand_icon: Icon used for expand toggle button.
    :type string:
    :param expanded: Array of expanded items. Can be used with `.sync` modifier
    :type array:
    :param fixed_header: Fixed header to top of table. **NOTE:** Does not work in IE11
    :type boolean:
    :param footer_props: See description |VDataTable_vuetify_link|.
    :type object:
    :param group_by: Changes which item property should be used for grouping items. Currently only supports a single grouping in the format: `group` or `['group']`. When using an array, only the first element is considered. Can be used with `.sync` modifier
    :type ['string', 'array']:
    :param group_desc: Changes which direction grouping is done. Can be used with `.sync` modifier
    :type ['boolean', 'array']:
    :param header_props: See description |VDataTable_vuetify_link|.
    :type object:
    :param headers: An array of objects that each describe a header column. See the example below for a definition of all properties
    :type DataTableHeader[]:
    :param headers_length: Can be used in combination with `hide-default-header` to specify the number of columns in the table to allow expansion rows and loading bar to function properly
    :type number:
    :param height: Set an explicit height of table
    :type ['number', 'string']:
    :param hide_default_footer: Hides default footer
    :type boolean:
    :param hide_default_header: Hide the default headers
    :type boolean:
    :param item_class: Property on supplied `items` that contains item's row class or function that takes an item as an argument and returns the class of corresponding row
    :type ['string', 'function']:
    :param item_key: The property on each item that is used as a unique key
    :type string:
    :param items: The array of items to display
    :type array:
    :param items_per_page: Changes how many items per page should be visible. Can be used with `.sync` modifier. Setting this prop to `-1` will display all items on the page
    :type number:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: If `true` and no items are provided, then a loading text will be shown
    :type ['boolean', 'string']:
    :param loading_text: Text shown when `loading` is true and no items are provided
    :type string:
    :param locale: See description |VDataTable_vuetify_link|.
    :type string:
    :param mobile_breakpoint: Used to set when to toggle between regular table and mobile view
    :type ['number', 'string']:
    :param multi_sort: If `true` then one can sort on multiple properties
    :type boolean:
    :param must_sort: If `true` then one can not disable sorting, it will always switch between ascending and descending
    :type boolean:
    :param no_data_text: Text shown when no items are provided to the component
    :type string:
    :param no_results_text: Text shown when `search` prop is used and there are no results
    :type string:
    :param options:
    :type DataOptions:
    :param page: The current displayed page number (1-indexed)
    :type number:
    :param search: Text input used to filter items
    :type string:
    :param selectable_key: The property on each item that is used to determine if it is selectable or not
    :type string:
    :param server_items_length: Used only when data is provided by a server. Should be set to the total amount of items available on server so that pagination works correctly
    :type number:
    :param show_expand: Shows the expand toggle in default rows
    :type boolean:
    :param show_group_by: Shows the group by toggle in the header and enables grouped rows
    :type boolean:
    :param show_select: Shows the select checkboxes in both the header and rows (if using default rows)
    :type boolean:
    :param single_expand: Changes expansion mode to single expand
    :type boolean:
    :param single_select: Changes selection mode to single select
    :type boolean:
    :param sort_by: Changes which item property (or properties) should be used for sort order. Can be used with `.sync` modifier
    :type ['string', 'array']:
    :param sort_desc: Changes which direction sorting is done. Can be used with `.sync` modifier
    :type ['boolean', 'array']:
    :param value: Used for controlling selected rows
    :type array:

    Events

    :param click_row: Emits when a table row is clicked. This event provides 2 arguments: the first is the item data that was clicked and the second is the other related data provided by the `item` slot. **NOTE:** will not emit when table rows are defined through a slot such as `item` or `body`.
    :param contextmenu_row: Emits when a table row is right-clicked. The item for the row is included. **NOTE:** will not emit when table rows are defined through a slot such as `item` or `body`.
    :param current_items: Emits the items provided via the **items** prop, every time the internal **computedItems** is changed.
    :param dblclick_row: Emits when a table row is double-clicked. The item for the row is included. **NOTE:** will not emit when table rows are defined through a slot such as `item` or `body`.
    :param input: Array of selected items
    :param item_expanded: Event emitted when an item is expanded or closed
    :param item_selected: Event emitted when an item is selected or deselected
    :param page_count: Emits when the **pageCount** property of the **pagination** prop is updated
    :param pagination: Emits when something changed to the `pagination` which can be provided via the `pagination` prop
    :param toggle_select_all: Emits when the `select-all` checkbox in table header is clicked. This checkbox is enabled by the **show-select** prop
    :param update_expanded: The `.sync` event for `expanded` prop
    :param update_group_by: Emits when the **group-by** property of the **options** property is updated
    :param update_group_desc: Emits when the **group-desc** property of the **options** prop is updated
    :param update_items_per_page: Emits when the **items-per-page** property of the **options** prop is updated
    :param update_multi_sort: Emits when the **multi-sort** property of the **options** prop is updated
    :param update_must_sort: Emits when the **must-sort** property of the **options** prop is updated
    :param update_options: Emits when one of the **options** properties is updated
    :param update_page: Emits when the **page** property of the **options** prop is updated
    :param update_sort_by: Emits when the **sort-by** property of the **options** prop is updated
    :param update_sort_desc: Emits when the **sort-desc** property of the **options** prop is updated
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-data-table", children, **kwargs)
        self.ttsSensitive()
        self._attr_names += [
            "calculate_widths",
            "caption",
            "checkbox_color",
            "custom_filter",  # JS functions unimplemented
            "custom_group",  # JS functions unimplemented
            "custom_sort",  # JS functions unimplemented
            "dark",
            "dense",
            "disable_filtering",
            "disable_pagination",
            "disable_sort",
            "expand_icon",
            "expanded",
            "fixed_header",
            "footer_props",
            "group_by",
            "group_desc",
            "header_props",
            "headers",
            "headers_length",
            "height",
            "hide_default_footer",
            "hide_default_header",
            "item_class",  # JS functions unimplemented
            "item_key",
            "items",
            "items_per_page",
            "light",
            "loader_height",
            "loading",
            "loading_text",
            "locale",
            "mobile_breakpoint",
            "multi_sort",
            "must_sort",
            "no_data_text",
            "no_results_text",
            "options",
            "page",
            "search",
            "selectable_key",
            "server_items_length",
            "show_expand",
            "show_group_by",
            "show_select",
            "single_expand",
            "single_select",
            "sort_by",
            "sort_desc",
            "value",
        ]
        self._event_names += [
            ("click_row", "click:row"),
            ("contextmenu_row", "contextmenu:row"),
            ("current_items", "current-items"),
            ("dblclick_row", "dblclick:row"),
            "input",
            ("item_expanded", "item-expanded"),
            ("item_selected", "item-selected"),
            ("page_count", "page-count"),
            "pagination",
            ("toggle_select_all", "toggle-select-all"),
            ("update_expanded", "update:expanded"),
            ("update_group_by", "update:group-by"),
            ("update_group_desc", "update:group-desc"),
            ("update_items_per_page", "update:items-per-page"),
            ("update_multi_sort", "update:multi-sort"),
            ("update_must_sort", "update:must-sort"),
            ("update_options", "update:options"),
            ("update_page", "update:page"),
            ("update_sort_by", "update:sort-by"),
            ("update_sort_desc", "update:sort-desc"),
        ]


class VEditDialog(AbstractElement):

    """
    Vuetify's VEditDialog component. See more info and examples |VEditDialog_vuetify_link|.

    .. |VEditDialog_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-edit-dialog" target="_blank">here</a>


    :param cancel_text: Sets the default text for the cancel button when using the **large** prop
    :type any:
    :param dark: See description |VEditDialog_vuetify_link|.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param large: Attaches a submit and cancel button to the dialog
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param persistent: Clicking outside or pressing **esc** key will not dismiss the dialog
    :type boolean:
    :param return_value:
    :type any:
    :param save_text: Sets the default text for the save button when using the **large** prop
    :type any:
    :param transition: See description |VEditDialog_vuetify_link|.
    :type string:

    Events

    :param cancel: Emits when editing is canceled
    :param close: Emits when edit-dialog close button is pressed
    :param open: Emits when editing is opened
    :param save: Emits when edit-dialog save button is pressed
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-edit-dialog", children, **kwargs)
        self._attr_names += [
            "cancel_text",
            "dark",
            "eager",
            "large",
            "light",
            "persistent",
            "return_value",
            "save_text",
            "transition",
        ]
        self._event_names += [
            "cancel",
            "close",
            "open",
            "save",
        ]


class VDataTableHeader(AbstractElement):

    """
    Vuetify's VDataTableHeader component. See more info and examples |VDataTableHeader_vuetify_link|.

    .. |VDataTableHeader_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-data-table-header" target="_blank">here</a>


    :param checkbox_color:
    :type string:
    :param disable_sort: Toggles rendering of sort button
    :type boolean:
    :param every_item: Indicates if all items in table are selected
    :type boolean:
    :param headers: Array of header items to display
    :type array:
    :param mobile: Renders mobile view of headers
    :type boolean:
    :param options: Options object. Identical to the one on `v-data-table`
    :type object:
    :param show_group_by: Shows group by button
    :type boolean:
    :param single_select: Toggles rendering of select-all checkbox
    :type boolean:
    :param some_items: Indicates if one or more items in table are selected
    :type boolean:
    :param sort_by_text: Sets the label text used by the default sort-by selector when `v-data-table` is rendering the mobile view
    :type string:
    :param sort_icon: Icon used for sort button
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-data-table-header", children, **kwargs)
        self._attr_names += [
            "checkbox_color",
            "disable_sort",
            "every_item",
            "headers",
            "mobile",
            "options",
            "show_group_by",
            "single_select",
            "some_items",
            "sort_by_text",
            "sort_icon",
        ]


class VSimpleTable(AbstractElement):

    """
    Vuetify's VSimpleTable component. See more info and examples |VSimpleTable_vuetify_link|.

    .. |VSimpleTable_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-simple-table" target="_blank">here</a>


    :param dark: See description |VSimpleTable_vuetify_link|.
    :type boolean:
    :param dense: Decreases paddings to render a dense table
    :type boolean:
    :param fixed_header: Sets table header to fixed mode
    :type boolean:
    :param height: Sets the height for the component
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-simple-table", children, **kwargs)
        self._attr_names += [
            "dark",
            "dense",
            "fixed_header",
            "height",
            "light",
        ]


class VDatePicker(AbstractElement):

    """
    Vuetify's VDatePicker component. See more info and examples |VDatePicker_vuetify_link|.

    .. |VDatePicker_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-date-picker" target="_blank">here</a>


    :param active_picker: Determines which picker in the date or month picker is being displayed. Allowed values: `'DATE'`, `'MONTH'`, `'YEAR'`
    :type string:
    :param allowed_dates: Restricts which dates can be selected
    :type function:
    :param color: See description |VDatePicker_vuetify_link|.
    :type string:
    :param dark: See description |VDatePicker_vuetify_link|.
    :type boolean:
    :param day_format: Allows you to customize the format of the day string that appears in the date table. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param disabled: Disables interaction with the picker
    :type boolean:
    :param elevation: See description |VDatePicker_vuetify_link|.
    :type ['number', 'string']:
    :param event_color: Sets the color for event dot. It can be string (all events will have the same color) or `object` where attribute is the event date and value is boolean/color/array of colors for specified date or `function` taking date as a parameter and returning boolean/color/array of colors for that date
    :type ['array', 'function', 'object', 'string']:
    :param events: Array of dates or object defining events or colors or function returning boolean/color/array of colors
    :type ['array', 'function', 'object']:
    :param first_day_of_week: Sets the first day of the week, starting with 0 for Sunday.
    :type ['string', 'number']:
    :param flat: Removes  elevation
    :type boolean:
    :param full_width: Forces 100% width
    :type boolean:
    :param header_color: Defines the header color. If not specified it will use the color defined by <code>color</code> prop or the default picker color
    :type string:
    :param header_date_format: Allows you to customize the format of the month string that appears in the header of the calendar. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param landscape: Orients picker horizontal
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param locale: Sets the locale. Accepts a string with a BCP 47 language tag.
    :type string:
    :param locale_first_day_of_year: Sets the day that determines the first week of the year, starting with 0 for **Sunday**. For ISO 8601 this should be 4.
    :type ['string', 'number']:
    :param max: Maximum allowed date/month (ISO 8601 format)
    :type string:
    :param min: Minimum allowed date/month (ISO 8601 format)
    :type string:
    :param month_format: Formatting function used for displaying months in the months table. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param multiple: Allow the selection of multiple dates
    :type boolean:
    :param next_icon: Sets the icon for next month/year button
    :type string:
    :param next_month_aria_label:
    :type string:
    :param next_year_aria_label:
    :type string:
    :param no_title: Hide the picker title
    :type boolean:
    :param picker_date: Displayed year/month
    :type string:
    :param prev_icon: Sets the icon for previous month/year button
    :type string:
    :param prev_month_aria_label:
    :type string:
    :param prev_year_aria_label:
    :type string:
    :param range: Allow the selection of date range
    :type boolean:
    :param reactive: Updates the picker model when changing months/years automatically
    :type boolean:
    :param readonly: Makes the picker readonly (doesn't allow to select new date)
    :type boolean:
    :param scrollable: Allows changing displayed month with mouse scroll
    :type boolean:
    :param selected_items_text: See description |VDatePicker_vuetify_link|.
    :type string:
    :param show_adjacent_months: Toggles visibility of days from previous and next months
    :type boolean:
    :param show_current: Toggles visibility of the current date/month outline or shows the provided date/month as a current
    :type ['boolean', 'string']:
    :param show_week: Toggles visibility of the week numbers in the body of the calendar
    :type boolean:
    :param title_date_format: Allows you to customize the format of the date string that appears in the title of the date picker. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param type: Determines the type of the picker - `date` for date picker, `month` for month picker
    :type string:
    :param value: Date picker model (ISO 8601 format, YYYY-mm-dd or YYYY-mm)
    :type ['array', 'string']:
    :param weekday_format: Allows you to customize the format of the weekday string that appears in the body of the calendar. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param width: Width of the picker
    :type ['number', 'string']:
    :param year_format: Allows you to customize the format of the year string that appears in the header of the calendar. Called with date (ISO 8601 **date** string) arguments.
    :type function:
    :param year_icon: Sets the icon in the year selection button
    :type string:

    Events

    :param change: Reactive date picker emits `input` even when any part of the date (year/month/day) changes, but `change` event is emitted only when the day (for date pickers) or month (for month pickers) changes. If `range` prop is set, date picker emits `change` when both [from, to] are selected.
    :param input: The updated bound model
    :param update_active_picker: The `.sync` event for `active-picker` prop
    :param update_picker_date: The `.sync` event for `picker-date` prop
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-date-picker", children, **kwargs)
        self._attr_names += [
            "active_picker",
            "allowed_dates",  # JS functions unimplemented
            "color",
            "dark",
            "day_format",  # JS functions unimplemented
            "disabled",
            "elevation",
            "event_color",  # JS functions unimplemented
            "events",  # JS functions unimplemented
            "first_day_of_week",
            "flat",
            "full_width",
            "header_color",
            "header_date_format",  # JS functions unimplemented
            "landscape",
            "light",
            "locale",
            "locale_first_day_of_year",
            "max",
            "min",
            "month_format",  # JS functions unimplemented
            "multiple",
            "next_icon",
            "next_month_aria_label",
            "next_year_aria_label",
            "no_title",
            "picker_date",
            "prev_icon",
            "prev_month_aria_label",
            "prev_year_aria_label",
            "range",
            "reactive",
            "readonly",
            "scrollable",
            "selected_items_text",
            "show_adjacent_months",
            "show_current",
            "show_week",
            "title_date_format",  # JS functions unimplemented
            "type",
            "value",
            "weekday_format",  # JS functions unimplemented
            "width",
            "year_format",  # JS functions unimplemented
            "year_icon",
        ]
        self._event_names += [
            ("click_date", "click:date"),
            ("click_month", "click:month"),
            ("click_year", "click:year"),
            ("dblclick_date", "dblclick:date"),
            ("dblclick_month", "dblclick:month"),
            ("dblclick_year", "dblclick:year"),
            ("mousedown_date", "mousedown:date"),
            ("mousedown_month", "mousedown:month"),
            ("mousedown_year", "mousedown:year"),
            ("mouseenter_date", "mouseenter:date"),
            ("mouseenter_month", "mouseenter:month"),
            ("mouseenter_year", "mouseenter:year"),
            ("mouseleave_date", "mouseleave:date"),
            ("mouseleave_month", "mouseleave:month"),
            ("mouseleave_year", "mouseleave:year"),
            ("mousemove_date", "mousemove:date"),
            ("mousemove_month", "mousemove:month"),
            ("mousemove_year", "mousemove:year"),
            ("mouseover_date", "mouseover:date"),
            ("mouseover_month", "mouseover:month"),
            ("mouseover_year", "mouseover:year"),
            ("mouseout_date", "mouseout:date"),
            ("mouseout_month", "mouseout:month"),
            ("mouseout_year", "mouseout:year"),
            ("mouseup_date", "mouseup:date"),
            ("mouseup_month", "mouseup:month"),
            ("mouseup_year", "mouseup:year"),
            ("focus_date", "focus:date"),
            ("focus_month", "focus:month"),
            ("focus_year", "focus:year"),
            ("click_date", "click:date"),
            ("click_month", "click:month"),
            ("click_year", "click:year"),
            ("dblclick_date", "dblclick:date"),
            ("dblclick_month", "dblclick:month"),
            ("dblclick_year", "dblclick:year"),
            ("mousedown_date", "mousedown:date"),
            ("mousedown_month", "mousedown:month"),
            ("mousedown_year", "mousedown:year"),
            ("mouseenter_date", "mouseenter:date"),
            ("mouseenter_month", "mouseenter:month"),
            ("mouseenter_year", "mouseenter:year"),
            ("mouseleave_date", "mouseleave:date"),
            ("mouseleave_month", "mouseleave:month"),
            ("mouseleave_year", "mouseleave:year"),
            ("mousemove_date", "mousemove:date"),
            ("mousemove_month", "mousemove:month"),
            ("mousemove_year", "mousemove:year"),
            ("mouseover_date", "mouseover:date"),
            ("mouseover_month", "mouseover:month"),
            ("mouseover_year", "mouseover:year"),
            ("mouseout_date", "mouseout:date"),
            ("mouseout_month", "mouseout:month"),
            ("mouseout_year", "mouseout:year"),
            ("mouseup_date", "mouseup:date"),
            ("mouseup_month", "mouseup:month"),
            ("mouseup_year", "mouseup:year"),
            ("focus_date", "focus:date"),
            ("focus_month", "focus:month"),
            ("focus_year", "focus:year"),
            ("click_date", "click:date"),
            ("click_month", "click:month"),
            ("click_year", "click:year"),
            ("dblclick_date", "dblclick:date"),
            ("dblclick_month", "dblclick:month"),
            ("dblclick_year", "dblclick:year"),
            ("mousedown_date", "mousedown:date"),
            ("mousedown_month", "mousedown:month"),
            ("mousedown_year", "mousedown:year"),
            ("mouseenter_date", "mouseenter:date"),
            ("mouseenter_month", "mouseenter:month"),
            ("mouseenter_year", "mouseenter:year"),
            ("mouseleave_date", "mouseleave:date"),
            ("mouseleave_month", "mouseleave:month"),
            ("mouseleave_year", "mouseleave:year"),
            ("mousemove_date", "mousemove:date"),
            ("mousemove_month", "mousemove:month"),
            ("mousemove_year", "mousemove:year"),
            ("mouseover_date", "mouseover:date"),
            ("mouseover_month", "mouseover:month"),
            ("mouseover_year", "mouseover:year"),
            ("mouseout_date", "mouseout:date"),
            ("mouseout_month", "mouseout:month"),
            ("mouseout_year", "mouseout:year"),
            ("mouseup_date", "mouseup:date"),
            ("mouseup_month", "mouseup:month"),
            ("mouseup_year", "mouseup:year"),
            ("focus_date", "focus:date"),
            ("focus_month", "focus:month"),
            ("focus_year", "focus:year"),
            "change",
            "input",
            ("update_active_picker", "update:active-picker"),
            ("update_picker_date", "update:picker-date"),
        ]


class VDialog(AbstractElement):

    """
    Vuetify's VDialog component. See more info and examples |VDialog_vuetify_link|.

    .. |VDialog_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-dialog" target="_blank">here</a>


    :param activator: Designate a custom activator when the `activator` slot is not used. String can be any valid querySelector and Object can be any valid Node.
    :type any:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param close_delay: Milliseconds to wait before closing component.
    :type ['number', 'string']:
    :param content_class: Applies a custom class to the detached element. This is useful because the content is moved to the beginning of the `v-app` component (unless the **attach** prop is provided) and is not targetable by classes passed directly on the component.
    :type string:
    :param dark: See description |VDialog_vuetify_link|.
    :type boolean:
    :param disabled: Disables the ability to open the component.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param fullscreen: Changes layout for fullscreen display.
    :type boolean:
    :param hide_overlay: Hides the display of the overlay.
    :type boolean:
    :param internal_activator: Detaches the menu content inside of the component as opposed to the document.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_width: Sets the maximum width for the component.
    :type ['string', 'number']:
    :param no_click_animation: Disables the bounce effect when clicking outside of a `v-dialog`'s content when using the **persistent** prop.
    :type boolean:
    :param open_delay: Milliseconds to wait before opening component.
    :type ['number', 'string']:
    :param open_on_focus:
    :type boolean:
    :param open_on_hover: Designates whether component should activate when its activator is hovered.
    :type boolean:
    :param origin: See description |VDialog_vuetify_link|.
    :type string:
    :param overlay_color: Sets the overlay color.
    :type string:
    :param overlay_opacity: Sets the overlay opacity.
    :type ['number', 'string']:
    :param persistent: Clicking outside of the element or pressing **esc** key will not deactivate it.
    :type boolean:
    :param retain_focus: Tab focus will return to the first child of the dialog by default. Disable this when using external tools that require focus such as TinyMCE or vue-clipboard.
    :type boolean:
    :param return_value:
    :type any:
    :param scrollable: See description |VDialog_vuetify_link|.
    :type boolean:
    :param transition: See description |VDialog_vuetify_link|.
    :type ['string', 'boolean']:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param width: Sets the width for the component.
    :type ['string', 'number']:

    Events

    :param click_outside: Event that fires when clicking outside an active dialog.
    :param input: The updated bound model
    :param keydown: Event that fires when key is pressed. If dialog is active and not using the **persistent** prop, the **esc** key will deactivate it.
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-dialog", children, **kwargs)
        self._attr_names += [
            "activator",
            "attach",
            "close_delay",
            "content_class",
            "dark",
            "disabled",
            "eager",
            "fullscreen",
            "hide_overlay",
            "internal_activator",
            "light",
            "max_width",
            "no_click_animation",
            "open_delay",
            "open_on_focus",
            "open_on_hover",
            "origin",
            "overlay_color",
            "overlay_opacity",
            "persistent",
            "retain_focus",
            "return_value",
            "scrollable",
            "transition",
            "value",
            "width",
        ]
        self._event_names += [
            ("click_outside", "click:outside"),
            "input",
            "keydown",
        ]


class VDivider(AbstractElement):

    """
    Vuetify's VDivider component. See more info and examples |VDivider_vuetify_link|.

    .. |VDivider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-divider" target="_blank">here</a>


    :param dark: See description |VDivider_vuetify_link|.
    :type boolean:
    :param inset: Adds indentation (72px) for **normal** dividers, reduces max height for **vertical**.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param vertical: Displays dividers vertically
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-divider", children, **kwargs)
        self._attr_names += [
            "dark",
            "inset",
            "light",
            "vertical",
        ]


class VExpansionPanels(AbstractElement):

    """
    Vuetify's VExpansionPanels component. See more info and examples |VExpansionPanels_vuetify_link|.

    .. |VExpansionPanels_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expansion-panels" target="_blank">here</a>


    :param accordion: Removes the margin around open panels
    :type boolean:
    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param dark: See description |VExpansionPanels_vuetify_link|.
    :type boolean:
    :param disabled: Disables the entire expansion-panel
    :type boolean:
    :param flat: Removes the expansion-panel's elevation and borders
    :type boolean:
    :param focusable: Makes the expansion-panel headers focusable
    :type boolean:
    :param hover: Applies a background-color shift on hover to expansion panel headers
    :type boolean:
    :param inset: Makes the expansion-panel open with a inset style
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param popout: Makes the expansion-panel open with an popout style
    :type boolean:
    :param readonly: Makes the entire expansion-panel read only.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the border-radius
    :type boolean:
    :param value: Controls the opened/closed state of content in the expansion-panel. Corresponds to a zero-based index of the currently opened content. If the `multiple` prop (previously `expand` in 1.5.x) is used then it is an array of numbers where each entry corresponds to the index of the opened content.  The index order is not relevant.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expansion-panels", children, **kwargs)
        self._attr_names += [
            "accordion",
            "active_class",
            "dark",
            "disabled",
            "flat",
            "focusable",
            "hover",
            "inset",
            "light",
            "mandatory",
            "max",
            "multiple",
            "popout",
            "readonly",
            "tag",
            "tile",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]


class VExpansionPanel(AbstractElement):

    """
    Vuetify's VExpansionPanel component. See more info and examples |VExpansionPanel_vuetify_link|.

    .. |VExpansionPanel_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expansion-panel" target="_blank">here</a>


    :param active_class: See description |VExpansionPanel_vuetify_link|.
    :type string:
    :param disabled: Disables the expansion-panel content
    :type boolean:
    :param readonly: Makes the expansion-panel content read only.
    :type boolean:

    Events

    :param change: Toggles the value of the selected panel
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expansion-panel", children, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "readonly",
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
        ]


class VExpansionPanelHeader(AbstractElement):

    """
    Vuetify's VExpansionPanelHeader component. See more info and examples |VExpansionPanelHeader_vuetify_link|.

    .. |VExpansionPanelHeader_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expansion-panel-header" target="_blank">here</a>


    :param color: See description |VExpansionPanelHeader_vuetify_link|.
    :type string:
    :param disable_icon_rotate: Removes the icon rotation animation when expanding a panel
    :type boolean:
    :param expand_icon: Set the expand action icon
    :type string:
    :param hide_actions: Hide the expand icon in the content header
    :type boolean:
    :param ripple: See description |VExpansionPanelHeader_vuetify_link|.
    :type ['boolean', 'object']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expansion-panel-header", children, **kwargs)
        self._attr_names += [
            "color",
            "disable_icon_rotate",
            "expand_icon",
            "hide_actions",
            "ripple",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
        ]


class VExpansionPanelContent(AbstractElement):

    """
    Vuetify's VExpansionPanelContent component. See more info and examples |VExpansionPanelContent_vuetify_link|.

    .. |VExpansionPanelContent_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expansion-panel-content" target="_blank">here</a>


    :param color: See description |VExpansionPanelContent_vuetify_link|.
    :type string:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expansion-panel-content", children, **kwargs)
        self._attr_names += [
            "color",
            "eager",
        ]


class VFileInput(AbstractElement):

    """
    Vuetify's VFileInput component. See more info and examples |VFileInput_vuetify_link|.

    .. |VFileInput_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-file-input" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param chips: Changes display of selections to chips
    :type boolean:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VFileInput_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_size_string: See description |VFileInput_vuetify_link|.
    :type string:
    :param counter_string: See description |VFileInput_vuetify_link|.
    :type string:
    :param counter_value:
    :type function:
    :param dark: See description |VFileInput_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_input: Display the icon only without the input (file names)
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Adds the **multiple** attribute to the input, allowing multiple file selections.
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param show_size: Sets the displayed size of selected file(s). When using **true** will default to _1000_ displaying (**kB, MB, GB**) while _1024_ will display (**KiB, MiB, GiB**).
    :type ['boolean', 'number']:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param small_chips: Changes display of selections to chips with the **small** property
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param truncate_length: The length of a filename before it is truncated with ellipsis
    :type ['number', 'string']:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: See description |VFileInput_vuetify_link|.
    :type any:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-file-input", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "append_outer_icon",
            "autofocus",
            "background_color",
            "chips",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_size_string",
            "counter_string",
            "counter_value",  # JS functions unimplemented
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_input",
            "hide_spin_buttons",
            "hint",
            "id",
            "label",
            "light",
            "loader_height",
            "loading",
            "messages",
            "multiple",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "reverse",
            "rounded",
            "rules",
            "shaped",
            "show_size",
            "single_line",
            "small_chips",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "truncate_length",
            "type",
            "validate_on_blur",
            "value",
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VFooter(AbstractElement):

    """
    Vuetify's VFooter component. See more info and examples |VFooter_vuetify_link|.

    .. |VFooter_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-footer" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param app: See description |VFooter_vuetify_link|.
    :type boolean:
    :param color: See description |VFooter_vuetify_link|.
    :type string:
    :param dark: See description |VFooter_vuetify_link|.
    :type boolean:
    :param elevation: See description |VFooter_vuetify_link|.
    :type ['number', 'string']:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param inset: Positions the toolbar offset from an application `v-navigation-drawer`
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param padless: Remove all padding from the footer
    :type boolean:
    :param rounded: See description |VFooter_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-footer", children, **kwargs)
        self._attr_names += [
            "absolute",
            "app",
            "color",
            "dark",
            "elevation",
            "fixed",
            "height",
            "inset",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "outlined",
            "padless",
            "rounded",
            "shaped",
            "tag",
            "tile",
            "width",
        ]


class VForm(AbstractElement):

    """
    Vuetify's VForm component. See more info and examples |VForm_vuetify_link|.

    .. |VForm_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-form" target="_blank">here</a>


    :param disabled: Puts all children inputs into a disabled state.
    :type boolean:
    :param lazy_validation: If enabled, **value** will always be _true_ unless there are visible validation errors. You can still call `validate()` to manually trigger validation
    :type boolean:
    :param readonly: Puts all children inputs into a readonly state.
    :type boolean:
    :param value: A boolean value representing the validity of the form.
    :type boolean:

    Events

    :param input: The updated bound model
    :param submit: Emitted when form is submitted
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-form", children, **kwargs)
        self._attr_names += [
            "disabled",
            "lazy_validation",
            "readonly",
            "value",
        ]
        self._event_names += [
            "input",
            "submit",
        ]


class VContainer(AbstractElement):

    """
    Vuetify's VContainer component. See more info and examples |VContainer_vuetify_link|.

    .. |VContainer_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-container" target="_blank">here</a>


    :param fluid: Removes viewport maximum-width size breakpoints
    :type boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-container", children, **kwargs)
        self._attr_names += [
            "fluid",
            "id",
            "tag",
        ]


class VCol(AbstractElement):

    """
    Vuetify's VCol component. See more info and examples |VCol_vuetify_link|.

    .. |VCol_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-col" target="_blank">here</a>


    :param align_self: See description |VCol_vuetify_link|.
    :type string:
    :param cols: Sets the default number of columns the component extends. Available options are **1 -> 12** and **auto**.
    :type ['boolean', 'string', 'number']:
    :param lg: Changes the number of columns on large and greater breakpoints.
    :type ['boolean', 'string', 'number']:
    :param md: Changes the number of columns on medium and greater breakpoints.
    :type ['boolean', 'string', 'number']:
    :param offset: Sets the default offset for the column.
    :type ['string', 'number']:
    :param offset_lg: Changes the offset of the component on large and greater breakpoints.
    :type ['string', 'number']:
    :param offset_md: Changes the offset of the component on medium and greater breakpoints.
    :type ['string', 'number']:
    :param offset_sm: Changes the offset of the component on small and greater breakpoints.
    :type ['string', 'number']:
    :param offset_xl: Changes the offset of the component on extra large and greater breakpoints.
    :type ['string', 'number']:
    :param order: See description |VCol_vuetify_link|.
    :type ['string', 'number']:
    :param order_lg: Changes the order of the component on large and greater breakpoints.
    :type ['string', 'number']:
    :param order_md: Changes the order of the component on medium and greater breakpoints.
    :type ['string', 'number']:
    :param order_sm: Changes the order of the component on small and greater breakpoints.
    :type ['string', 'number']:
    :param order_xl: Changes the order of the component on extra large and greater breakpoints.
    :type ['string', 'number']:
    :param sm: Changes the number of columns on small and greater breakpoints.
    :type ['boolean', 'string', 'number']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param xl: Changes the number of columns on extra large and greater breakpoints.
    :type ['boolean', 'string', 'number']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-col", children, **kwargs)
        self._attr_names += [
            "align_self",
            "cols",
            "lg",
            "md",
            "offset",
            "offset_lg",
            "offset_md",
            "offset_sm",
            "offset_xl",
            "order",
            "order_lg",
            "order_md",
            "order_sm",
            "order_xl",
            "sm",
            "tag",
            "xl",
        ]


class VRow(AbstractElement):

    """
    Vuetify's VRow component. See more info and examples |VRow_vuetify_link|.

    .. |VRow_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-row" target="_blank">here</a>


    :param align: See description |VRow_vuetify_link|.
    :type string:
    :param align_content: See description |VRow_vuetify_link|.
    :type string:
    :param align_content_lg: Changes the **align-content** property on large and greater breakpoints.
    :type string:
    :param align_content_md: Changes the **align-content** property on medium and greater breakpoints.
    :type string:
    :param align_content_sm: Changes the **align-content** property on small and greater breakpoints.
    :type string:
    :param align_content_xl: Changes the **align-content** property on extra large and greater breakpoints.
    :type string:
    :param align_lg: Changes the **align-items** property on large and greater breakpoints.
    :type string:
    :param align_md: Changes the **align-items** property on medium and greater breakpoints.
    :type string:
    :param align_sm: Changes the **align-items** property on small and greater breakpoints.
    :type string:
    :param align_xl: Changes the **align-items** property on extra large and greater breakpoints.
    :type string:
    :param dense: Reduces the gutter between `v-col`s.
    :type boolean:
    :param justify: See description |VRow_vuetify_link|.
    :type string:
    :param justify_lg: Changes the **justify-content** property on large and greater breakpoints.
    :type string:
    :param justify_md: Changes the **justify-content** property on medium and greater breakpoints.
    :type string:
    :param justify_sm: Changes the **justify-content** property on small and greater breakpoints.
    :type string:
    :param justify_xl: Changes the **justify-content** property on extra large and greater breakpoints.
    :type string:
    :param no_gutters: Removes the gutter between `v-col`s.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-row", children, **kwargs)
        self._attr_names += [
            "align",
            "align_content",
            "align_content_lg",
            "align_content_md",
            "align_content_sm",
            "align_content_xl",
            "align_lg",
            "align_md",
            "align_sm",
            "align_xl",
            "dense",
            "justify",
            "justify_lg",
            "justify_md",
            "justify_sm",
            "justify_xl",
            "no_gutters",
            "tag",
        ]


class VSpacer(AbstractElement):

    """
    Vuetify's VSpacer component. See more info and examples |VSpacer_vuetify_link|.

    .. |VSpacer_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-spacer" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-spacer", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VLayout(AbstractElement):

    """
    Vuetify's VLayout component. See more info and examples |VLayout_vuetify_link|.

    .. |VLayout_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-layout" target="_blank">here</a>


    :param align_baseline:
    :type Boolean:
    :param align_center:
    :type Boolean:
    :param align_content_center:
    :type Boolean:
    :param align_content_end:
    :type Boolean:
    :param align_content_space_around:
    :type Boolean:
    :param align_content_space_between:
    :type Boolean:
    :param align_content_start:
    :type Boolean:
    :param align_end:
    :type Boolean:
    :param align_start:
    :type Boolean:
    :param column:
    :type boolean:
    :param d_{type}:
    :type Boolean:
    :param fill_height:
    :type Boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param justify_center:
    :type Boolean:
    :param justify_end:
    :type Boolean:
    :param justify_space_around:
    :type Boolean:
    :param justify_space_between:
    :type Boolean:
    :param justify_start:
    :type Boolean:
    :param reverse:
    :type boolean:
    :param row:
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type String:
    :param wrap:
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-layout", children, **kwargs)
        self._attr_names += [
            "align_baseline",
            "align_center",
            "align_content_center",
            "align_content_end",
            "align_content_space_around",
            "align_content_space_between",
            "align_content_start",
            "align_end",
            "align_start",
            "column",
            "d_{type}",
            "fill_height",
            "id",
            "justify_center",
            "justify_end",
            "justify_space_around",
            "justify_space_between",
            "justify_start",
            "reverse",
            "row",
            "tag",
            "wrap",
        ]


class VFlex(AbstractElement):

    """
    Vuetify's VFlex component. See more info and examples |VFlex_vuetify_link|.

    .. |VFlex_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-flex" target="_blank">here</a>


    :param (size)(1_12):
    :type boolean:
    :param align_self_baseline:
    :type boolean:
    :param align_self_center:
    :type boolean:
    :param align_self_end:
    :type boolean:
    :param align_self_start:
    :type boolean:
    :param grow:
    :type boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param offset_(size)(0_12):
    :type boolean:
    :param order_(size)(1_12):
    :type boolean:
    :param shrink:
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-flex", children, **kwargs)
        self._attr_names += [
            "sm1",
            "sm2",
            "sm3",
            "sm4",
            "sm5",
            "sm6",
            "sm7",
            "sm8",
            "sm9",
            "sm10",
            "sm11",
            "sm12",
            "md1",
            "md2",
            "md3",
            "md4",
            "md5",
            "md6",
            "md7",
            "md8",
            "md9",
            "md10",
            "md11",
            "md12",
            "lg1",
            "lg2",
            "lg3",
            "lg4",
            "lg5",
            "lg6",
            "lg7",
            "lg8",
            "lg9",
            "lg10",
            "lg11",
            "lg12",
            "xl1",
            "xl2",
            "xl3",
            "xl4",
            "xl5",
            "xl6",
            "xl7",
            "xl8",
            "xl9",
            "xl10",
            "xl11",
            "xl12",
            "align_self_baseline",
            "align_self_center",
            "align_self_end",
            "align_self_start",
            "grow",
            "id",
            "offset_sm0",
            "offset_sm1",
            "offset_sm2",
            "offset_sm3",
            "offset_sm4",
            "offset_sm5",
            "offset_sm6",
            "offset_sm7",
            "offset_sm8",
            "offset_sm9",
            "offset_sm10",
            "offset_sm11",
            "offset_sm12",
            "offset_md0",
            "offset_md1",
            "offset_md2",
            "offset_md3",
            "offset_md4",
            "offset_md5",
            "offset_md6",
            "offset_md7",
            "offset_md8",
            "offset_md9",
            "offset_md10",
            "offset_md11",
            "offset_md12",
            "offset_lg0",
            "offset_lg1",
            "offset_lg2",
            "offset_lg3",
            "offset_lg4",
            "offset_lg5",
            "offset_lg6",
            "offset_lg7",
            "offset_lg8",
            "offset_lg9",
            "offset_lg10",
            "offset_lg11",
            "offset_lg12",
            "offset_xl0",
            "offset_xl1",
            "offset_xl2",
            "offset_xl3",
            "offset_xl4",
            "offset_xl5",
            "offset_xl6",
            "offset_xl7",
            "offset_xl8",
            "offset_xl9",
            "offset_xl10",
            "offset_xl11",
            "offset_xl12",
            "order_sm1",
            "order_sm2",
            "order_sm3",
            "order_sm4",
            "order_sm5",
            "order_sm6",
            "order_sm7",
            "order_sm8",
            "order_sm9",
            "order_sm10",
            "order_sm11",
            "order_sm12",
            "order_md1",
            "order_md2",
            "order_md3",
            "order_md4",
            "order_md5",
            "order_md6",
            "order_md7",
            "order_md8",
            "order_md9",
            "order_md10",
            "order_md11",
            "order_md12",
            "order_lg1",
            "order_lg2",
            "order_lg3",
            "order_lg4",
            "order_lg5",
            "order_lg6",
            "order_lg7",
            "order_lg8",
            "order_lg9",
            "order_lg10",
            "order_lg11",
            "order_lg12",
            "order_xl1",
            "order_xl2",
            "order_xl3",
            "order_xl4",
            "order_xl5",
            "order_xl6",
            "order_xl7",
            "order_xl8",
            "order_xl9",
            "order_xl10",
            "order_xl11",
            "order_xl12",
            "shrink",
            "tag",
        ]


class VHover(AbstractElement):

    """
    Vuetify's VHover component. See more info and examples |VHover_vuetify_link|.

    .. |VHover_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-hover" target="_blank">here</a>


    :param close_delay: Milliseconds to wait before closing component.
    :type ['number', 'string']:
    :param disabled: Turns off hover functionality
    :type boolean:
    :param open_delay: Milliseconds to wait before opening component.
    :type ['number', 'string']:
    :param value: Controls whether the component is visible or hidden.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-hover", children, **kwargs)
        self._attr_names += [
            "close_delay",
            "disabled",
            "open_delay",
            "value",
        ]


class VIcon(AbstractElement):

    """
    Vuetify's VIcon component. See more info and examples |VIcon_vuetify_link|.

    .. |VIcon_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-icon" target="_blank">here</a>


    :param color: See description |VIcon_vuetify_link|.
    :type string:
    :param dark: See description |VIcon_vuetify_link|.
    :type boolean:
    :param dense: Makes icon smaller (20px)
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param large: Makes the component large.
    :type boolean:
    :param left: Applies appropriate margins to the icon inside of a button when placed to the **left** of another element or text
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param right: Applies appropriate margins to the icon inside of a button when placed to the **right** of another element or text
    :type boolean:
    :param size: Specifies a custom font size for the icon
    :type ['number', 'string']:
    :param small: Makes the component small.
    :type boolean:
    :param tag: Specifies a custom tag to be used
    :type string:
    :param x_large: Makes the component extra large.
    :type boolean:
    :param x_small: Makes the component extra small.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-icon", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "dense",
            "disabled",
            "large",
            "left",
            "light",
            "right",
            "size",
            "small",
            "tag",
            "x_large",
            "x_small",
        ]


class VImg(AbstractElement):

    """
    Vuetify's VImg component. See more info and examples |VImg_vuetify_link|.

    .. |VImg_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-img" target="_blank">here</a>


    :param alt: Alternate text for screen readers. Leave empty for decorative images
    :type string:
    :param aspect_ratio: Calculated as `width/height`, so for a 1920x1080px image this will be `1.7778`. Will be calculated automatically if omitted
    :type ['string', 'number']:
    :param contain: Prevents the image from being cropped if it doesn't fit
    :type boolean:
    :param content_class: Apply a custom class to the responsive content div.
    :type string:
    :param dark: See description |VImg_vuetify_link|.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param gradient: See description |VImg_vuetify_link|.
    :type string:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param lazy_src: See description |VImg_vuetify_link|.
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param options: See description |VImg_vuetify_link|.
    :type object:
    :param position: See description |VImg_vuetify_link|.
    :type string:
    :param sizes: See description |VImg_vuetify_link|.
    :type string:
    :param src: The image URL. This prop is mandatory
    :type ['string', 'object']:
    :param srcset: See description |VImg_vuetify_link|.
    :type string:
    :param transition: The transition to use when switching from `lazy-src` to `src`
    :type ['boolean', 'string']:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param error: Emitted when there is an error
    :param load: Emitted when image is loaded
    :param loadstart: Emitted when the image starts to load
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-img", children, **kwargs)
        self._attr_names += [
            "alt",
            "aspect_ratio",
            "contain",
            "content_class",
            "dark",
            "eager",
            "gradient",
            "height",
            "lazy_src",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "options",
            "position",
            "sizes",
            "src",
            "srcset",
            "transition",
            "width",
        ]
        self._event_names += [
            "error",
            "load",
            "loadstart",
        ]


class VInput(AbstractElement):

    """
    Vuetify's VInput component. See more info and examples |VInput_vuetify_link|.

    .. |VInput_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-input" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param color: See description |VInput_vuetify_link|.
    :type string:
    :param dark: See description |VInput_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type boolean:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-input", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "background_color",
            "color",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "height",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "label",
            "light",
            "loading",
            "messages",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "rules",
            "success",
            "success_messages",
            "validate_on_blur",
            "value",
        ]
        self._event_names += [
            "change",
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VItem(AbstractElement):

    """
    Vuetify's VItem component. See more info and examples |VItem_vuetify_link|.

    .. |VItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-item" target="_blank">here</a>


    :param active_class: See description |VItem_vuetify_link|.
    :type string:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param value: The value used when the component is selected in a group. If not provided, the index will be used.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "value",
        ]


class VItemGroup(AbstractElement):

    """
    Vuetify's VItemGroup component. See more info and examples |VItemGroup_vuetify_link|.

    .. |VItemGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-item-group" target="_blank">here</a>


    :param active_class: See description |VItemGroup_vuetify_link|.
    :type string:
    :param dark: See description |VItemGroup_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-item-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "dark",
            "light",
            "mandatory",
            "max",
            "multiple",
            "tag",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
        ]


class VLazy(AbstractElement):

    """
    Vuetify's VLazy component. See more info and examples |VLazy_vuetify_link|.

    .. |VLazy_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-lazy" target="_blank">here</a>


    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param options: See description |VLazy_vuetify_link|.
    :type object:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param transition: See description |VLazy_vuetify_link|.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-lazy", children, **kwargs)
        self._attr_names += [
            "height",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "options",
            "tag",
            "transition",
            "value",
            "width",
        ]


class VListItemActionText(AbstractElement):

    """
    Vuetify's VListItemActionText component. See more info and examples |VListItemActionText_vuetify_link|.

    .. |VListItemActionText_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-action-text" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-action-text", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VListItemContent(AbstractElement):

    """
    Vuetify's VListItemContent component. See more info and examples |VListItemContent_vuetify_link|.

    .. |VListItemContent_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-content" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-content", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VListItemTitle(AbstractElement):

    """
    Vuetify's VListItemTitle component. See more info and examples |VListItemTitle_vuetify_link|.

    .. |VListItemTitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-title" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-title", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VListItemSubtitle(AbstractElement):

    """
    Vuetify's VListItemSubtitle component. See more info and examples |VListItemSubtitle_vuetify_link|.

    .. |VListItemSubtitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-subtitle" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-subtitle", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VList(AbstractElement):

    """
    Vuetify's VList component. See more info and examples |VList_vuetify_link|.

    .. |VList_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list" target="_blank">here</a>


    :param color: See description |VList_vuetify_link|.
    :type string:
    :param dark: See description |VList_vuetify_link|.
    :type boolean:
    :param dense: Lowers max height of list tiles
    :type boolean:
    :param disabled: Disables all children `v-list-item` components
    :type boolean:
    :param elevation: See description |VList_vuetify_link|.
    :type ['number', 'string']:
    :param expand: Will only collapse when explicitly closed
    :type boolean:
    :param flat: Remove the highlighted background on active `v-list-item`s
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param nav: See description |VList_vuetify_link|.
    :type boolean:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param rounded: Rounds the `v-list-item` edges
    :type boolean:
    :param shaped: Provides an alternative active style for `v-list-item`.
    :type boolean:
    :param subheader: Removes top padding. Used when previous sibling is a header
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param three_line: See description |VList_vuetify_link|.
    :type boolean:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param two_line: See description |VList_vuetify_link|.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "dense",
            "disabled",
            "elevation",
            "expand",
            "flat",
            "height",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "nav",
            "outlined",
            "rounded",
            "shaped",
            "subheader",
            "tag",
            "three_line",
            "tile",
            "two_line",
            "width",
        ]


class VListGroup(AbstractElement):

    """
    Vuetify's VListGroup component. See more info and examples |VListGroup_vuetify_link|.

    .. |VListGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-group" target="_blank">here</a>


    :param active_class: See description |VListGroup_vuetify_link|.
    :type string:
    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param color: See description |VListGroup_vuetify_link|.
    :type string:
    :param disabled: Disables all children `v-list-item` components
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param group: Assign a route namespace. Accepts a string or regexp for determining active state
    :type ['string', 'regexp']:
    :param no_action: Removes left padding assigned for action icons from group items
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param ripple: See description |VListGroup_vuetify_link|.
    :type ['boolean', 'object']:
    :param sub_group: Designate the component as nested list group
    :type boolean:
    :param value: Expands / Collapse the list-group
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append_icon",
            "color",
            "disabled",
            "eager",
            "group",
            "no_action",
            "prepend_icon",
            "ripple",
            "sub_group",
            "value",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
        ]


class VListItem(AbstractElement):

    """
    Vuetify's VListItem component. See more info and examples |VListItem_vuetify_link|.

    .. |VListItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item" target="_blank">here</a>


    :param active_class: See description |VListItem_vuetify_link|.
    :type string:
    :param append: See description |VListItem_vuetify_link|.
    :type boolean:
    :param color: Applies specified color to the control when in an **active** state or **input-value** is **true** - it can be the name of material color (for example `success` or `purple`) or css color (`#033` or `rgba(255, 0, 0, 0.5)`)
    :type string:
    :param dark: See description |VListItem_vuetify_link|.
    :type boolean:
    :param dense: Lowers max height of list tiles
    :type boolean:
    :param disabled: Disables the component
    :type boolean:
    :param exact: See description |VListItem_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VListItem_vuetify_link|.
    :type string:
    :param exact_path: See description |VListItem_vuetify_link|.
    :type boolean:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param inactive: If set, the list tile will not be rendered as a link even if it has to/href prop or @click handler
    :type boolean:
    :param input_value: Controls the **active** state of the item. This is typically used to highlight the component
    :type any:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param nuxt: See description |VListItem_vuetify_link|.
    :type boolean:
    :param replace: See description |VListItem_vuetify_link|.
    :type boolean:
    :param ripple: See description |VListItem_vuetify_link|.
    :type ['boolean', 'object']:
    :param selectable: See description |VListItem_vuetify_link|.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param three_line: See description |VListItem_vuetify_link|.
    :type boolean:
    :param to: See description |VListItem_vuetify_link|.
    :type ['string', 'object']:
    :param two_line: See description |VListItem_vuetify_link|.
    :type boolean:
    :param value: See description |VListItem_vuetify_link|.
    :type any:

    Events

    :param keydown:
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append",
            "color",
            "dark",
            "dense",
            "disabled",
            "exact",
            "exact_active_class",
            "exact_path",
            "href",
            "inactive",
            "input_value",
            "light",
            "link",
            "nuxt",
            "replace",
            "ripple",
            "selectable",
            "tag",
            "target",
            "three_line",
            "to",
            "two_line",
            "value",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
            "keydown",
        ]


class VListItemAction(AbstractElement):

    """
    Vuetify's VListItemAction component. See more info and examples |VListItemAction_vuetify_link|.

    .. |VListItemAction_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-action" target="_blank">here</a>



    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-action", children, **kwargs)


class VListItemAvatar(AbstractElement):

    """
    Vuetify's VListItemAvatar component. See more info and examples |VListItemAvatar_vuetify_link|.

    .. |VListItemAvatar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-avatar" target="_blank">here</a>


    :param color: See description |VListItemAvatar_vuetify_link|.
    :type string:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param horizontal: Uses an alternative horizontal style.
    :type boolean:
    :param left: See description |VListItemAvatar_vuetify_link|.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param right: See description |VListItemAvatar_vuetify_link|.
    :type boolean:
    :param rounded: See description |VListItemAvatar_vuetify_link|.
    :type ['boolean', 'string']:
    :param size: Sets the height and width of the component.
    :type ['number', 'string']:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-avatar", children, **kwargs)
        self._attr_names += [
            "color",
            "height",
            "horizontal",
            "left",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "right",
            "rounded",
            "size",
            "tile",
            "width",
        ]


class VListItemIcon(AbstractElement):

    """
    Vuetify's VListItemIcon component. See more info and examples |VListItemIcon_vuetify_link|.

    .. |VListItemIcon_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-icon" target="_blank">here</a>



    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-icon", children, **kwargs)


class VListItemGroup(AbstractElement):

    """
    Vuetify's VListItemGroup component. See more info and examples |VListItemGroup_vuetify_link|.

    .. |VListItemGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-list-item-group" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param color: See description |VListItemGroup_vuetify_link|.
    :type string:
    :param dark: See description |VListItemGroup_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param value: Sets the active list-item inside the list-group
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-list-item-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "color",
            "dark",
            "light",
            "mandatory",
            "max",
            "multiple",
            "tag",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
        ]


class VMain(AbstractElement):

    """
    Vuetify's VMain component. See more info and examples |VMain_vuetify_link|.

    .. |VMain_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-main" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-main", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VMenu(AbstractElement):

    """
    Vuetify's VMenu component. See more info and examples |VMenu_vuetify_link|.

    .. |VMenu_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-menu" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param activator: Designate a custom activator when the `activator` slot is not used. String can be any valid querySelector and Object can be any valid Node.
    :type any:
    :param allow_overflow: Removes overflow re-positioning for the content
    :type boolean:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param auto: Centers list on selected element
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param close_delay: Milliseconds to wait before closing component. Only works with the **open-on-hover** prop
    :type ['number', 'string']:
    :param close_on_click: Designates if menu should close on outside-activator click
    :type boolean:
    :param close_on_content_click: Designates if menu should close when its content is clicked
    :type boolean:
    :param content_class: Applies a custom class to the detached element. This is useful because the content is moved to the beginning of the `v-app` component (unless the **attach** prop is provided) and is not targetable by classes passed directly on the component.
    :type string:
    :param dark: See description |VMenu_vuetify_link|.
    :type boolean:
    :param disable_keys: Removes all keyboard interaction
    :type boolean:
    :param disabled: Disables the menu
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param internal_activator: Detaches the menu content inside of the component as opposed to the document.
    :type boolean:
    :param left: Aligns the component towards the left.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the max height of the menu content
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the content
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the content
    :type ['number', 'string']:
    :param nudge_bottom: Nudge the content to the bottom
    :type ['number', 'string']:
    :param nudge_left: Nudge the content to the left
    :type ['number', 'string']:
    :param nudge_right: Nudge the content to the right
    :type ['number', 'string']:
    :param nudge_top: Nudge the content to the top
    :type ['number', 'string']:
    :param nudge_width: Nudge the content width
    :type ['number', 'string']:
    :param offset_overflow: Causes the component to flip to the opposite side when repositioned due to overflow
    :type boolean:
    :param offset_x: Offset the menu on the x-axis. Works in conjunction with direction left/right
    :type boolean:
    :param offset_y: Offset the menu on the y-axis. Works in conjunction with direction top/bottom
    :type boolean:
    :param open_delay: Milliseconds to wait before opening component. Only works with the **open-on-hover** prop
    :type ['number', 'string']:
    :param open_on_click: Designates whether menu should open on activator click
    :type boolean:
    :param open_on_focus:
    :type boolean:
    :param open_on_hover: Designates whether menu should open on activator hover
    :type boolean:
    :param origin: See description |VMenu_vuetify_link|.
    :type string:
    :param position_x: Used to position the content when not using an activator slot
    :type number:
    :param position_y: Used to position the content when not using an activator slot
    :type number:
    :param return_value: The value that is updated when the menu is closed - must be primitive. Dot notation is supported
    :type any:
    :param right: Aligns the component towards the right.
    :type boolean:
    :param rounded: See description |VMenu_vuetify_link|.
    :type ['boolean', 'string']:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param transition: See description |VMenu_vuetify_link|.
    :type ['boolean', 'string']:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param z_index: The z-index used for the component
    :type ['number', 'string']:

    Events

    :param input: The updated bound model
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-menu", children, **kwargs)
        self._attr_names += [
            "absolute",
            "activator",
            "allow_overflow",
            "attach",
            "auto",
            "bottom",
            "close_delay",
            "close_on_click",
            "close_on_content_click",
            "content_class",
            "dark",
            "disable_keys",
            "disabled",
            "eager",
            "internal_activator",
            "left",
            "light",
            "max_height",
            "max_width",
            "min_width",
            "nudge_bottom",
            "nudge_left",
            "nudge_right",
            "nudge_top",
            "nudge_width",
            "offset_overflow",
            "offset_x",
            "offset_y",
            "open_delay",
            "open_on_click",
            "open_on_focus",
            "open_on_hover",
            "origin",
            "position_x",
            "position_y",
            "return_value",
            "right",
            "rounded",
            "tile",
            "top",
            "transition",
            "value",
            "z_index",
        ]
        self._event_names += [
            "input",
        ]


class VNavigationDrawer(AbstractElement):

    """
    Vuetify's VNavigationDrawer component. See more info and examples |VNavigationDrawer_vuetify_link|.

    .. |VNavigationDrawer_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-navigation-drawer" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param app: See description |VNavigationDrawer_vuetify_link|.
    :type boolean:
    :param bottom: Expands from the bottom of the screen on mobile devices
    :type boolean:
    :param clipped: A clipped drawer rests under the application toolbar. **Note:** requires the **clipped-left** or **clipped-right** prop on `v-app-bar` to work as intended
    :type boolean:
    :param color: See description |VNavigationDrawer_vuetify_link|.
    :type string:
    :param dark: See description |VNavigationDrawer_vuetify_link|.
    :type boolean:
    :param disable_resize_watcher: Will automatically open/close drawer when resized depending if mobile or desktop.
    :type boolean:
    :param disable_route_watcher: Disables opening of navigation drawer when route changes
    :type boolean:
    :param expand_on_hover: Collapses the drawer to a **mini-variant** until hovering with the mouse
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param floating: A floating drawer has no visible container (no border-right)
    :type boolean:
    :param height: Sets the height of the navigation drawer
    :type ['number', 'string']:
    :param hide_overlay: Hides the display of the overlay.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mini_variant: Condenses navigation drawer width, also accepts the **.sync** modifier. With this, the drawer will re-open when clicking it
    :type boolean:
    :param mini_variant_width: Designates the width assigned when the `mini` prop is turned on
    :type ['number', 'string']:
    :param mobile_breakpoint: Sets the designated mobile breakpoint for the component. This will apply alternate styles for mobile devices such as the `temporary` prop, or activate the `bottom` prop when the breakpoint value is met. Setting the value to `0` will disable this functionality.
    :type ['number', 'string']:
    :param overlay_color: Sets the overlay color.
    :type string:
    :param overlay_opacity: Sets the overlay opacity.
    :type ['number', 'string']:
    :param permanent: The drawer remains visible regardless of screen size
    :type boolean:
    :param right: Places the navigation drawer on the right
    :type boolean:
    :param src: See description |VNavigationDrawer_vuetify_link|.
    :type ['string', 'object']:
    :param stateless: Remove all automated state functionality (resize, mobile, route) and manually control the drawer state
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param temporary: A temporary drawer sits above its application and uses a scrim (overlay) to darken the background
    :type boolean:
    :param touchless: Disable mobile touch functionality
    :type boolean:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param input: The updated bound model
    :param transitionend: Emits event object when transition is complete.
    :param update_mini_variant: The `mini-variant.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-navigation-drawer", children, **kwargs)
        self._attr_names += [
            "absolute",
            "app",
            "bottom",
            "clipped",
            "color",
            "dark",
            "disable_resize_watcher",
            "disable_route_watcher",
            "expand_on_hover",
            "fixed",
            "floating",
            "height",
            "hide_overlay",
            "light",
            "mini_variant",
            "mini_variant_width",
            "mobile_breakpoint",
            "overlay_color",
            "overlay_opacity",
            "permanent",
            "right",
            "src",
            "stateless",
            "tag",
            "temporary",
            "touchless",
            "value",
            "width",
        ]
        self._event_names += [
            "input",
            "transitionend",
            ("update_mini_variant", "update:mini-variant"),
        ]


class VOtpInput(AbstractElement):

    """
    Vuetify's VOtpInput component. See more info and examples |VOtpInput_vuetify_link|.

    .. |VOtpInput_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-otp-input" target="_blank">here</a>


    :param dark: See description |VOtpInput_vuetify_link|.
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param length: The OTP field's length
    :type ['number', 'string']:
    :param plain: Outlined style applied by default to the input, set to `true` to apply plain style
    :type boolean:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param type: Supported types: `text`, `password`, `number`
    :type string:
    :param value: The input's value
    :type any:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param finish: Emitted when the input is filled completely and cursor is blurred
    :param input: The updated bound model
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-otp-input", children, **kwargs)
        self._attr_names += [
            "dark",
            "disabled",
            "hide_spin_buttons",
            "id",
            "length",
            "plain",
            "readonly",
            "type",
            "value",
        ]
        self._event_names += [
            "change",
            "finish",
            "input",
        ]


class VOverflowBtn(AbstractElement):

    """
    Vuetify's VOverflowBtn component. See more info and examples |VOverflowBtn_vuetify_link|.

    .. |VOverflowBtn_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-overflow-btn" target="_blank">here</a>


    :param allow_overflow: Allow the menu to overflow off the screen
    :type boolean:
    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param auto_select_first: When searching, will always highlight the first option
    :type boolean:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param cache_items: Keeps a local _unique_ copy of all items that have been passed through the **items** prop.
    :type boolean:
    :param chips: Changes display of selections to chips
    :type boolean:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VOverflowBtn_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VOverflowBtn_vuetify_link|.
    :type boolean:
    :param deletable_chips: Adds a remove icon to selected chips
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disable_lookup: Disables keyboard lookup
    :type boolean:
    :param disabled: Disables the input
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param editable: Creates an editable button
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param filter: See description |VOverflowBtn_vuetify_link|.
    :type function:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_no_data: Hides the menu when there are no options to show.  Useful for preventing the menu from opening before results are fetched asynchronously.  Also has the effect of opening the menu when the `items` array changes if not already open.
    :type boolean:
    :param hide_selected: Do not display in the select menu items that are already selected
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param item_color: Sets color of selected items
    :type string:
    :param item_disabled: Set property of **items**'s disabled value
    :type ['string', 'array', 'function']:
    :param item_text: Set property of **items**'s text value
    :type ['string', 'array', 'function']:
    :param item_value: See description |VOverflowBtn_vuetify_link|.
    :type ['string', 'array', 'function']:
    :param items: Can be an array of objects or array of strings. When using objects, will look for a text, value and disabled keys. This can be changed using the **item-text**, **item-value** and **item-disabled** props.  Objects that have a **header** or **divider** property are considered special cases and generate a list header or divider; these items are not selectable.
    :type array:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param menu_props: Pass props through to the `v-menu` component. Accepts either a string for boolean props `menu-props="auto, overflowY"`, or an object `:menu-props="{ auto: true, overflowY: true }"`
    :type ['string', 'array', 'object']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes select to multiple. Accepts array for value
    :type boolean:
    :param no_data_text: Display text when there is no data
    :type string:
    :param no_filter: Do not apply filtering when searching. Useful when data is being filtered server side
    :type boolean:
    :param open_on_clear: When using the **clearable** prop, once cleared, the select menu will either open or stay open, depending on the current state
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param return_object: Changes the selection behavior to return the object directly rather than the value specified with **item-value**
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param search_input: Search value. Can be used with `.sync` modifier.
    :type string:
    :param segmented: Creates a segmented button
    :type boolean:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param small_chips: Changes display of selections to chips with the **small** property
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: See description |VOverflowBtn_vuetify_link|.
    :type function:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    :param update_list_index: Emitted when menu item is selected using keyboard arrows
    :param update_search_input: The `search-input.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-overflow-btn", children, **kwargs)
        self._attr_names += [
            "allow_overflow",
            "append_icon",
            "append_outer_icon",
            "attach",
            "auto_select_first",
            "autofocus",
            "background_color",
            "cache_items",
            "chips",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "deletable_chips",
            "dense",
            "disable_lookup",
            "disabled",
            "eager",
            "editable",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "filter",  # JS functions unimplemented
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_no_data",
            "hide_selected",
            "hide_spin_buttons",
            "hint",
            "id",
            "item_color",
            "item_disabled",  # JS functions unimplemented
            "item_text",  # JS functions unimplemented
            "item_value",  # JS functions unimplemented
            "items",
            "label",
            "light",
            "loader_height",
            "loading",
            "menu_props",
            "messages",
            "multiple",
            "no_data_text",
            "no_filter",
            "open_on_clear",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "return_object",
            "reverse",
            "rounded",
            "rules",
            "search_input",
            "segmented",
            "shaped",
            "single_line",
            "small_chips",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
            ("update_list_index", "update:list-index"),
            ("update_search_input", "update:search-input"),
        ]


class VOverlay(AbstractElement):

    """
    Vuetify's VOverlay component. See more info and examples |VOverlay_vuetify_link|.

    .. |VOverlay_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-overlay" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param color: See description |VOverlay_vuetify_link|.
    :type string:
    :param dark: See description |VOverlay_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param opacity: Sets the overlay opacity
    :type ['number', 'string']:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param z_index: The z-index used for the component
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-overlay", children, **kwargs)
        self._attr_names += [
            "absolute",
            "color",
            "dark",
            "light",
            "opacity",
            "value",
            "z_index",
        ]


class VPagination(AbstractElement):

    """
    Vuetify's VPagination component. See more info and examples |VPagination_vuetify_link|.

    .. |VPagination_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-pagination" target="_blank">here</a>


    :param circle: Shape pagination elements as circles
    :type boolean:
    :param color: See description |VPagination_vuetify_link|.
    :type string:
    :param current_page_aria_label:
    :type string:
    :param dark: See description |VPagination_vuetify_link|.
    :type boolean:
    :param disabled: Disables component
    :type boolean:
    :param length: The length of the pagination component
    :type number:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param next_aria_label:
    :type string:
    :param next_icon: Specify the icon to use for the next icon
    :type string:
    :param page_aria_label:
    :type string:
    :param prev_icon: Specify the icon to use for the prev icon
    :type string:
    :param previous_aria_label:
    :type string:
    :param total_visible: Specify the max total visible pagination numbers
    :type ['number', 'string']:
    :param value: Current selected page
    :type number:
    :param wrapper_aria_label:
    :type string:

    Events

    :param input: The updated bound model
    :param next: Emitted when going to next item
    :param previous: Emitted when going to previous item
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-pagination", children, **kwargs)
        self._attr_names += [
            "circle",
            "color",
            "current_page_aria_label",
            "dark",
            "disabled",
            "length",
            "light",
            "next_aria_label",
            "next_icon",
            "page_aria_label",
            "prev_icon",
            "previous_aria_label",
            "total_visible",
            "value",
            "wrapper_aria_label",
        ]
        self._event_names += [
            "input",
            "next",
            "previous",
        ]


class VSheet(AbstractElement):

    """
    Vuetify's VSheet component. See more info and examples |VSheet_vuetify_link|.

    .. |VSheet_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-sheet" target="_blank">here</a>


    :param color: See description |VSheet_vuetify_link|.
    :type string:
    :param dark: See description |VSheet_vuetify_link|.
    :type boolean:
    :param elevation: See description |VSheet_vuetify_link|.
    :type ['number', 'string']:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param rounded: See description |VSheet_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-sheet", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "elevation",
            "height",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "outlined",
            "rounded",
            "shaped",
            "tag",
            "tile",
            "width",
        ]


class VParallax(AbstractElement):

    """
    Vuetify's VParallax component. See more info and examples |VParallax_vuetify_link|.

    .. |VParallax_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-parallax" target="_blank">here</a>


    :param alt: Attaches an alt property to the parallax image
    :type string:
    :param height: Sets the height for the component
    :type ['string', 'number']:
    :param src: The image to parallax
    :type string:
    :param srcset: See description |VParallax_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-parallax", children, **kwargs)
        self._attr_names += [
            "alt",
            "height",
            "src",
            "srcset",
        ]


class VProgressCircular(AbstractElement):

    """
    Vuetify's VProgressCircular component. See more info and examples |VProgressCircular_vuetify_link|.

    .. |VProgressCircular_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-progress-circular" target="_blank">here</a>


    :param button: Deprecated - Pending removal
    :type boolean:
    :param color: See description |VProgressCircular_vuetify_link|.
    :type string:
    :param indeterminate: Constantly animates, use when loading progress is unknown.
    :type boolean:
    :param rotate: Rotates the circle start point in deg
    :type ['number', 'string']:
    :param size: Sets the diameter of the circle in pixels
    :type ['number', 'string']:
    :param value: The percentage value for current progress
    :type ['number', 'string']:
    :param width: Sets the stroke of the circle in pixels
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-progress-circular", children, **kwargs)
        self._attr_names += [
            "button",
            "color",
            "indeterminate",
            "rotate",
            "size",
            "value",
            "width",
        ]


class VProgressLinear(AbstractElement):

    """
    Vuetify's VProgressLinear component. See more info and examples |VProgressLinear_vuetify_link|.

    .. |VProgressLinear_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-progress-linear" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param active: Reduce the height to 0, hiding component
    :type boolean:
    :param background_color: Background color, set to component's color if null
    :type string:
    :param background_opacity: Background opacity, if null it defaults to 0.3 if background color is not specified or 1 otherwise
    :type ['number', 'string']:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param buffer_value: The percentage value for the buffer
    :type ['number', 'string']:
    :param color: See description |VProgressLinear_vuetify_link|.
    :type string:
    :param dark: See description |VProgressLinear_vuetify_link|.
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param height: Sets the height for the component
    :type ['number', 'string']:
    :param indeterminate: Constantly animates, use when loading progress is unknown.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param query: Animates like **indeterminate** prop but inverse
    :type boolean:
    :param reverse: Displays reversed progress (right to left in LTR mode and left to right in RTL)
    :type boolean:
    :param rounded: Adds a border radius to the progress component
    :type boolean:
    :param stream: An alternative style for portraying loading that works in tandem with **buffer-value**
    :type boolean:
    :param striped: Adds a stripe background to the filled portion of the progress component
    :type boolean:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param value: The designated model value for the component.
    :type ['number', 'string']:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-progress-linear", children, **kwargs)
        self._attr_names += [
            "absolute",
            "active",
            "background_color",
            "background_opacity",
            "bottom",
            "buffer_value",
            "color",
            "dark",
            "fixed",
            "height",
            "indeterminate",
            "light",
            "query",
            "reverse",
            "rounded",
            "stream",
            "striped",
            "top",
            "value",
        ]
        self._event_names += [
            "change",
        ]


class VRadioGroup(AbstractElement):

    """
    Vuetify's VRadioGroup component. See more info and examples |VRadioGroup_vuetify_link|.

    .. |VRadioGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-radio-group" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param column: Displays radio buttons in column
    :type boolean:
    :param dark: See description |VRadioGroup_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param name: Sets the component's name attribute
    :type string:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param row: Displays radio buttons in row
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-radio-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append_icon",
            "background_color",
            "column",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "label",
            "light",
            "mandatory",
            "max",
            "messages",
            "multiple",
            "name",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "row",
            "rules",
            "success",
            "success_messages",
            "tag",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VRadio(AbstractElement):

    """
    Vuetify's VRadio component. See more info and examples |VRadio_vuetify_link|.

    .. |VRadio_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-radio" target="_blank">here</a>


    :param active_class: See description |VRadio_vuetify_link|.
    :type string:
    :param color: See description |VRadio_vuetify_link|.
    :type string:
    :param dark: See description |VRadio_vuetify_link|.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param name: Sets the component's name attribute
    :type string:
    :param off_icon: The icon used when inactive
    :type string:
    :param on_icon: The icon used when active
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param ripple: See description |VRadio_vuetify_link|.
    :type ['boolean', 'object']:
    :param value: The value used when the component is selected in a group. If not provided, the index will be used.
    :type any:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-radio", children, **kwargs)
        self._attr_names += [
            "active_class",
            "color",
            "dark",
            "disabled",
            "id",
            "label",
            "light",
            "name",
            "off_icon",
            "on_icon",
            "readonly",
            "ripple",
            "value",
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VRangeSlider(AbstractElement):

    """
    Vuetify's VRangeSlider component. See more info and examples |VRangeSlider_vuetify_link|.

    .. |VRangeSlider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-range-slider" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param color: See description |VRangeSlider_vuetify_link|.
    :type string:
    :param dark: See description |VRangeSlider_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param inverse_label: Reverse the label position. Works with **rtl**.
    :type boolean:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param max: Sets the maximum allowed value
    :type ['number', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param min: Sets the minimum allowed value
    :type ['number', 'string']:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param step: If greater than 0, sets step interval for ticks
    :type ['number', 'string']:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param thumb_color: Sets the thumb and thumb label color
    :type string:
    :param thumb_label: Show thumb label. If `true` it shows label when using slider. If set to `'always'` it always shows label.
    :type ['boolean', 'string']:
    :param thumb_size: Controls the size of the thumb label.
    :type ['number', 'string']:
    :param tick_labels: When provided with Array<string>, will attempt to map the labels to each step in index order
    :type array:
    :param tick_size: Controls the size of **ticks**
    :type ['number', 'string']:
    :param ticks: Show track ticks. If `true` it shows ticks when using slider. If set to `'always'` it always shows ticks.
    :type ['boolean', 'string']:
    :param track_color: Sets the track's color
    :type string:
    :param track_fill_color: Sets the track's fill color
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param vertical: Changes slider direction to vertical
    :type boolean:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param end: Slider value emitted at the end of slider movement
    :param input: The updated bound model
    :param start: Slider value emitted at start of slider movement
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-range-slider", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "background_color",
            "color",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "height",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "inverse_label",
            "label",
            "light",
            "loader_height",
            "loading",
            "max",
            "messages",
            "min",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "rules",
            "step",
            "success",
            "success_messages",
            "thumb_color",
            "thumb_label",
            "thumb_size",
            "tick_labels",
            "tick_size",
            "ticks",
            "track_color",
            "track_fill_color",
            "validate_on_blur",
            "value",
            "vertical",
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            "end",
            "input",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            "start",
            ("update_error", "update:error"),
        ]


class VRating(AbstractElement):

    """
    Vuetify's VRating component. See more info and examples |VRating_vuetify_link|.

    .. |VRating_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-rating" target="_blank">here</a>


    :param background_color: The color used empty icons
    :type string:
    :param clearable: Allows for the component to be cleared. Triggers when the icon containing the current value is clicked.
    :type boolean:
    :param close_delay: Milliseconds to wait before closing component.
    :type ['number', 'string']:
    :param color: See description |VRating_vuetify_link|.
    :type string:
    :param dark: See description |VRating_vuetify_link|.
    :type boolean:
    :param dense: Icons have a smaller size
    :type boolean:
    :param empty_icon: The icon displayed when empty
    :type string:
    :param full_icon: The icon displayed when full
    :type string:
    :param half_icon: The icon displayed when half (requires **half-increments** prop)
    :type string:
    :param half_increments: Allows the selection of half increments
    :type boolean:
    :param hover: Provides visual feedback when hovering over icons
    :type boolean:
    :param icon_label: The **aria-label** used for icons
    :type string:
    :param large: Makes the component large.
    :type boolean:
    :param length: The amount of ratings to show
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param open_delay: Milliseconds to wait before opening component.
    :type ['number', 'string']:
    :param readonly: Removes all hover effects and pointer events
    :type boolean:
    :param ripple: See description |VRating_vuetify_link|.
    :type ['boolean', 'object']:
    :param size: Sets the height and width of the component.
    :type ['number', 'string']:
    :param small: Makes the component small.
    :type boolean:
    :param value: The rating value
    :type number:
    :param x_large: Makes the component extra large.
    :type boolean:
    :param x_small: Makes the component extra small.
    :type boolean:

    Events

    :param input: Emits the rating number when this value changes
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-rating", children, **kwargs)
        self._attr_names += [
            "background_color",
            "clearable",
            "close_delay",
            "color",
            "dark",
            "dense",
            "empty_icon",
            "full_icon",
            "half_icon",
            "half_increments",
            "hover",
            "icon_label",
            "large",
            "length",
            "light",
            "open_delay",
            "readonly",
            "ripple",
            "size",
            "small",
            "value",
            "x_large",
            "x_small",
        ]
        self._event_names += [
            "input",
        ]


class VResponsive(AbstractElement):

    """
    Vuetify's VResponsive component. See more info and examples |VResponsive_vuetify_link|.

    .. |VResponsive_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-responsive" target="_blank">here</a>


    :param aspect_ratio: Sets a base aspect ratio, calculated as width/height. This will only set a **minimum** height, the component can still grow if it has a lot of content.
    :type ['string', 'number']:
    :param content_class: Apply a custom class to the responsive content div.
    :type string:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-responsive", children, **kwargs)
        self._attr_names += [
            "aspect_ratio",
            "content_class",
            "height",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "width",
        ]


class VSelect(AbstractElement):

    """
    Vuetify's VSelect component. See more info and examples |VSelect_vuetify_link|.

    .. |VSelect_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-select" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param cache_items: Keeps a local _unique_ copy of all items that have been passed through the **items** prop.
    :type boolean:
    :param chips: Changes display of selections to chips
    :type boolean:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VSelect_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VSelect_vuetify_link|.
    :type boolean:
    :param deletable_chips: Adds a remove icon to selected chips
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disable_lookup: Disables keyboard lookup
    :type boolean:
    :param disabled: Disables the input
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_selected: Do not display in the select menu items that are already selected
    :type boolean:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param item_color: Sets color of selected items
    :type string:
    :param item_disabled: Set property of **items**'s disabled value
    :type ['string', 'array', 'function']:
    :param item_text: Set property of **items**'s text value
    :type ['string', 'array', 'function']:
    :param item_value: See description |VSelect_vuetify_link|.
    :type ['string', 'array', 'function']:
    :param items: Can be an array of objects or array of strings. When using objects, will look for a text, value and disabled keys. This can be changed using the **item-text**, **item-value** and **item-disabled** props.  Objects that have a **header** or **divider** property are considered special cases and generate a list header or divider; these items are not selectable.
    :type array:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param menu_props: Pass props through to the `v-menu` component. Accepts either a string for boolean props `menu-props="auto, overflowY"`, or an object `:menu-props="{ auto: true, overflowY: true }"`
    :type ['string', 'array', 'object']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes select to multiple. Accepts array for value
    :type boolean:
    :param no_data_text: Display text when there is no data
    :type string:
    :param open_on_clear: When using the **clearable** prop, once cleared, the select menu will either open or stay open, depending on the current state
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param return_object: Changes the selection behavior to return the object directly rather than the value specified with **item-value**
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param small_chips: Changes display of selections to chips with the **small** property
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: See description |VSelect_vuetify_link|.
    :type function:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    :param update_list_index: Emitted when menu item is selected using keyboard arrows
    :param update_search_input: The `search-input.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-select", children, **kwargs)
        self.ttsSensitive()
        self._attr_names += [
            "append_icon",
            "append_outer_icon",
            "attach",
            "autofocus",
            "background_color",
            "cache_items",
            "chips",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "deletable_chips",
            "dense",
            "disable_lookup",
            "disabled",
            "eager",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_selected",
            "hide_spin_buttons",
            "hint",
            "id",
            "item_color",
            "item_disabled",  # JS functions unimplemented
            "item_text",  # JS functions unimplemented
            "item_value",  # JS functions unimplemented
            "items",
            "label",
            "light",
            "loader_height",
            "loading",
            "menu_props",
            "messages",
            "multiple",
            "no_data_text",
            "open_on_clear",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "return_object",
            "reverse",
            "rounded",
            "rules",
            "shaped",
            "single_line",
            "small_chips",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
            ("update_list_index", "update:list-index"),
            ("update_search_input", "update:search-input"),
        ]


class VSkeletonLoader(AbstractElement):

    """
    Vuetify's VSkeletonLoader component. See more info and examples |VSkeletonLoader_vuetify_link|.

    .. |VSkeletonLoader_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-skeleton-loader" target="_blank">here</a>


    :param boilerplate: Remove the loading animation from the skeleton
    :type boolean:
    :param dark: See description |VSkeletonLoader_vuetify_link|.
    :type boolean:
    :param elevation: See description |VSkeletonLoader_vuetify_link|.
    :type ['number', 'string']:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loading: Applies a loading animation with a on-hover loading cursor. A value of **false** will only work when there is content in the `default` slot.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param tile: Removes the component's border-radius
    :type boolean:
    :param transition: See description |VSkeletonLoader_vuetify_link|.
    :type string:
    :param type: A string delimited list of skeleton components to create such as `type="text@3"` or `type="card, list-item"`. Will recursively generate a corresponding skeleton from the provided string. Also supports short-hand for multiple elements such as **article@3** and **paragraph@2** which will generate 3 _article_ skeletons and 2 _paragraph_ skeletons. Please see below for a list of available pre-defined options.
    :type string:
    :param types: A custom types object that will be combined with the pre-defined options. For a list of available pre-defined options, see the **type** prop.
    :type object:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-skeleton-loader", children, **kwargs)
        self._attr_names += [
            "boilerplate",
            "dark",
            "elevation",
            "height",
            "light",
            "loading",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "tile",
            "transition",
            "type",
            "types",
            "width",
        ]


class VSlider(AbstractElement):

    """
    Vuetify's VSlider component. See more info and examples |VSlider_vuetify_link|.

    .. |VSlider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slider" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param color: See description |VSlider_vuetify_link|.
    :type string:
    :param dark: See description |VSlider_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param inverse_label: Reverse the label position. Works with **rtl**.
    :type boolean:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param max: Sets the maximum allowed value
    :type ['number', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param min: Sets the minimum allowed value
    :type ['number', 'string']:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param step: If greater than 0, sets step interval for ticks
    :type ['number', 'string']:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param thumb_color: Sets the thumb and thumb label color
    :type string:
    :param thumb_label: Show thumb label. If `true` it shows label when using slider. If set to `'always'` it always shows label.
    :type ['boolean', 'string']:
    :param thumb_size: Controls the size of the thumb label.
    :type ['number', 'string']:
    :param tick_labels: When provided with Array<string>, will attempt to map the labels to each step in index order
    :type array:
    :param tick_size: Controls the size of **ticks**
    :type ['number', 'string']:
    :param ticks: Show track ticks. If `true` it shows ticks when using slider. If set to `'always'` it always shows ticks.
    :type ['boolean', 'string']:
    :param track_color: Sets the track's color
    :type string:
    :param track_fill_color: Sets the track's fill color
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param vertical: Changes slider direction to vertical
    :type boolean:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param end: Slider value emitted at the end of slider movement
    :param input: The updated bound model
    :param start: Slider value emitted at start of slider movement
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slider", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "background_color",
            "color",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "height",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "inverse_label",
            "label",
            "light",
            "loader_height",
            "loading",
            "max",
            "messages",
            "min",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "rules",
            "step",
            "success",
            "success_messages",
            "thumb_color",
            "thumb_label",
            "thumb_size",
            "tick_labels",
            "tick_size",
            "ticks",
            "track_color",
            "track_fill_color",
            "validate_on_blur",
            "value",
            "vertical",
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            "end",
            "input",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            "start",
            ("update_error", "update:error"),
        ]


class VSlideGroup(AbstractElement):

    """
    Vuetify's VSlideGroup component. See more info and examples |VSlideGroup_vuetify_link|.

    .. |VSlideGroup_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-group" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param center_active: Forces the selected component to be centered
    :type boolean:
    :param dark: See description |VSlideGroup_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param mobile_breakpoint: Sets the designated mobile breakpoint for the component.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param next_icon: The appended slot when arrows are shown
    :type string:
    :param prev_icon: The prepended slot when arrows are shown
    :type string:
    :param show_arrows: See description |VSlideGroup_vuetify_link|.
    :type ['boolean', 'string']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the component value is changed by user interaction
    :param click_next: Emitted when the next is clicked
    :param click_prev: Emitted when the prev is clicked
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-group", children, **kwargs)
        self._attr_names += [
            "active_class",
            "center_active",
            "dark",
            "light",
            "mandatory",
            "max",
            "mobile_breakpoint",
            "multiple",
            "next_icon",
            "prev_icon",
            "show_arrows",
            "tag",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
            ("click_next", "click:next"),
            ("click_prev", "click:prev"),
        ]


class VSlideItem(AbstractElement):

    """
    Vuetify's VSlideItem component. See more info and examples |VSlideItem_vuetify_link|.

    .. |VSlideItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-item" target="_blank">here</a>


    :param active_class: See description |VSlideItem_vuetify_link|.
    :type string:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param value: The value used when the component is selected in a group. If not provided, the index will be used.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "value",
        ]


class VSnackbar(AbstractElement):

    """
    Vuetify's VSnackbar component. See more info and examples |VSnackbar_vuetify_link|.

    .. |VSnackbar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-snackbar" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param app: Respects boundaries of—and will not overlap with—other `app` components like `v-app-bar`, `v-navigation-drawer`, and `v-footer`.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param centered: Positions the snackbar in the center of the screen, (x and y axis).
    :type boolean:
    :param color: See description |VSnackbar_vuetify_link|.
    :type string:
    :param content_class: Apply a custom class to the snackbar content
    :type string:
    :param dark: See description |VSnackbar_vuetify_link|.
    :type boolean:
    :param elevation: See description |VSnackbar_vuetify_link|.
    :type ['number', 'string']:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param left: Aligns the component towards the left.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param multi_line: Gives the snackbar a larger minimum height.
    :type boolean:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param right: Aligns the component towards the right.
    :type boolean:
    :param rounded: See description |VSnackbar_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param text: Applies the defined **color** to text and a low opacity background of the same.
    :type boolean:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param timeout: Time (in milliseconds) to wait until snackbar is automatically hidden.  Use `-1` to keep open indefinitely (`0` in version < 2.3 ). It is recommended for this number to be between `4000` and `10000`. Changes to this property will reset the timeout.
    :type ['number', 'string']:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param transition: See description |VSnackbar_vuetify_link|.
    :type ['boolean', 'string']:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param vertical: Stacks snackbar content on top of the actions (button).
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param input: The updated bound model
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-snackbar", children, **kwargs)
        self._attr_names += [
            "absolute",
            "app",
            "bottom",
            "centered",
            "color",
            "content_class",
            "dark",
            "elevation",
            "height",
            "left",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "multi_line",
            "outlined",
            "right",
            "rounded",
            "shaped",
            "tag",
            "text",
            "tile",
            "timeout",
            "top",
            "transition",
            "value",
            "vertical",
            "width",
        ]
        self._event_names += [
            "input",
        ]


class VSparkline(AbstractElement):

    """
    Vuetify's VSparkline component. See more info and examples |VSparkline_vuetify_link|.

    .. |VSparkline_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-sparkline" target="_blank">here</a>


    :param auto_draw: Trace the length of the line when first rendered
    :type boolean:
    :param auto_draw_duration: Amount of time (in ms) to run the trace animation
    :type number:
    :param auto_draw_easing: The easing function to use for the trace animation
    :type string:
    :param auto_line_width: Automatically expand bars to use space efficiently
    :type boolean:
    :param color: See description |VSparkline_vuetify_link|.
    :type string:
    :param fill: Using the **fill** property allows you to better customize the look and feel of your sparkline.
    :type boolean:
    :param gradient: An array of colors to use as a linear-gradient
    :type array:
    :param gradient_direction: The direction the gradient should run
    :type string:
    :param height: Height of the SVG trendline or bars
    :type ['string', 'number']:
    :param label_size: The label font size
    :type ['number', 'string']:
    :param labels: An array of string labels that correspond to the same index as its data counterpart
    :type array:
    :param line_width: The thickness of the line, in px
    :type ['string', 'number']:
    :param padding: Low `smooth` or high `line-width` values may result in cropping, increase padding to compensate
    :type ['string', 'number']:
    :param show_labels: Show labels below each data point
    :type boolean:
    :param smooth: Number of px to use as a corner radius. `true` defaults to 8, `false` is 0
    :type ['boolean', 'number', 'string']:
    :param type: Choose between a trendline or bars
    :type string:
    :param value: An array of numbers.
    :type array:
    :param width: Width of the SVG trendline or bars
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-sparkline", children, **kwargs)
        self._attr_names += [
            "auto_draw",
            "auto_draw_duration",
            "auto_draw_easing",
            "auto_line_width",
            "color",
            "fill",
            "gradient",
            "gradient_direction",
            "height",
            "label_size",
            "labels",
            "line_width",
            "padding",
            "show_labels",
            "smooth",
            "type",
            "value",
            "width",
        ]


class VSpeedDial(AbstractElement):

    """
    Vuetify's VSpeedDial component. See more info and examples |VSpeedDial_vuetify_link|.

    .. |VSpeedDial_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-speed-dial" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param direction: Direction in which speed-dial content will show. Possible values are `top`, `bottom`, `left`, `right`.
    :type string:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param left: Aligns the component towards the left.
    :type boolean:
    :param mode: See description |VSpeedDial_vuetify_link|.
    :type string:
    :param open_on_hover: Opens speed-dial on hover
    :type boolean:
    :param origin: See description |VSpeedDial_vuetify_link|.
    :type string:
    :param right: Aligns the component towards the right.
    :type boolean:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param transition: See description |VSpeedDial_vuetify_link|.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-speed-dial", children, **kwargs)
        self._attr_names += [
            "absolute",
            "bottom",
            "direction",
            "fixed",
            "left",
            "mode",
            "open_on_hover",
            "origin",
            "right",
            "top",
            "transition",
            "value",
        ]


class VStepper(AbstractElement):

    """
    Vuetify's VStepper component. See more info and examples |VStepper_vuetify_link|.

    .. |VStepper_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-stepper" target="_blank">here</a>


    :param alt_labels: Places the labels beneath the step
    :type boolean:
    :param color: See description |VStepper_vuetify_link|.
    :type string:
    :param dark: See description |VStepper_vuetify_link|.
    :type boolean:
    :param elevation: See description |VStepper_vuetify_link|.
    :type ['number', 'string']:
    :param flat: Removes the stepper's elevation.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param non_linear: Allow user to jump to any step
    :type boolean:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param rounded: See description |VStepper_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param value: The designated model value for the component.
    :type any:
    :param vertical: Display steps vertically
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    Events

    :param change: Emitted when step is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-stepper", children, **kwargs)
        self._attr_names += [
            "alt_labels",
            "color",
            "dark",
            "elevation",
            "flat",
            "height",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "non_linear",
            "outlined",
            "rounded",
            "shaped",
            "tag",
            "tile",
            "value",
            "vertical",
            "width",
        ]
        self._event_names += [
            "change",
        ]


class VStepperContent(AbstractElement):

    """
    Vuetify's VStepperContent component. See more info and examples |VStepperContent_vuetify_link|.

    .. |VStepperContent_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-stepper-content" target="_blank">here</a>


    :param step: Sets step to associate the content to
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-stepper-content", children, **kwargs)
        self._attr_names += [
            "step",
        ]


class VStepperStep(AbstractElement):

    """
    Vuetify's VStepperStep component. See more info and examples |VStepperStep_vuetify_link|.

    .. |VStepperStep_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-stepper-step" target="_blank">here</a>


    :param color: See description |VStepperStep_vuetify_link|.
    :type string:
    :param complete: Marks step as complete
    :type boolean:
    :param complete_icon: Icon to display when step is marked as completed
    :type string:
    :param edit_icon: Icon to display when step is editable
    :type string:
    :param editable: Marks step as editable
    :type boolean:
    :param error_icon: Icon to display when step has an error
    :type string:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param step: Content to display inside step circle
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-stepper-step", children, **kwargs)
        self._attr_names += [
            "color",
            "complete",
            "complete_icon",
            "edit_icon",
            "editable",
            "error_icon",
            "rules",
            "step",
        ]
        self._event_names += [
            # click, #Implemented in AbstractElement parent class
        ]


class VStepperHeader(AbstractElement):

    """
    Vuetify's VStepperHeader component. See more info and examples |VStepperHeader_vuetify_link|.

    .. |VStepperHeader_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-stepper-header" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-stepper-header", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VStepperItems(AbstractElement):

    """
    Vuetify's VStepperItems component. See more info and examples |VStepperItems_vuetify_link|.

    .. |VStepperItems_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-stepper-items" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-stepper-items", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VSubheader(AbstractElement):

    """
    Vuetify's VSubheader component. See more info and examples |VSubheader_vuetify_link|.

    .. |VSubheader_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-subheader" target="_blank">here</a>


    :param dark: See description |VSubheader_vuetify_link|.
    :type boolean:
    :param inset: Adds indentation (72px)
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-subheader", children, **kwargs)
        self._attr_names += [
            "dark",
            "inset",
            "light",
        ]


class VSwitch(AbstractElement):

    """
    Vuetify's VSwitch component. See more info and examples |VSwitch_vuetify_link|.

    .. |VSwitch_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-switch" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param background_color: Changes the background-color of the input
    :type string:
    :param color: See description |VSwitch_vuetify_link|.
    :type string:
    :param dark: See description |VSwitch_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param false_value: Sets value for falsy state
    :type any:
    :param flat: Display component without elevation. Default elevation for thumb is 4dp, `flat` resets it
    :type boolean:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param input_value: The **v-model** bound value
    :type any:
    :param inset: Enlarge the `v-switch` track to encompass the thumb
    :type boolean:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loading: Displays circular progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - primary, secondary, success, info, warning, error) or a Boolean which uses the component color (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param multiple: Changes expected model to an array
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param ripple: See description |VSwitch_vuetify_link|.
    :type ['boolean', 'object']:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param true_value: Sets value for truthy state
    :type any:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:

    Events

    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-switch", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "background_color",
            "color",
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "false_value",
            "flat",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "input_value",
            "inset",
            "label",
            "light",
            "loading",
            "messages",
            "multiple",
            "persistent_hint",
            "prepend_icon",
            "readonly",
            "ripple",
            "rules",
            "success",
            "success_messages",
            "true_value",
            "validate_on_blur",
            "value",
            "value_comparator",  # JS functions unimplemented
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VSystemBar(AbstractElement):

    """
    Vuetify's VSystemBar component. See more info and examples |VSystemBar_vuetify_link|.

    .. |VSystemBar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-system-bar" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param app: See description |VSystemBar_vuetify_link|.
    :type boolean:
    :param color: See description |VSystemBar_vuetify_link|.
    :type string:
    :param dark: See description |VSystemBar_vuetify_link|.
    :type boolean:
    :param fixed: Applies **position: fixed** to the component.
    :type boolean:
    :param height: Sets the height for the component.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param lights_out: Reduces the system bar opacity.
    :type boolean:
    :param window: Increases the system bar height to 32px (24px default).
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-system-bar", children, **kwargs)
        self._attr_names += [
            "absolute",
            "app",
            "color",
            "dark",
            "fixed",
            "height",
            "light",
            "lights_out",
            "window",
        ]


class VTabs(AbstractElement):

    """
    Vuetify's VTabs component. See more info and examples |VTabs_vuetify_link|.

    .. |VTabs_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tabs" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param align_with_title: Make `v-tabs` lined up with the toolbar title
    :type boolean:
    :param background_color: Changes the background color of the component.
    :type string:
    :param center_active: Forces the selected tab to be centered
    :type boolean:
    :param centered: Centers the tabs
    :type boolean:
    :param color: See description |VTabs_vuetify_link|.
    :type string:
    :param dark: See description |VTabs_vuetify_link|.
    :type boolean:
    :param fixed_tabs: `v-tabs-item` min-width 160px, max-width 360px
    :type boolean:
    :param grow: Force `v-tab`'s to take up all available space
    :type boolean:
    :param height: Sets the height of the tabs bar
    :type ['number', 'string']:
    :param hide_slider: Hide's the generated `v-tabs-slider`
    :type boolean:
    :param icons_and_text: Will stack icon and text vertically
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mobile_breakpoint: Sets the designated mobile breakpoint for the component.
    :type ['string', 'number']:
    :param next_icon: Right pagination icon
    :type string:
    :param optional: Does not require an active item. Useful when using `v-tab` as a `router-link`
    :type boolean:
    :param prev_icon: Left pagination icon
    :type string:
    :param right: Aligns tabs to the right
    :type boolean:
    :param show_arrows: Show pagination arrows if the tab items overflow their container. For mobile devices, arrows will only display when using this prop.
    :type ['boolean', 'string']:
    :param slider_color: Changes the background color of an auto-generated `v-tabs-slider`
    :type string:
    :param slider_size: Changes the size of the slider, **height** for horizontal, **width** for vertical.
    :type ['number', 'string']:
    :param value: The designated model value for the component.
    :type any:
    :param vertical: Stacks tabs on top of each other vertically.
    :type boolean:

    Events

    :param change: Emitted when tab is changed by user interaction. Returns a string if **href** attribute is set and number if it is not.
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tabs", children, **kwargs)
        self._attr_names += [
            "active_class",
            "align_with_title",
            "background_color",
            "center_active",
            "centered",
            "color",
            "dark",
            "fixed_tabs",
            "grow",
            "height",
            "hide_slider",
            "icons_and_text",
            "light",
            "mobile_breakpoint",
            "next_icon",
            "optional",
            "prev_icon",
            "right",
            "show_arrows",
            "slider_color",
            "slider_size",
            "value",
            "vertical",
        ]
        self._event_names += [
            "change",
        ]


class VTab(AbstractElement):

    """
    Vuetify's VTab component. See more info and examples |VTab_vuetify_link|.

    .. |VTab_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tab" target="_blank">here</a>


    :param active_class: See description |VTab_vuetify_link|.
    :type string:
    :param append: See description |VTab_vuetify_link|.
    :type boolean:
    :param dark: See description |VTab_vuetify_link|.
    :type boolean:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param exact: See description |VTab_vuetify_link|.
    :type boolean:
    :param exact_active_class: See description |VTab_vuetify_link|.
    :type string:
    :param exact_path: See description |VTab_vuetify_link|.
    :type boolean:
    :param href: Designates the component as anchor and applies the **href** attribute.
    :type ['string', 'object']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param link: Designates that the component is a link. This is automatic when using the **href** or **to** prop.
    :type boolean:
    :param nuxt: See description |VTab_vuetify_link|.
    :type boolean:
    :param replace: See description |VTab_vuetify_link|.
    :type boolean:
    :param ripple: See description |VTab_vuetify_link|.
    :type ['boolean', 'object']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param target: Designates the target attribute. This should only be applied when using the **href** prop.
    :type string:
    :param to: See description |VTab_vuetify_link|.
    :type ['string', 'object']:

    Events

    :param change: Emitted when tab becomes active
    :param keydown: Emitted when **enter** key is pressed
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tab", children, **kwargs)
        self._attr_names += [
            "active_class",
            "append",
            "dark",
            "disabled",
            "exact",
            "exact_active_class",
            "exact_path",
            "href",
            "light",
            "link",
            "nuxt",
            "replace",
            "ripple",
            "tag",
            "target",
            "to",
        ]
        self._event_names += [
            "change",
            # click, #Implemented in AbstractElement parent class
            "keydown",
        ]


class VTabItem(AbstractElement):

    """
    Vuetify's VTabItem component. See more info and examples |VTabItem_vuetify_link|.

    .. |VTabItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tab-item" target="_blank">here</a>


    :param active_class: See description |VTabItem_vuetify_link|.
    :type string:
    :param disabled: Removes the ability to click or target the component.
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param id: Sets the DOM id on the component
    :type string:
    :param reverse_transition: Sets the reverse transition
    :type ['boolean', 'string']:
    :param transition: See description |VTabItem_vuetify_link|.
    :type ['boolean', 'string']:
    :param value: Sets the value of the tab. If not provided, the index will be used.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tab-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "eager",
            "id",
            "reverse_transition",
            "transition",
            "value",
        ]


class VTabsItems(AbstractElement):

    """
    Vuetify's VTabsItems component. See more info and examples |VTabsItems_vuetify_link|.

    .. |VTabsItems_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tabs-items" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param continuous: If `true`, window will "wrap around" from the last item to the first, and from the first item to the last
    :type boolean:
    :param dark: See description |VTabsItems_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param mandatory: Forces a value to always be selected (if available).
    :type boolean:
    :param max: Sets a maximum number of selections that can be made.
    :type ['number', 'string']:
    :param multiple: Allow multiple selections. The **value** prop must be an _array_.
    :type boolean:
    :param next_icon: Icon used for the "next" button if `show-arrows` is `true`
    :type ['boolean', 'string']:
    :param prev_icon: Icon used for the "prev" button if `show-arrows` is `true`
    :type ['boolean', 'string']:
    :param reverse: Reverse the normal transition direction.
    :type boolean:
    :param show_arrows: Display the "next" and "prev" buttons
    :type boolean:
    :param show_arrows_on_hover: Display the "next" and "prev" buttons on hover. `show-arrows` MUST ALSO be set.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param touch: Provide a custom **left** and **right** function when swiped left or right.
    :type object:
    :param touchless: Disable touch support.
    :type boolean:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:
    :param vertical: Uses a vertical transition when changing windows.
    :type boolean:

    Events

    :param change: Emitted when user swipes between tabs.
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tabs-items", children, **kwargs)
        self._attr_names += [
            "active_class",
            "continuous",
            "dark",
            "light",
            "mandatory",
            "max",
            "multiple",
            "next_icon",
            "prev_icon",
            "reverse",
            "show_arrows",
            "show_arrows_on_hover",
            "tag",
            "touch",
            "touchless",
            "value",
            "value_comparator",  # JS functions unimplemented
            "vertical",
        ]
        self._event_names += [
            "change",
        ]


class VTabsSlider(AbstractElement):

    """
    Vuetify's VTabsSlider component. See more info and examples |VTabsSlider_vuetify_link|.

    .. |VTabsSlider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tabs-slider" target="_blank">here</a>


    :param color: See description |VTabsSlider_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tabs-slider", children, **kwargs)
        self._attr_names += [
            "color",
        ]


class VTextarea(AbstractElement):

    """
    Vuetify's VTextarea component. See more info and examples |VTextarea_vuetify_link|.

    .. |VTextarea_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-textarea" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param auto_grow: Automatically grow the textarea depending on amount of text
    :type boolean:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VTextarea_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VTextarea_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param no_resize: Remove resize handle
    :type boolean:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input's placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param row_height: Height value for each row. Requires the use of the **auto-grow** prop.
    :type ['number', 'string']:
    :param rows: Default row count
    :type ['number', 'string']:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-textarea", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "append_outer_icon",
            "auto_grow",
            "autofocus",
            "background_color",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "label",
            "light",
            "loader_height",
            "loading",
            "messages",
            "no_resize",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "reverse",
            "rounded",
            "row_height",
            "rows",
            "rules",
            "shaped",
            "single_line",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VTextField(AbstractElement):

    """
    Vuetify's VTextField component. See more info and examples |VTextField_vuetify_link|.

    .. |VTextField_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-text-field" target="_blank">here</a>


    :param append_icon: Appends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param append_outer_icon: Appends an icon to the outside the component's input, uses same syntax as `v-icon`
    :type string:
    :param autofocus: Enables autofocus
    :type boolean:
    :param background_color: Changes the background-color of the input
    :type string:
    :param clear_icon: Applied when using **clearable** and the input is dirty
    :type string:
    :param clearable: Add input clear functionality, default icon is Material Design Icons **mdi-clear**
    :type boolean:
    :param color: See description |VTextField_vuetify_link|.
    :type string:
    :param counter: Creates counter for input length; if no number is specified, it defaults to 25. Does not apply any validation.
    :type ['boolean', 'number', 'string']:
    :param counter_value:
    :type function:
    :param dark: See description |VTextField_vuetify_link|.
    :type boolean:
    :param dense: Reduces the input height
    :type boolean:
    :param disabled: Disable the input
    :type boolean:
    :param error: Puts the input in a manual error state
    :type boolean:
    :param error_count: The total number of errors that should display at once
    :type ['number', 'string']:
    :param error_messages: Puts the input in an error state and passes through custom error messages. Will be combined with any validations that occur from the **rules** prop. This field will not trigger validation
    :type ['string', 'array']:
    :param filled: Applies the alternate filled input style
    :type boolean:
    :param flat: Removes elevation (shadow) added to element when using the **solo** or **solo-inverted** props
    :type boolean:
    :param full_width: Designates input type as full-width
    :type boolean:
    :param height: Sets the height of the input
    :type ['number', 'string']:
    :param hide_details: Hides hint and validation errors. When set to `auto` messages will be rendered only if there's a message (hint, error message, counter value etc) to display
    :type ['boolean', 'string']:
    :param hide_spin_buttons: Hides spin buttons on the input when type is set to `number`.
    :type boolean:
    :param hint: Hint text
    :type string:
    :param id: Sets the DOM id on the component
    :type string:
    :param label: Sets input label
    :type string:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param loader_height: Specifies the height of the loader
    :type ['number', 'string']:
    :param loading: Displays linear progress bar. Can either be a String which specifies which color is applied to the progress bar (any material color or theme color - **primary**, **secondary**, **success**, **info**, **warning**, **error**) or a Boolean which uses the component **color** (set by color prop - if it's supported by the component) or the primary color
    :type ['boolean', 'string']:
    :param messages: Displays a list of messages or message if using a string
    :type ['string', 'array']:
    :param outlined: Applies the outlined style to the input
    :type boolean:
    :param persistent_hint: Forces hint to always be visible
    :type boolean:
    :param persistent_placeholder: Forces placeholder to always be visible
    :type boolean:
    :param placeholder: Sets the input’s placeholder text
    :type string:
    :param prefix: Displays prefix text
    :type string:
    :param prepend_icon: Prepends an icon to the component, uses the same syntax as `v-icon`
    :type string:
    :param prepend_inner_icon: Prepends an icon inside the component's input, uses the same syntax as `v-icon`
    :type string:
    :param readonly: Puts input in readonly state
    :type boolean:
    :param reverse: Reverses the input orientation
    :type boolean:
    :param rounded: Adds a border radius to the input
    :type boolean:
    :param rules: Accepts a mixed array of types `function`, `boolean` and `string`. Functions pass an input value as an argument and must return either `true` / `false` or a `string` containing an error message. The input field will enter an error state if a function returns (or any value in the array contains) `false` or is a `string`
    :type array:
    :param shaped: Round if `outlined` and increase `border-radius` if `filled`. Must be used with either `outlined` or `filled`
    :type boolean:
    :param single_line: Label does not move on focus/dirty
    :type boolean:
    :param solo: Changes the style of the input
    :type boolean:
    :param solo_inverted: Reduces element opacity until focused
    :type boolean:
    :param success: Puts the input in a manual success state
    :type boolean:
    :param success_messages: Puts the input in a success state and passes through custom success messages.
    :type ['string', 'array']:
    :param suffix: Displays suffix text
    :type string:
    :param type: Sets input type
    :type string:
    :param validate_on_blur: Delays validation until blur event
    :type boolean:
    :param value: The input's value
    :type any:

    Events

    :param blur: Emitted when the input is blurred
    :param change: Emitted when the input is changed by user interaction
    :param click_append: Emitted when appended icon is clicked
    :param click_append_outer: Emitted when appended outer icon is clicked
    :param click_clear: Emitted when clearable icon clicked
    :param click_prepend: Emitted when prepended icon is clicked
    :param click_prepend_inner: Emitted when prepended inner icon is clicked
    :param focus: Emitted when component is focused
    :param input: The updated bound model
    :param keydown: Emitted when **any** key is pressed
    :param update_error: The `error.sync` event
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-text-field", children, **kwargs)
        self._attr_names += [
            "append_icon",
            "append_outer_icon",
            "autofocus",
            "background_color",
            "clear_icon",
            "clearable",
            "color",
            "counter",
            "counter_value",  # JS functions unimplemented
            "dark",
            "dense",
            "disabled",
            "error",
            "error_count",
            "error_messages",
            "filled",
            "flat",
            "full_width",
            "height",
            "hide_details",
            "hide_spin_buttons",
            "hint",
            "id",
            "label",
            "light",
            "loader_height",
            "loading",
            "messages",
            "outlined",
            "persistent_hint",
            "persistent_placeholder",
            "placeholder",
            "prefix",
            "prepend_icon",
            "prepend_inner_icon",
            "readonly",
            "reverse",
            "rounded",
            "rules",
            "shaped",
            "single_line",
            "solo",
            "solo_inverted",
            "success",
            "success_messages",
            "suffix",
            "type",
            "validate_on_blur",
            "value",
        ]
        self._event_names += [
            "blur",
            "change",
            # click, #Implemented in AbstractElement parent class
            ("click_append", "click:append"),
            ("click_append_outer", "click:append-outer"),
            ("click_clear", "click:clear"),
            ("click_prepend", "click:prepend"),
            ("click_prepend_inner", "click:prepend-inner"),
            "focus",
            "input",
            "keydown",
            # mousedown, #Implemented in AbstractElement parent class
            # mouseup, #Implemented in AbstractElement parent class
            ("update_error", "update:error"),
        ]


class VThemeProvider(AbstractElement):

    """
    Vuetify's VThemeProvider component. See more info and examples |VThemeProvider_vuetify_link|.

    .. |VThemeProvider_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-theme-provider" target="_blank">here</a>


    :param dark: See description |VThemeProvider_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param root: Use the current value of `$vuetify.theme.dark` as opposed to the provided one.
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-theme-provider", children, **kwargs)
        self._attr_names += [
            "dark",
            "light",
            "root",
        ]


class VTimeline(AbstractElement):

    """
    Vuetify's VTimeline component. See more info and examples |VTimeline_vuetify_link|.

    .. |VTimeline_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-timeline" target="_blank">here</a>


    :param align_top: Align caret and dot of timeline items to the top
    :type boolean:
    :param dark: See description |VTimeline_vuetify_link|.
    :type boolean:
    :param dense: Hide opposite slot content, and position all items to one side of timeline
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param reverse: Reverse direction of timeline items
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-timeline", children, **kwargs)
        self._attr_names += [
            "align_top",
            "dark",
            "dense",
            "light",
            "reverse",
        ]


class VTimelineItem(AbstractElement):

    """
    Vuetify's VTimelineItem component. See more info and examples |VTimelineItem_vuetify_link|.

    .. |VTimelineItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-timeline-item" target="_blank">here</a>


    :param color: See description |VTimelineItem_vuetify_link|.
    :type string:
    :param dark: See description |VTimelineItem_vuetify_link|.
    :type boolean:
    :param fill_dot: Remove padding from dot container
    :type boolean:
    :param hide_dot: Hide display of timeline dot
    :type boolean:
    :param icon: Specify icon for dot container
    :type string:
    :param icon_color: See description |VTimelineItem_vuetify_link|.
    :type string:
    :param large: Large size dot
    :type boolean:
    :param left: Explicitly set the item to a left orientation
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param right: Explicitly set the item to a right orientation
    :type boolean:
    :param small: Small size dot
    :type boolean:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-timeline-item", children, **kwargs)
        self._attr_names += [
            "color",
            "dark",
            "fill_dot",
            "hide_dot",
            "icon",
            "icon_color",
            "large",
            "left",
            "light",
            "right",
            "small",
        ]


class VTimePicker(AbstractElement):

    """
    Vuetify's VTimePicker component. See more info and examples |VTimePicker_vuetify_link|.

    .. |VTimePicker_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-time-picker" target="_blank">here</a>


    :param allowed_hours: Restricts which hours can be selected
    :type ['function', 'array']:
    :param allowed_minutes: Restricts which minutes can be selected
    :type ['function', 'array']:
    :param allowed_seconds: Restricts which seconds can be selected
    :type ['function', 'array']:
    :param ampm_in_title: Place AM/PM switch in title, not near the clock.
    :type boolean:
    :param color: See description |VTimePicker_vuetify_link|.
    :type string:
    :param dark: See description |VTimePicker_vuetify_link|.
    :type boolean:
    :param disabled: disables picker
    :type boolean:
    :param elevation: See description |VTimePicker_vuetify_link|.
    :type ['number', 'string']:
    :param flat: Removes  elevation
    :type boolean:
    :param format: Defines the format of a time displayed in picker. Available options are `ampm` and `24hr`.
    :type string:
    :param full_width: Forces 100% width
    :type boolean:
    :param header_color: Defines the header color. If not specified it will use the color defined by <code>color</code> prop or the default picker color
    :type string:
    :param landscape: Orients picker horizontal
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max: Maximum allowed time
    :type string:
    :param min: Minimum allowed time
    :type string:
    :param no_title: Hide the picker title
    :type boolean:
    :param readonly: Puts picker in readonly state
    :type boolean:
    :param scrollable: Allows changing hour/minute with mouse scroll
    :type boolean:
    :param use_seconds: Toggles the use of seconds in picker
    :type boolean:
    :param value: Time picker model (ISO 8601 format, 24hr hh:mm)
    :type any:
    :param width: Width of the picker
    :type ['number', 'string']:

    Events

    :param change: Emitted when the time selection is done (when user changes the minute for HH:MM picker and the second for HH:MM:SS picker
    :param click_hour: Emitted when user selects the hour
    :param click_minute: Emitted when user selects the minute
    :param click_second: Emitted when user selects the second
    :param input: The updated bound model
    :param update_period: Emitted when user clicks the AM/PM button
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-time-picker", children, **kwargs)
        self._attr_names += [
            "allowed_hours",  # JS functions unimplemented
            "allowed_minutes",  # JS functions unimplemented
            "allowed_seconds",  # JS functions unimplemented
            "ampm_in_title",
            "color",
            "dark",
            "disabled",
            "elevation",
            "flat",
            "format",
            "full_width",
            "header_color",
            "landscape",
            "light",
            "max",
            "min",
            "no_title",
            "readonly",
            "scrollable",
            "use_seconds",
            "value",
            "width",
        ]
        self._event_names += [
            "change",
            ("click_hour", "click:hour"),
            ("click_minute", "click:minute"),
            ("click_second", "click:second"),
            "input",
            ("update_period", "update:period"),
        ]


class VToolbar(AbstractElement):

    """
    Vuetify's VToolbar component. See more info and examples |VToolbar_vuetify_link|.

    .. |VToolbar_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-toolbar" target="_blank">here</a>


    :param absolute: Applies position: absolute to the component.
    :type boolean:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param collapse: Puts the toolbar into a collapsed state reducing its maximum width.
    :type boolean:
    :param color: See description |VToolbar_vuetify_link|.
    :type string:
    :param dark: See description |VToolbar_vuetify_link|.
    :type boolean:
    :param dense: Reduces the height of the toolbar content to 48px (96px when using the **prominent** prop).
    :type boolean:
    :param elevation: See description |VToolbar_vuetify_link|.
    :type ['number', 'string']:
    :param extended: Use this prop to increase the height of the toolbar _without_ using the `extension` slot for adding content. May be used in conjunction with the **extension-height** prop, and any of the other props that affect the height of the toolbar, e.g. **prominent**, **dense**, etc., **WITH THE EXCEPTION** of **height**.
    :type boolean:
    :param extension_height: Specify an explicit height for the `extension` slot.
    :type ['number', 'string']:
    :param flat: Removes the toolbar's box-shadow.
    :type boolean:
    :param floating: Applies **display: inline-flex** to the component.
    :type boolean:
    :param height: Designates a specific height for the toolbar. Overrides the heights imposed by other props, e.g. **prominent**, **dense**, **extended**, etc.
    :type ['number', 'string']:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param outlined: Removes elevation (box-shadow) and adds a *thin* border.
    :type boolean:
    :param prominent: Increases the height of the toolbar content to 128px.
    :type boolean:
    :param rounded: See description |VToolbar_vuetify_link|.
    :type ['boolean', 'string']:
    :param shaped: Applies a large border radius on the top left and bottom right of the card.
    :type boolean:
    :param short: Reduce the height of the toolbar content to 56px (112px when using the **prominent** prop).
    :type boolean:
    :param src: See description |VToolbar_vuetify_link|.
    :type ['string', 'object']:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param tile: Removes the component's **border-radius**.
    :type boolean:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-toolbar", children, **kwargs)
        self._attr_names += [
            "absolute",
            "bottom",
            "collapse",
            "color",
            "dark",
            "dense",
            "elevation",
            "extended",
            "extension_height",
            "flat",
            "floating",
            "height",
            "light",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "outlined",
            "prominent",
            "rounded",
            "shaped",
            "short",
            "src",
            "tag",
            "tile",
            "width",
        ]


class VToolbarItems(AbstractElement):

    """
    Vuetify's VToolbarItems component. See more info and examples |VToolbarItems_vuetify_link|.

    .. |VToolbarItems_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-toolbar-items" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-toolbar-items", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VToolbarTitle(AbstractElement):

    """
    Vuetify's VToolbarTitle component. See more info and examples |VToolbarTitle_vuetify_link|.

    .. |VToolbarTitle_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-toolbar-title" target="_blank">here</a>


    :param tag: Specify a custom tag used on the root element.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-toolbar-title", children, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VTooltip(AbstractElement):

    """
    Vuetify's VTooltip component. See more info and examples |VTooltip_vuetify_link|.

    .. |VTooltip_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tooltip" target="_blank">here</a>


    :param absolute: Applies **position: absolute** to the component.
    :type boolean:
    :param activator: Designate a custom activator when the `activator` slot is not used. String can be any valid querySelector and Object can be any valid Node.
    :type any:
    :param allow_overflow: Removes overflow re-positioning for the content
    :type boolean:
    :param attach: Specifies which DOM element that this component should detach to. String can be any valid querySelector and Object can be any valid Node. This will attach to the root `v-app` component by default.
    :type any:
    :param bottom: Aligns the component towards the bottom.
    :type boolean:
    :param close_delay: Delay (in ms) after which menu closes (when open-on-hover prop is set to true)
    :type ['number', 'string']:
    :param color: See description |VTooltip_vuetify_link|.
    :type string:
    :param content_class: Applies a custom class to the detached element. This is useful because the content is moved to the beginning of the `v-app` component (unless the **attach** prop is provided) and is not targetable by classes passed directly on the component.
    :type string:
    :param disabled: Disables the tooltip
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param internal_activator: Designates whether to use an internal activator
    :type boolean:
    :param left: Aligns the component towards the left.
    :type boolean:
    :param max_width: Sets the maximum width for the content
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the content
    :type ['number', 'string']:
    :param nudge_bottom: Nudge the content to the bottom
    :type ['number', 'string']:
    :param nudge_left: Nudge the content to the left
    :type ['number', 'string']:
    :param nudge_right: Nudge the content to the right
    :type ['number', 'string']:
    :param nudge_top: Nudge the content to the top
    :type ['number', 'string']:
    :param nudge_width: Nudge the content width
    :type ['number', 'string']:
    :param offset_overflow: Causes the component to flip to the opposite side when repositioned due to overflow
    :type boolean:
    :param open_delay: Delay (in ms) after which tooltip opens (when `open-on-hover` prop is set to **true**)
    :type ['number', 'string']:
    :param open_on_click: Designates whether the tooltip should open on activator click
    :type boolean:
    :param open_on_focus:
    :type boolean:
    :param open_on_hover: Designates whether the tooltip should open on activator hover
    :type boolean:
    :param position_x: Used to position the content when not using an activator slot
    :type number:
    :param position_y: Used to position the content when not using an activator slot
    :type number:
    :param right: Aligns the component towards the right.
    :type boolean:
    :param tag: Specifies a custom tag for the activator wrapper
    :type string:
    :param top: Aligns the content towards the top.
    :type boolean:
    :param transition: See description |VTooltip_vuetify_link|.
    :type string:
    :param value: Controls whether the component is visible or hidden.
    :type any:
    :param z_index: The z-index used for the component
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tooltip", children, **kwargs)
        self._attr_names += [
            "absolute",
            "activator",
            "allow_overflow",
            "attach",
            "bottom",
            "close_delay",
            "color",
            "content_class",
            "disabled",
            "eager",
            "internal_activator",
            "left",
            "max_width",
            "min_width",
            "nudge_bottom",
            "nudge_left",
            "nudge_right",
            "nudge_top",
            "nudge_width",
            "offset_overflow",
            "open_delay",
            "open_on_click",
            "open_on_focus",
            "open_on_hover",
            "position_x",
            "position_y",
            "right",
            "tag",
            "top",
            "transition",
            "value",
            "z_index",
        ]


class VTreeview(AbstractElement):

    """
    Vuetify's VTreeview component. See more info and examples |VTreeview_vuetify_link|.

    .. |VTreeview_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-treeview" target="_blank">here</a>


    :param activatable: Allows user to mark a node as active by clicking on it
    :type boolean:
    :param active: Syncable prop that allows one to control which nodes are active. The array consists of the `item-key` of each active item.
    :type array:
    :param active_class: The class applied to the node when active
    :type string:
    :param color: Sets the color of the active node
    :type string:
    :param dark: See description |VTreeview_vuetify_link|.
    :type boolean:
    :param dense: Decreases the height of the items
    :type boolean:
    :param disable_per_node: Prevents disabling children nodes
    :type boolean:
    :param disabled: Disables selection for all nodes
    :type boolean:
    :param expand_icon: Icon used to indicate that a node can be expanded
    :type string:
    :param filter: Custom item filtering function. By default it will use case-insensitive search in item's label.
    :type function:
    :param hoverable: Applies a hover class when mousing over nodes
    :type boolean:
    :param indeterminate_icon: Icon used when node is in an indeterminate state. Only visible when `selectable` is `true`.
    :type string:
    :param item_children: Property on supplied `items` that contains its children
    :type string:
    :param item_disabled: Property on supplied `items` that contains the disabled state of the item
    :type string:
    :param item_key: Property on supplied `items` used to keep track of node state. The value of this property has to be unique among all items.
    :type string:
    :param item_text: Property on supplied `items` that contains its label text
    :type string:
    :param items: An array of items used to build the treeview
    :type array:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param load_children: A function used when dynamically loading children. If this prop is set, then the supplied function will be run if expanding an item that has a `item-children` property that is an empty array. Supports returning a Promise.
    :type function:
    :param loading_icon: Icon used when node is in a loading state
    :type string:
    :param multiple_active: When `true`, allows user to have multiple active nodes at the same time
    :type boolean:
    :param off_icon: Icon used when node is not selected. Only visible when `selectable` is `true`.
    :type string:
    :param on_icon: Icon used when leaf node is selected or when a branch node is fully selected. Only visible when `selectable` is `true`.
    :type string:
    :param open: Syncable prop that allows one to control which nodes are open. The array consists of the `item-key` of each open item.
    :type array:
    :param open_all: When `true` will cause all branch nodes to be opened when component is mounted
    :type boolean:
    :param open_on_click: When `true` will cause nodes to be opened by clicking anywhere on it, instead of only opening by clicking on expand icon. When using this prop with `activatable` you will be unable to mark nodes with children as active.
    :type boolean:
    :param return_object: When `true` will make `v-model`, `active.sync` and `open.sync` return the complete object instead of just the key
    :type boolean:
    :param rounded: Provides an alternative active style for `v-treeview` node. Only visible when `activatable` is `true` and should not be used in conjunction with the `shaped` prop.
    :type boolean:
    :param search: The search model for filtering results
    :type string:
    :param selectable: Will render a checkbox next to each node allowing them to be selected
    :type boolean:
    :param selected_color: The color of the selection checkbox
    :type string:
    :param selection_type: Controls how the treeview selects nodes. There are two modes available: 'leaf' and 'independent'
    :type string:
    :param shaped: Provides an alternative active style for `v-treeview` node. Only visible when `activatable` is `true` and should not be used in conjunction with the `rounded` prop.
    :type boolean:
    :param transition: Applies a transition when nodes are opened and closed
    :type boolean:
    :param value: Allows one to control which nodes are selected. The array consists of the `item-key` of each selected item. Is used with `@input` event to allow for `v-model` binding.
    :type array:

    Events

    :param input: Emits the array of selected items when this value changes
    :param update_active: Emits the array of active items when this value changes
    :param update_open: Emits the array of open items when this value changes
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-treeview", children, **kwargs)
        self._attr_names += [
            "activatable",
            "active",
            "active_class",
            "color",
            "dark",
            "dense",
            "disable_per_node",
            "disabled",
            "expand_icon",
            "filter",  # JS functions unimplemented
            "hoverable",
            "indeterminate_icon",
            "item_children",
            "item_disabled",
            "item_key",
            "item_text",
            "items",
            "light",
            "load_children",  # JS functions unimplemented
            "loading_icon",
            "multiple_active",
            "off_icon",
            "on_icon",
            "open",
            "open_all",
            "open_on_click",
            "return_object",
            "rounded",
            "search",
            "selectable",
            "selected_color",
            "selection_type",
            "shaped",
            "transition",
            "value",
        ]
        self._event_names += [
            "input",
            ("update_active", "update:active"),
            ("update_open", "update:open"),
        ]


class VVirtualScroll(AbstractElement):

    """
    Vuetify's VVirtualScroll component. See more info and examples |VVirtualScroll_vuetify_link|.

    .. |VVirtualScroll_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-virtual-scroll" target="_blank">here</a>


    :param bench: The number of items **outside** the user view that are rendered (even if they are **not** viewable); to help prevent empty white space when scrolling *fast*.
    :type ['number', 'string']:
    :param height: Height of the component as a css value
    :type ['number', 'string']:
    :param item_height: Height in pixels of the items to display
    :type ['number', 'string']:
    :param items: The array of items to display
    :type array:
    :param max_height: Sets the maximum height for the component.
    :type ['number', 'string']:
    :param max_width: Sets the maximum width for the component.
    :type ['number', 'string']:
    :param min_height: Sets the minimum height for the component.
    :type ['number', 'string']:
    :param min_width: Sets the minimum width for the component.
    :type ['number', 'string']:
    :param width: Sets the width for the component.
    :type ['number', 'string']:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-virtual-scroll", children, **kwargs)
        self._attr_names += [
            "bench",
            "height",
            "item_height",
            "items",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "width",
        ]


class VWindow(AbstractElement):

    """
    Vuetify's VWindow component. See more info and examples |VWindow_vuetify_link|.

    .. |VWindow_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-window" target="_blank">here</a>


    :param active_class: The **active-class** applied to children when they are activated.
    :type string:
    :param continuous: If `true`, window will "wrap around" from the last item to the first, and from the first item to the last
    :type boolean:
    :param dark: See description |VWindow_vuetify_link|.
    :type boolean:
    :param light: Applies the light theme variant to the component.
    :type boolean:
    :param next_icon: Icon used for the "next" button if `show-arrows` is `true`
    :type ['boolean', 'string']:
    :param prev_icon: Icon used for the "prev" button if `show-arrows` is `true`
    :type ['boolean', 'string']:
    :param reverse: Reverse the normal transition direction.
    :type boolean:
    :param show_arrows: Display the "next" and "prev" buttons
    :type boolean:
    :param show_arrows_on_hover: Display the "next" and "prev" buttons on hover. `show-arrows` MUST ALSO be set.
    :type boolean:
    :param tag: Specify a custom tag used on the root element.
    :type string:
    :param touch: Provide a custom **left** and **right** function when swiped left or right.
    :type object:
    :param touchless: Disable touch support.
    :type boolean:
    :param value: The designated model value for the component.
    :type any:
    :param value_comparator: Apply a custom value comparator function
    :type function:
    :param vertical: Uses a vertical transition when changing windows.
    :type boolean:

    Events

    :param change: Emitted when the component value is changed by user interaction
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-window", children, **kwargs)
        self._attr_names += [
            "active_class",
            "continuous",
            "dark",
            "light",
            "next_icon",
            "prev_icon",
            "reverse",
            "show_arrows",
            "show_arrows_on_hover",
            "tag",
            "touch",
            "touchless",
            "value",
            "value_comparator",  # JS functions unimplemented
            "vertical",
        ]
        self._event_names += [
            "change",
        ]


class VWindowItem(AbstractElement):

    """
    Vuetify's VWindowItem component. See more info and examples |VWindowItem_vuetify_link|.

    .. |VWindowItem_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-window-item" target="_blank">here</a>


    :param active_class: See description |VWindowItem_vuetify_link|.
    :type string:
    :param disabled: Prevents the item from becoming active when using the "next" and "prev" buttons or the `toggle` method
    :type boolean:
    :param eager: Will force the components content to render on mounted. This is useful if you have content that will not be rendered in the DOM that you want crawled for SEO.
    :type boolean:
    :param reverse_transition: Sets the reverse transition
    :type ['boolean', 'string']:
    :param transition: See description |VWindowItem_vuetify_link|.
    :type ['boolean', 'string']:
    :param value: The value used when the component is selected in a group. If not provided, the index will be used.
    :type any:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-window-item", children, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "eager",
            "reverse_transition",
            "transition",
            "value",
        ]


class VCarouselTransition(AbstractElement):

    """
    Vuetify's VCarouselTransition component. See more info and examples |VCarouselTransition_vuetify_link|.

    .. |VCarouselTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-carousel-transition" target="_blank">here</a>


    :param group: See description |VCarouselTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VCarouselTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VCarouselTransition_vuetify_link|.
    :type string:
    :param origin: See description |VCarouselTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-carousel-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VCarouselReverseTransition(AbstractElement):

    """
    Vuetify's VCarouselReverseTransition component. See more info and examples |VCarouselReverseTransition_vuetify_link|.

    .. |VCarouselReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-carousel-reverse-transition" target="_blank">here</a>


    :param group: See description |VCarouselReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VCarouselReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VCarouselReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VCarouselReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-carousel-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VTabTransition(AbstractElement):

    """
    Vuetify's VTabTransition component. See more info and examples |VTabTransition_vuetify_link|.

    .. |VTabTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tab-transition" target="_blank">here</a>


    :param group: See description |VTabTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VTabTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VTabTransition_vuetify_link|.
    :type string:
    :param origin: See description |VTabTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tab-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VTabReverseTransition(AbstractElement):

    """
    Vuetify's VTabReverseTransition component. See more info and examples |VTabReverseTransition_vuetify_link|.

    .. |VTabReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-tab-reverse-transition" target="_blank">here</a>


    :param group: See description |VTabReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VTabReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VTabReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VTabReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-tab-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VMenuTransition(AbstractElement):

    """
    Vuetify's VMenuTransition component. See more info and examples |VMenuTransition_vuetify_link|.

    .. |VMenuTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-menu-transition" target="_blank">here</a>


    :param group: See description |VMenuTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VMenuTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VMenuTransition_vuetify_link|.
    :type string:
    :param origin: See description |VMenuTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-menu-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VFabTransition(AbstractElement):

    """
    Vuetify's VFabTransition component. See more info and examples |VFabTransition_vuetify_link|.

    .. |VFabTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-fab-transition" target="_blank">here</a>


    :param group: See description |VFabTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VFabTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VFabTransition_vuetify_link|.
    :type string:
    :param origin: See description |VFabTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-fab-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogTransition(AbstractElement):

    """
    Vuetify's VDialogTransition component. See more info and examples |VDialogTransition_vuetify_link|.

    .. |VDialogTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-dialog-transition" target="_blank">here</a>


    :param group: See description |VDialogTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VDialogTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VDialogTransition_vuetify_link|.
    :type string:
    :param origin: See description |VDialogTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-dialog-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogBottomTransition(AbstractElement):

    """
    Vuetify's VDialogBottomTransition component. See more info and examples |VDialogBottomTransition_vuetify_link|.

    .. |VDialogBottomTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-dialog-bottom-transition" target="_blank">here</a>


    :param group: See description |VDialogBottomTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VDialogBottomTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VDialogBottomTransition_vuetify_link|.
    :type string:
    :param origin: See description |VDialogBottomTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-dialog-bottom-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogTopTransition(AbstractElement):

    """
    Vuetify's VDialogTopTransition component. See more info and examples |VDialogTopTransition_vuetify_link|.

    .. |VDialogTopTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-dialog-top-transition" target="_blank">here</a>


    :param group: See description |VDialogTopTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VDialogTopTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VDialogTopTransition_vuetify_link|.
    :type string:
    :param origin: See description |VDialogTopTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-dialog-top-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VFadeTransition(AbstractElement):

    """
    Vuetify's VFadeTransition component. See more info and examples |VFadeTransition_vuetify_link|.

    .. |VFadeTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-fade-transition" target="_blank">here</a>


    :param group: See description |VFadeTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VFadeTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VFadeTransition_vuetify_link|.
    :type string:
    :param origin: See description |VFadeTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-fade-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScaleTransition(AbstractElement):

    """
    Vuetify's VScaleTransition component. See more info and examples |VScaleTransition_vuetify_link|.

    .. |VScaleTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-scale-transition" target="_blank">here</a>


    :param group: See description |VScaleTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VScaleTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VScaleTransition_vuetify_link|.
    :type string:
    :param origin: See description |VScaleTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-scale-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollXTransition(AbstractElement):

    """
    Vuetify's VScrollXTransition component. See more info and examples |VScrollXTransition_vuetify_link|.

    .. |VScrollXTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-scroll-x-transition" target="_blank">here</a>


    :param group: See description |VScrollXTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VScrollXTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VScrollXTransition_vuetify_link|.
    :type string:
    :param origin: See description |VScrollXTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-scroll-x-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollXReverseTransition(AbstractElement):

    """
    Vuetify's VScrollXReverseTransition component. See more info and examples |VScrollXReverseTransition_vuetify_link|.

    .. |VScrollXReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-scroll-x-reverse-transition" target="_blank">here</a>


    :param group: See description |VScrollXReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VScrollXReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VScrollXReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VScrollXReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-scroll-x-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollYTransition(AbstractElement):

    """
    Vuetify's VScrollYTransition component. See more info and examples |VScrollYTransition_vuetify_link|.

    .. |VScrollYTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-scroll-y-transition" target="_blank">here</a>


    :param group: See description |VScrollYTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VScrollYTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VScrollYTransition_vuetify_link|.
    :type string:
    :param origin: See description |VScrollYTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-scroll-y-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollYReverseTransition(AbstractElement):

    """
    Vuetify's VScrollYReverseTransition component. See more info and examples |VScrollYReverseTransition_vuetify_link|.

    .. |VScrollYReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-scroll-y-reverse-transition" target="_blank">here</a>


    :param group: See description |VScrollYReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VScrollYReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VScrollYReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VScrollYReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-scroll-y-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideXTransition(AbstractElement):

    """
    Vuetify's VSlideXTransition component. See more info and examples |VSlideXTransition_vuetify_link|.

    .. |VSlideXTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-x-transition" target="_blank">here</a>


    :param group: See description |VSlideXTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VSlideXTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VSlideXTransition_vuetify_link|.
    :type string:
    :param origin: See description |VSlideXTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-x-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideXReverseTransition(AbstractElement):

    """
    Vuetify's VSlideXReverseTransition component. See more info and examples |VSlideXReverseTransition_vuetify_link|.

    .. |VSlideXReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-x-reverse-transition" target="_blank">here</a>


    :param group: See description |VSlideXReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VSlideXReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VSlideXReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VSlideXReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-x-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideYTransition(AbstractElement):

    """
    Vuetify's VSlideYTransition component. See more info and examples |VSlideYTransition_vuetify_link|.

    .. |VSlideYTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-y-transition" target="_blank">here</a>


    :param group: See description |VSlideYTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VSlideYTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VSlideYTransition_vuetify_link|.
    :type string:
    :param origin: See description |VSlideYTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-y-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideYReverseTransition(AbstractElement):

    """
    Vuetify's VSlideYReverseTransition component. See more info and examples |VSlideYReverseTransition_vuetify_link|.

    .. |VSlideYReverseTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-slide-y-reverse-transition" target="_blank">here</a>


    :param group: See description |VSlideYReverseTransition_vuetify_link|.
    :type boolean:
    :param hide_on_leave: Hides the leaving element (no exit animation)
    :type boolean:
    :param leave_absolute: See description |VSlideYReverseTransition_vuetify_link|.
    :type boolean:
    :param mode: See description |VSlideYReverseTransition_vuetify_link|.
    :type string:
    :param origin: See description |VSlideYReverseTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-slide-y-reverse-transition", children, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VExpandTransition(AbstractElement):

    """
    Vuetify's VExpandTransition component. See more info and examples |VExpandTransition_vuetify_link|.

    .. |VExpandTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expand-transition" target="_blank">here</a>


    :param mode: See description |VExpandTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expand-transition", children, **kwargs)
        self._attr_names += [
            "mode",
        ]


class VExpandXTransition(AbstractElement):

    """
    Vuetify's VExpandXTransition component. See more info and examples |VExpandXTransition_vuetify_link|.

    .. |VExpandXTransition_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-expand-x-transition" target="_blank">here</a>


    :param mode: See description |VExpandXTransition_vuetify_link|.
    :type string:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("v-expand-x-transition", children, **kwargs)
        self._attr_names += [
            "mode",
        ]
