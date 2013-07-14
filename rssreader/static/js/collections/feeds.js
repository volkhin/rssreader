define([
    'jquery',
    'underscore',
    'backbone',
    'models/feed'
], function($, _, Backbone, Feed) {
    FeedsList = Backbone.Collection.extend({
        model: Feed,
        url: '/api/1/feeds'
    });

    return FeedsList;
});
