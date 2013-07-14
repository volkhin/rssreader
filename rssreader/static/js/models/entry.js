define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var Entry = Backbone.Model.extend({
        urlRoot: '/api/1/entries'
    });

    return Entry;
});
