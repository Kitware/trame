window.trame.utils.my_code = {
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