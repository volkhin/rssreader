require.config({
    // baseUrl: '/static/js',
    paths: {
        'jquery': 'libs/jquery',
        'bootstrap': 'libs/bootstrap',
        'underscore': 'libs/underscore',
        'backbone': 'libs/backbone'
    },

    shim: {
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },

        'underscore': {
            exports: '_'
        }
    }
});

require([
        'app',
        ], function(App) {
            App.initialize();
        });
