from trame import get_app_instance
from trame.html import AbstractElement

# Make sure used module is available
_app = get_app_instance()
if "vuetify" not in _app.vue_use:
    _app.vue_use += ["vuetify"]


class VApp(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-app", __content, **kwargs)
        self._attr_names += [
            "id",
        ]


class VAppBar(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-app-bar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-app-bar-nav-icon", __content, **kwargs)


class VAppBarTitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-app-bar-title", __content, **kwargs)


class VAlert(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-alert", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-autocomplete", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-avatar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-badge", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-banner", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-bottom-navigation", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-bottom-sheet", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-breadcrumbs", __content, **kwargs)
        self._attr_names += [
            "dark",
            "divider",
            "items",
            "large",
            "light",
        ]


class VBreadcrumbsItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-breadcrumbs-item", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-breadcrumbs-divider", __content, **kwargs)


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


class VCalendar(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-calendar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-calendar-daily", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-calendar-weekly", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-calendar-monthly", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-card", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-card-actions", __content, **kwargs)


class VCardSubtitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-card-subtitle", __content, **kwargs)


class VCardText(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-card-text", __content, **kwargs)


class VCardTitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-card-title", __content, **kwargs)


class VCarousel(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-carousel", __content, **kwargs)
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
            "vertical",
            "vertical_delimiters",
        ]
        self._event_names += [
            "change",
        ]


class VCarouselItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-carousel-item", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-checkbox", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-simple-checkbox", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-chip", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-chip-group", __content, **kwargs)
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
        ]
        self._event_names += [
            "change",
        ]


class VColorPicker(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-color-picker", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-content", __content, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VCombobox(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-combobox", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-data-iterator", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-data-footer", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-data-table", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-edit-dialog", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-data-table-header", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-simple-table", __content, **kwargs)
        self._attr_names += [
            "dark",
            "dense",
            "fixed_header",
            "height",
            "light",
        ]


class VDatePicker(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-date-picker", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-dialog", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-divider", __content, **kwargs)
        self._attr_names += [
            "dark",
            "inset",
            "light",
            "vertical",
        ]


class VExpansionPanels(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expansion-panels", __content, **kwargs)
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
        ]


class VExpansionPanel(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expansion-panel", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expansion-panel-header", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expansion-panel-content", __content, **kwargs)
        self._attr_names += [
            "color",
            "eager",
        ]


class VFileInput(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-file-input", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-footer", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-form", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-container", __content, **kwargs)
        self._attr_names += [
            "fluid",
            "id",
            "tag",
        ]


class VCol(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-col", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-row", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-spacer", __content, **kwargs)


class VLayout(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-layout", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-flex", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-hover", __content, **kwargs)
        self._attr_names += [
            "close_delay",
            "disabled",
            "open_delay",
            "value",
        ]


class VIcon(AbstractElement):
    def __init__(self, __content=None, **kwargs):
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


class VImg(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-img", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-input", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-item", __content, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "value",
        ]


class VItemGroup(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-item-group", __content, **kwargs)
        self._attr_names += [
            "active_class",
            "dark",
            "light",
            "mandatory",
            "max",
            "multiple",
            "tag",
            "value",
        ]
        self._event_names += [
            "change",
        ]


class VLazy(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-lazy", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-action-text", __content, **kwargs)


class VListItemContent(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-content", __content, **kwargs)


class VListItemTitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-title", __content, **kwargs)


class VListItemSubtitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-subtitle", __content, **kwargs)


class VList(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-group", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-action", __content, **kwargs)


class VListItemAvatar(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-avatar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-icon", __content, **kwargs)


class VListItemGroup(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-list-item-group", __content, **kwargs)
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
        ]
        self._event_names += [
            "change",
        ]


class VMain(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-main", __content, **kwargs)
        self._attr_names += [
            "tag",
        ]


class VMenu(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-menu", __content, **kwargs)
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
            "fixed",
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-navigation-drawer", __content, **kwargs)
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


class VOverflowBtn(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-overflow-btn", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-overlay", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-pagination", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-sheet", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-parallax", __content, **kwargs)
        self._attr_names += [
            "alt",
            "height",
            "src",
            "srcset",
        ]


class VProgressCircular(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-progress-circular", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-progress-linear", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-radio-group", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-radio", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-range-slider", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-rating", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-responsive", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-select", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-skeleton-loader", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slider", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-group", __content, **kwargs)
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
        ]
        self._event_names += [
            "change",
            ("click_next", "click:next"),
            ("click_prev", "click:prev"),
        ]


class VSlideItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-item", __content, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "value",
        ]


class VSnackbar(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-snackbar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-sparkline", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-speed-dial", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-stepper", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-stepper-content", __content, **kwargs)
        self._attr_names += [
            "step",
        ]


class VStepperStep(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-stepper-step", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-stepper-header", __content, **kwargs)


class VStepperItems(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-stepper-items", __content, **kwargs)


class VSubheader(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-subheader", __content, **kwargs)
        self._attr_names += [
            "dark",
            "inset",
            "light",
        ]


class VSwitch(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-switch", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-system-bar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tabs", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tab", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tab-item", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tabs-items", __content, **kwargs)
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
            "vertical",
        ]
        self._event_names += [
            "change",
        ]


class VTabsSlider(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tabs-slider", __content, **kwargs)
        self._attr_names += [
            "color",
        ]


class VTextarea(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-textarea", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-text-field", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-theme-provider", __content, **kwargs)
        self._attr_names += [
            "dark",
            "light",
            "root",
        ]


class VTimeline(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-timeline", __content, **kwargs)
        self._attr_names += [
            "align_top",
            "dark",
            "dense",
            "light",
            "reverse",
        ]


class VTimelineItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-timeline-item", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-time-picker", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-toolbar", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-toolbar-items", __content, **kwargs)


class VToolbarTitle(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-toolbar-title", __content, **kwargs)


class VTooltip(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tooltip", __content, **kwargs)
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
            "fixed",
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-treeview", __content, **kwargs)
        self._attr_names += [
            "activatable",
            "active",
            "active_class",
            "color",
            "dark",
            "dense",
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-virtual-scroll", __content, **kwargs)
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
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-window", __content, **kwargs)
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
            "vertical",
        ]
        self._event_names += [
            "change",
        ]


class VWindowItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-window-item", __content, **kwargs)
        self._attr_names += [
            "active_class",
            "disabled",
            "eager",
            "reverse_transition",
            "transition",
            "value",
        ]


class VCarouselTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-carousel-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VCarouselReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-carousel-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VTabTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tab-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VTabReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-tab-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VMenuTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-menu-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VFabTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-fab-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-dialog-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogBottomTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-dialog-bottom-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VDialogTopTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-dialog-top-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VFadeTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-fade-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScaleTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-scale-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollXTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-scroll-x-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollXReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-scroll-x-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollYTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-scroll-y-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VScrollYReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-scroll-y-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideXTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-x-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideXReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-x-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideYTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-y-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VSlideYReverseTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-slide-y-reverse-transition", __content, **kwargs)
        self._attr_names += [
            "group",
            "hide_on_leave",
            "leave_absolute",
            "mode",
            "origin",
        ]


class VExpandTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expand-transition", __content, **kwargs)
        self._attr_names += [
            "mode",
        ]


class VExpandXTransition(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("v-expand-x-transition", __content, **kwargs)
        self._attr_names += [
            "mode",
        ]
