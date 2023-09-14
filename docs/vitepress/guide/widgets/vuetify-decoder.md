# Modules
## Vuetify
trame leverages Vuetify as its primary UI Component Library. [Vuetify](https://vuetifyjs.com/en/introduction/why-vuetify/#what-is-vuetify3f) is a mature, efficient, and expansive framework for good-looking web applications with the same simple state management system as trame.

trame makes Vuetify available in your Python with minimal overhead. As an example, let's look at how we would make a simple text box. This is taken from Vuetify's excellent [examples and documentation](https://vuetifyjs.com/en/components/text-fields/#icon-slots), which we recommend you consult while writing frontends with trame.
```javascript
// Somewhere in javascript
const currentSuffix = "lbs";
const myWeight = 28.0;
```
```html
<!-- Somewhere in html -->
<v-text-field label="Weight" v-model="myWeight" :suffix="currentSuffix"></v-text-field>
```

![](/assets/images/tutorial/vuetify-example.gif)

Here we have a vuetify text field. The variable `myWeight` is bound by the `v-model` attribute, so our Shared State can can write to it and read from it. We've included a label and a suffix for the text box. While the label is a static string, the "`:`" in `:suffix` means we will look up the variable `currentSuffix`. This variable could change to 'kg' if our user prefers the metric system.

We can do the same in our trame app with small modifications:
```python
# Set vars in Shared State
update_state("myWeight", 28)
update_state("currentSuffix", "lbs")

# Somewhere in your view
field = VTextField(label="Weight", v_model="myWeight", suffix=["currentSuffix"])
```
Notice that in our Python we use CamelCase in our component's name, and hyphens become underscores (as in `v_model`). We distinguish the plain string "Weight" from our variable lookup "currentSuffix" by wrapping the latter in a list. Our [API/CheatSheet] has more on how to accomplish common tasks with Vuetify.
