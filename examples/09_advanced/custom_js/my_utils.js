// global trame.utils can be extended by users
// - within template definition, it can be accessed as "utils.my_code.rules.int"
window.trame.utils.my_code = {
    actions: {
        hello(name) {
            alert(`This alert was triggered by my_code for ${name}`)
        },
    },
    rules: {
        number(v) {
            if (Number.isNaN(Number(v))) {
                return "Value needs to be a number";
            }
            return true;
        },
        int(v) {
            if (!Number.isInteger(Number(v))) {
                return "Value needs to be an integer";
            }
            return true;
        }
    }
}