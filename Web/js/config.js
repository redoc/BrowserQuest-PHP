define(['text!../config/config_base.json'],
    function(content) {
        var config = JSON.parse(content)
        require(['text!../config/config.json'], function(text) {
            var sub_conifg =  JSON.parse(text);
            Object.assign(config,  sub_conifg)
        });
        return config;
    }
);