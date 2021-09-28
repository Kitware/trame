from trame import get_app_instance
from trame.html import AbstractElement

# Make sure used module is available
_app = get_app_instance()
if "vuetify" not in _app.vue_use:
    _app.vue_use += ["vuetify"]

# v-alert
class VAlert(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-alert", **kwargs)
        self._attr_names += [
            "border",
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


# v-app
class VApp(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-app", **kwargs)
        self._attr_names += ["id"]


# v-app-bar
class VAppBar(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-app-bar", **kwargs)
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


# v-app-bar-nav-icon
# v-app-bar-title
# v-autocomplete
# v-avatar
# v-badge
# v-banner
# v-bottom-navigation
# v-bottom-sheet
# v-breadcrumbs
# v-breadcrumbs-divider
# v-breadcrumbs-item
# v-btn
class VBtn(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-btn", __content, **kwargs)
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


# v-btn-toggle
class VBtnToggle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-btn-toggle", __content, **kwargs)
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
        ]
        self._event_names += [
            "change",
        ]


# v-calendar
# v-calendar-daily
# v-calendar-monthly
# v-calendar-weekly
# v-card
# v-card-actions
# v-card-subtitle
# v-card-text
# v-card-title
# v-carousel
# v-carousel-item
# v-carousel-reverse-transition
# v-carousel-transition
# v-checkbox
# v-chip
# v-chip-group
# v-chip-outside
# v-col
class VCol(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-col", **kwargs)
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


# v-color-picker
# v-combobox
# v-container
class VContainer(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-container", **kwargs)
        self._attr_names += ["id", "tag", "fluid", "fill_height"]


# v-content
class VContent(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-content", **kwargs)
        self._attr_names += ["tag"]


# v-data-footer
# v-data-iterator
# v-data-table
# v-data-table-header
# v-date-picker
# v-dialog
# v-dialog-bottom-transition
# v-dialog-top-transition
# v-dialog-transition
# v-divider
class VDivider(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-divider", **kwargs)
        self._attr_names += ["dark", "inset", "light", "vertical"]


# v-edit-dialog
# v-expand-transition
# v-expand-x-transition
# v-expansion-panel
# v-expansion-panel-content
# v-expansion-panel-header
# v-expansion-panels
# v-fab-transition
# v-fade-transition
# v-file-input
# v-flex
# v-footer
# v-form
# v-hover
# v-icon
class VIcon(AbstractElement):
    def __init__(self, __content, **kwargs):
        super().__init__("v-icon", __content, **kwargs)
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


# v-img
# v-input
# v-intersect
# v-item
# v-item-group
# v-layout
# v-lazy
# v-list
# v-list-group
# v-list-item
# v-list-item-action
# v-list-item-action-text
# v-list-item-avatar
# v-list-item-content
# v-list-item-group
# v-list-item-icon
# v-list-item-subtitle
# v-list-item-title
# v-main
class VMain(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-main", **kwargs)
        self._attr_names += ["tag"]


# v-menu
# v-menu-transition
# v-mutate
# v-navigation-drawer
# v-overflow-btn
# v-overlay
# v-pagination
# v-parallax
# v-progress-circular
# v-progress-linear
class VProgressLinear(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-progress-linear", **kwargs)
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
        self._event_names += ["change"]


# v-radio
# v-radio-group
# v-range-slider
# v-rating
# v-resize
# v-responsive
# v-ripple
# v-row
class VRow(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-row", **kwargs)
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
            "no_gutter",
            "tag",
        ]


# v-scale-transition
# v-scroll
# v-scroll-x-reverse-transition
# v-scroll-x-transition
# v-scroll-y-reverse-transition
# v-scroll-y-transition
# v-select
class VSelect(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-select", **kwargs)
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
            "hint",
            "id",
            "item_color",
            "item_disabled",
            "item_text",
            "item_value",
            "items",
            "label",
            "light",
            "loader_height",
            "loading",
            "menu_props",
            "messages",
            "multiple",
            "open_on_clear",
            "outlined",
            "persitent_hint",
            "persitent_placeholder",
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
        ]
        self._event_names += [
            "blur",
            "change",
            "click",
            "click_append",
            "click_append_outer",
            "click_clear",
            "click_prepend",
            "click_prepend_inner",
            "focus",
            "input",
        ]


# v-sheet
# v-simple-checkbox
# v-simple-table
# v-skeleton-loader
# v-slide-group
# v-slide-item
# v-slide-x-reverse-transition
# v-slide-x-transition
# v-slide-y-reverse-transition
# v-slide-y-transition
# v-slider
class VSlider(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-slider", **kwargs)
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
            "click",
            ("click_append", "click:append"),
            ("click_prepend", "click:prepend"),
            "end",
            "input",
            "start",
            "mousedown",
            "mouseup",
        ]


# v-snackbar
# v-spacer
class VSpacer(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-spacer", **kwargs)


# v-sparkline
# v-speed-dial
# v-stepper
# v-stepper-content
# v-stepper-header
# v-stepper-items
# v-stepper-step
# v-subheader
# v-switch
class VSwitch(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("v-switch", **kwargs)
        self.ttsSensitive()
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
        ]
        self._event_names += [
            "change",
            "click",
            ("click_append", "click:append"),
            ("click_prepend", "click:append"),
            "mousedown",
            "mouseup",
            ("update_error", "update:error"),
        ]


# v-system-bar
# v-tab
# v-tab-item
# v-tab-reverse-transition
# v-tab-transition
# v-tabs
# v-tabs-items
# v-tabs-slider
# v-text-field
# v-textarea
# v-theme-provider
# v-time-picker
# v-timeline
# v-timeline-item
# v-toolbar
# v-toolbar-items
# v-toolbar-title
# v-tooltip
# v-touch
# v-tree-view
# v-virtual-scroll
# v-window
# v-window-item
