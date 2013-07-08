$(function() {
    var Entry = Backbone.Model.extend({
        defaults: {
            title: "[no title]",
            content: "[no content]",
            // read: false,
            // starred: false
        }, 
        initialize: function() {
        },
    });


    var EntriesList = Backbone.Collection.extend({
        model: Entry,
        url: '/api/feeds',
        initialize: function() {
        },
        parse: function(response, options) {
            return response.entries;
        },
    });


    var EntryView = Backbone.View.extend({
        tagName: "div",
        // className: "clickable",
        template: _.template($('#entry-view-template').html()),
        events: {
            "click .entry-title": "onTitleClick",
        },
        initialize: function() {
            _.bindAll(this, "render");
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'all', function(e) {
                console.log('Single entry', e);
            });
            this.visible = false;
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            if (this.visible) {
                this.$('.entry-content').show();
            } else {
                this.$('.entry-content').hide();
            }
            return this;
        },
        onTitleClick: function() {
            this.visible = !this.visible;
            this.model.save({ read: true });
            this.render();
        },
    });


    var EntriesView = Backbone.View.extend({
        el: $('#entries'),
        initialize: function(options) {
            _.bindAll(this, "render");
            /* this.listenTo(this.collection, 'all', function(e) {
                console.log('entries', e);
            }); */
            this.listenTo(this.collection, 'add', this.addOne);
            this.listenTo(this.collection, 'sync', this.render);
            this.$el.prepend($('<div id="info"></div>'));
            this.info = this.$('#info');
        },
        render: function() {
            this.info.html('total entries: ' + this.collection.length);
            return this;
        },
        addOne: function(m, c, opt) {
            var entryView = new EntryView({model: m});
            this.$el.append(entryView.render().el);
        },
    });


    var collection = new EntriesList;
    collection.fetch();
    var App = new EntriesView({collection: collection});
});
