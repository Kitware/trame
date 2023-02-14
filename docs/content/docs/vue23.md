# Vue 2/3

trame is starting to enable support for both vue2 and vue3. This mainly mean that it could be worth building components that are compatible with either version. And to achieve that they are several path possible, but ideally you should rely on the composition API to enable a single bundle for both runtime.
Otherwise, you can build "almost the same code" against vue2 and vue3 to produce bundles that can be use for each version of vue independently.

## How to specify vue version at runtime

The __server__ instance now has a `server.client_type` property that you can only be set once to either `vue2` or `vue3`.

In `trame<3.0.0` the `client_type` default is `'vue2'` but it is good to start fixing your version in your code as after `trame>=3.0.0` the default will be `vue3` even if `vue2` will still be supported. Also `trame>=3` will only keep `trame-client` and `trame-server` as dependencies which means it will be the responsibility of the application to list their other trame dependencies such as `trame-vtk`, `trame-vuetify` and so on...

## Building a vue2 package with vite

__package.json__
```json
{
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore --ignore-pattern public"
    },
    "dependencies": {
        "@vitejs/plugin-vue2": "^2.2.0"
    },
    "peerDependencies": {
        "vue": "^2.7.0"
    },
    "devDependencies": {
        "@rushstack/eslint-patch": "^1.1.4",
        "@vue/eslint-config-prettier": "^7.0.0",
        "eslint": "^8.33.0",
        "eslint-plugin-vue": "^9.3.0",
        "prettier": "^2.7.1",
        "vite": "^4.1.0",
        "vue": "^2.7.14"
    },
}
```

__vite.config.js__
```javascript
import { defineConfig } from "vite";
import vue from '@vitejs/plugin-vue2';

export default defineConfig({
  plugins: [vue()],
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_xxx",
      format: "umd",
      fileName: "trame-xxx",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../trame_xxx/module/vue2-serve",
    assetsDir: ".",
  },
});
```

## Building a vue3 package with vite

__package.json__
```json
{
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore --ignore-pattern public"
    },
    "dependencies": {
        "@vitejs/plugin-vue": "^4.0.0"
    },
    "peerDependencies": {
        "vue": "^3.0.0"
    },
    "devDependencies": {
        "@rushstack/eslint-patch": "^1.1.4",
        "@vue/eslint-config-prettier": "^7.0.0",
        "eslint": "^8.33.0",
        "eslint-plugin-vue": "^9.3.0",
        "prettier": "^2.7.1",
        "vite": "^4.1.0",
        "vue": "^3.0.0"
    },
}
```

__vite.config.js__
```javascript
import { defineConfig } from "vite";
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_xxx",
      format: "umd",
      fileName: "trame-xxx",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../trame_xxx/module/vue3-serve",
    assetsDir: ".",
  },
});
```

## Building a vue2/vue3 package with vite

This assume no option API is used but only the composition API.

__package.json__
```json
{
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore --ignore-pattern public"
    },
    "dependencies": {
        "@vitejs/plugin-vue": "^4.0.0"
    },
    "peerDependencies": {
        "vue": "^2.7.0 || ^3.0.0"
    },
    "devDependencies": {
        "@rushstack/eslint-patch": "^1.1.4",
        "@vue/eslint-config-prettier": "^7.0.0",
        "eslint": "^8.33.0",
        "eslint-plugin-vue": "^9.3.0",
        "prettier": "^2.7.1",
        "vite": "^4.1.0",
        "vue": "^3.0.0"
    },
}
```

__vite.config.js__
```javascript
import { defineConfig } from "vite";
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "trame_xxx",
      format: "umd",
      fileName: "trame-xxx",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../trame_xxx/module/serve",
    assetsDir: ".",
  },
});
```

## Python implementation compatibility handling

If you have different physical JS bundle for each vue version you should have those bundles separated like `.../module/vue2.py` and `.../module/vue3.py` which can then internally serve different directories and define their own `vue_use`. And then you should setup a `.../module/__init__.py` like below to switch at runtime.

```python
def setup(server, **kargs):
    client_type = "vue2"
    if hasattr(server, "client_type"):
        client_type = server.client_type

    if client_type == "vue2":
        from . import vue2

        server.enable_module(vue2)
    elif client_type == "vue3":
        from . import vue3

        server.enable_module(vue3)
    else:
        raise TypeError(
            f"Trying to initialize trame_XXXX with unknown client_type={client_type}"
        )
```

Then if internally your Python Widget code, you set dynamic attribute, you may have to do the following:

```python
# vue2/3 handling (add .value for vue3)
if self.server.client_type == "vue2":
    self._attributes["view_id"] = f':viewId="{self.__view_key_id}"'
else:
    self._attributes["view_id"] = f':viewId="{self.__view_key_id}.value"'
```

## Python usage

With vue3, the reactive variable needs to be managed in a slightly different manner which means you should expect the following difference

__vue2__

```python
vuetify.VSlider(v_model="resolution")
```

__vue3__

```python
vuetify3.VSlider(v_model="resolution.value")
# or
vuetify3.VSlider(v_model="state.resolution")
```