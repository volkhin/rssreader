define([
    'jquery',
    'underscore',
    'backbone',
    'models/entry'
], function($, _, Backbone, Entry) {
    var EntriesList = Backbone.Collection.extend({
        model: Entry,
        url: '/api/1/entries'
    });

    return EntriesList;
});
