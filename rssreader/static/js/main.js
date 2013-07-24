require.config({
    // baseUrl: '/static/js',
    paths: {
        'jquery': 'libs/jquery',
        'bootstrap': 'libs/bootstrap',
        'underscore': 'libs/underscore',
        'backbone': 'libs/backbone',
        'jquery-upload': 'libs/jquery.upload-1.0.2',
        'jquery-color': 'libs/jquery.color',
        'moment': 'libs/moment',
        'mousetrap': 'libs/mousetrap'
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
