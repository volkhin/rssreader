define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    Settings = Backbone.Model.extend({
        url: '/api/1/settings'
    });

    return Settings;
});
