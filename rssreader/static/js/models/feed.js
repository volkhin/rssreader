define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var Feed = Backbone.Model.extend({
        defaults: {
            title: '',
        },

        urlRoot: '/api/1/feeds'
    });

    return Feed;
});
