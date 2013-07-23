define([
    'jquery',
    'underscore',
    'backbone',
    'moment'
], function($, _, Backbone, moment) {
    var EntryView = Backbone.View.extend({
        tagName: "div",

        className: 'entry-container',

        template: _.template($('#entry-view-template').html()),

        events: {
            "click .entry-title": "onTitleClick",
            "click .entry-starred": "onStarClick",
            "click .entry-read": "onReadClick",
        },

        initialize: function() {
            _.bindAll(this, "render");
            this.listenTo(this.model, 'change', this.render);
            this.visible = false;
        },

        render: function() {
            var obj = $(this.template(this.model.toJSON()));
            if (this.visible) {
                obj.find('.entry-content').show();
            } else {
                obj.find('.entry-content').hide();
            }
            this.$el.empty();
            this.$el.append(obj);
            return this;
        },

        onTitleClick: function() {
            this.visible = !this.visible;
            if (this.visible) {
                this.$('.entry-content').show();
                if (this.model.get('read') !== true) {
                    this.model.save({ read: true });
                }
            } else {
                this.$('.entry-content').hide();
            }
        },

        onStarClick: function() {
            starred = this.model.get('starred');
            this.model.save({ starred: !starred });
        },

        onReadClick: function() {
            read = this.model.get('read');
            this.model.save({ read: !read });
        }
    });

    return EntryView;
});
