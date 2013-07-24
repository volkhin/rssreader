define([
    'jquery',
    'underscore',
    'backbone',
    'mediator'
], function($, _, Backbone, Mediator) {
    var ShowReadWidget = Backbone.View.extend({
        tagName: 'li',

        template: _.template('<%= show %> / <%= hide %> read items'),

        events: {
            'click .show_read': 'showRead',
            'click .hide_read': 'hideRead',
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.listenTo(this.model, 'change:show_read', this.render);
        },

        render: function() {
            var show = $('<span class="show_read">show</span>');
            var hide = $('<span class="hide_read">hide</span>');
            var showWrapper = (this.model.get('show_read') === true) ?
                '<strong/>' : '<a href="#">';
            show.wrapInner(showWrapper);
            var hideWrapper = (this.model.get('show_read') === false) ?
                '<strong/>' : '<a href="#">';
            hide.wrapInner(hideWrapper);
            this.$el.html(this.template({
                show: show[0].outerHTML,
                hide: hide[0].outerHTML
            }));
            return this;
        },

        showRead: function(e) {
            this.model.save({show_read: true}, {
                success: function() {
                    Mediator.trigger('refresh', true);
                }
            });
            return false;
        },

        hideRead: function(e) {
            this.model.save({show_read: false}, {
                success: function() {
                    Mediator.trigger('refresh', true);
                }
            });
            return false;
        }
    });

    return ShowReadWidget;
});
