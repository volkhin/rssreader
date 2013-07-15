define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var ManageFeedLine = Backbone.View.extend({
        tagName: 'li',

        template: _.template($('#manage-feed-item-template').html()),

        events: {
            'click .remove-feed': 'remove_feed'
        },

        initialize: function() {
            _.bindAll(this, 'render');
        },

        render: function() {
            this.$el.empty();
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },

        remove_feed: function() {
            this.model.destroy();
            return false;
        }
    });

    return ManageFeedLine;
});
