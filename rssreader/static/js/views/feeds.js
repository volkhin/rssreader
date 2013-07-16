define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var FeedsView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render', 'addOne');
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'sync', this.render);
            this.listenTo(this.collection, 'change', this.render);
            this.listenTo(this.collection, 'remove', this.render);
            this.listenTo(this.collection, 'destroy', this.render);
            this.listenTo(this.collection, 'add', this.addOne);
        },

        link_template: _.template($('#entry-nav-link').html()),

        render: function() {
            this.$el.empty();
            this.collection.forEach(this.addOne);
            return this;
        },

        addOne: function(m) {
            link_el = this.link_template(m.toJSON());
            this.$el.append(link_el);
        }
    });

    return FeedsView;
});
