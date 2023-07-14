window.trame_splitpanes = {
    install(vue) {
        Object.keys(window.splitpanes).forEach((name) => {
            vue.component(name, window.splitpanes[name]);
        });
    }
}