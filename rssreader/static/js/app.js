$(function() {

    var Entry = Backbone.Model.extend({
    });


    var EntriesList = Backbone.Collection.extend({

        model: Entry,

        url: '/api/1/entries'

    });


    var EntryView = Backbone.View.extend({

        tagName: "div",

        template: _.template($('#entry-view-template').html()),

        events: {
            "click .entry-title": "onTitleClick",
            "click .entry-starred": "onStarClick",
            "click .entry-read": "onReadClick",
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
            if (this.visible) {
                this.model.save({ read: true });
            }
            this.render();
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


    var EntriesView = Backbone.View.extend({

        el: $('#entries'),

        initialize: function(options) {
            _.bindAll(this, 'render', 'addOne', 'reset');
            this.listenTo(this.collection, 'all', function(e) {
                console.log('entries', e);
            }); 
            this.listenTo(this.collection, 'add', this.addOne);
            this.listenTo(this.collection, 'sync', this.render);
            this.listenTo(this.collection, 'reset', this.reset);
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

        reset: function() {
            // TODO: it's slow, add all elements at once
            this.$el.html('');
            this.collection.forEach(this.addOne);
        }

    });


    var NavigationView = Backbone.View.extend({

        el: $('#navigation'),

        events: {
            'click .refresh': 'refresh',
            'click .show_unread': 'show_unread',
            'click .show_most_recent': 'show_most_recent',
            'click .show_starred': 'show_starred',
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.render();
        },

        render: function() {
            var obj = $('<ul></ul>');
            obj.append('<li><a class="refresh" href="#">Refresh</a></li>');
            obj.append('<li><a class="show_unread" href="#">All unread</a></li>');
            obj.append('<li><a class="show_most_recent" href="#">Most recent</a></li>');
            obj.append('<li><a class="show_starred" href="#">Show starred</a></li>');
            this.$el.html(obj.html());
        },

        refresh: function() {
            this.collection.fetch({reset: true});
        },

        show_unread: function() {
            this.collection.fetch({reset:true, data: {show_read: false}});
        },

        show_most_recent: function() {
            this.collection.fetch({reset:true, data: {show_read: true}});
        },

        show_starred: function() {
            this.collection.fetch({reset:true,
                data: {starred_only: true, show_read: true}});
        }

    });


    var MainRouter = Backbone.Router.extend({

        routes: {
            "": "index",
            "about": "about"
        },

        index: function() {
            var collection = new EntriesList();
            collection.fetch({reset: true});
            var App = new EntriesView({ collection: collection });
            var Navigation = new NavigationView({ collection: collection });
        },

        about: function() {
            $('body').html('about page');
        }

    });


    var router = new MainRouter();
    Backbone.history.start();

});
