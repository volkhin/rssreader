define([
    'jquery',
    'underscore',
    'backbone',
    'views/manage-feed-line',
    'bootstrap'
], function($, _, Backbone, ManageFeedLine) {
    var ManageFeedsWidget = Backbone.View.extend({
        el: $('#manage-feeds-form'),

        initialize: function() {
            _.bindAll(this, 'render', 'show');
            this.listenTo(this.collection, 'sync', this.render);
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'change', this.render);
            this.listenTo(this.collection, 'remove', this.render);
            this.listenTo(this.collection, 'destroy', this.render);
        },

        render: function() {
            this.$('ul').empty();
            var self = this;
            this.collection.each(function(feed) {
                var feedView = new ManageFeedLine({model: feed});
                self.$('ul').append(feedView.render().el);
            });
            return this;
        },

        show: function() {
            this.$el.modal('show');
        }
    });

    return ManageFeedsWidget;
});
