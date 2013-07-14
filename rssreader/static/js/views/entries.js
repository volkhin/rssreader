define([
    'jquery',
    'underscore',
    'backbone',
    'views/entry'
], function($, _, Backbone, EntryView) {
    var EntriesView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'render', 'addOne');
            this.listenTo(this.collection, 'add', this.addOne);
            // this.listenTo(this.collection, 'sync', this.render); #FIXME
            this.listenTo(this.collection, 'reset', this.render);
        },

        render: function() {
            // TODO: it's slow, add all elements at once
            this.$el.children().detach();
            this.collection.forEach(this.addOne);
            return this;
        },

        addOne: function(m, c, opt) {
            var entryView = new EntryView({model: m});
            this.$el.append(entryView.render().$el);
        }
    });

    return EntriesView;
});
