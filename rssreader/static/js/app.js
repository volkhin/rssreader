window.App = {};

App.Entry = Backbone.Model.extend({
    urlRoot: '/api/1/entries'
});


App.EntriesList = Backbone.Collection.extend({
    model: App.Entry,
    url: '/api/1/entries'
});


App.Feed = Backbone.Model.extend({
    urlRoot: '/api/1/feeds'
});


App.FeedsList = Backbone.Collection.extend({
    model: App.Feed,
    url: '/api/1/feeds'
});


App.Settings = Backbone.Model.extend({
    url: '/api/1/settings'
});


App.EntryView = Backbone.View.extend({
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
        this.visible = false;
    },

    render: function() {
        this.$el.empty();
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


App.EntriesView = Backbone.View.extend({
    initialize: function(options) {
        _.bindAll(this, 'render', 'addOne', 'showFeed');
        this.listenTo(this.collection, 'add', this.addOne);
        this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(this.collection, 'reset', this.render);
        globalEvents.on('navigate:feed', this.showFeed);
    },

    render: function() {
        // TODO: it's slow, add all elements at once
        this.$el.children().detach();
        this.collection.forEach(this.addOne);
        return this;
    },

    addOne: function(m, c, opt) {
        var entryView = new App.EntryView({model: m});
        this.$el.append(entryView.render().$el);
    },

    showFeed: function(feed) {
        this.collection.fetch({reset:true, data: {feed_id: feed.get('id')}});
    }
});


App.NavigationView = Backbone.View.extend({
    events: {
        'click .refresh': 'refresh',
        'click .show_most_recent': 'show_most_recent',
        'click .show_starred': 'show_starred',
    },

    initialize: function() {
        _.bindAll(this, 'render');
        this.render();
    },

    render: function() {
        this.$el.empty();
        var obj = $('<ul></ul>');
        obj.append('<li><a class="refresh" href="#">Refresh</a></li>');
        obj.append('<li><a class="show_most_recent" href="#">Most recent</a></li>');
        obj.append('<li><a class="show_starred" href="#">Show starred</a></li>');
        this.$el.append(obj);
        return this;
    },

    refresh: function() {
        this.collection.fetch({reset: true});
    },

    show_most_recent: function() {
        this.collection.fetch({reset:true});
    },

    show_starred: function() {
        this.collection.fetch({
            reset:true,
            data: {starred_only: true, show_read: true}
        });
    }
});

App.ShowReadWidget = Backbone.View.extend({
    tagName: 'li',

    template: _.template('<%= show %> / <%= hide %> read items'),

    events: {
        'click .show_read': 'showRead',
        'click .hide_read': 'hideRead',
    },

    initialize: function() {
        _.bindAll(this, 'render', 'showRead', 'hideRead');
        this.listenTo(this.model, 'change:show_read', this.render);
    },

    render: function() {
        var show = $('<span class="show_read">show</span>');
        var hide = $('<span class="hide_read">hide</span>');
        var showWrapper = (this.model.get('show_read') === true) ?
            '<strong />' : '<a href="#">';
        show.wrapInner(showWrapper);
        var hideWrapper = (this.model.get('show_read') === false) ?
            '<strong />' : '<a href="#">';
        hide.wrapInner(hideWrapper);
        this.$el.html(this.template({
            show: show[0].outerHTML,
            hide: hide[0].outerHTML
        }));
        return this;
    },

    showRead: function() {
        this.model.save({show_read: true});
    },

    hideRead: function() {
        this.model.save({show_read: false});
    }
});

App.SettingsView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'render');
        this.showReadWidget = new App.ShowReadWidget({model: this.model});
        this.render();
    },

    render: function() {
        this.$el.children().detach();
        this.$el.append(this.showReadWidget.render().$el);
        return this;
    }
});


App.FeedView = Backbone.View.extend({
    tagName: 'li',

    template: _.template('<a href="#"><%= title %></a>'),

    events: {
        'click a': 'onClick',
    },

    initialize: function() {
        _.bindAll(this, 'render', 'onClick');
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    onClick: function() {
        globalEvents.trigger('navigate:feed', this.model);
    }
});


App.FeedsView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'render', 'addOne');
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(this.collection, 'add', this.addOne);
    },

    render: function() {
        this.$el.empty();
        this.collection.forEach(this.addOne);
        return this;
    },

    addOne: function(m) {
        view = new App.FeedView({model: m});
        this.$el.append(view.render().el);
    }
});


App.MainRouter = Backbone.Router.extend({
    routes: {
        "": "index",
        "about": "about"
    },

    index: function() {
    },

    about: function() {
        $('body').html('about page');
    }
});


window.globalEvents = _.extend({}, Backbone.Events);


var settings = new App.Settings();
settings.fetch({reset: true});
var collection = new App.EntriesList();
collection.fetch({reset: true});
var feeds = new App.FeedsList();
feeds.fetch({reset: true});

$(function() {
    var settingsView = new App.SettingsView({
        el: $('#settings'),
        model: settings
    });
    var entriesView = new App.EntriesView({
        el: $('#entries'),
        collection: collection
    });
    var navigationView = new App.NavigationView({
        el: $('#navigation'),
        collection: collection
    });
    var feedsView = new App.FeedsView({
        el: $('#feeds'),
        collection: feeds
    });
    var router = new App.MainRouter();
    Backbone.history.start();
});
