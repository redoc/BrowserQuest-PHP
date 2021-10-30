function parseJson(text) {
    try {
        return JSON.parse(text);
    } catch(e) {
        console.log("parse json failed: "+text, e)
        return null
    }
};

define(['text!../config/config_build.json'],
    function(build) {
        var config = {
            dev: { url: "ws://59.110.46.185:8000", dispatcher: false },
            build: JSON.parse(build)
        };
        require(['text!../config/config.json'], function(local) {
            config.local = parseJson(local);
        });
        return config;
    }
);