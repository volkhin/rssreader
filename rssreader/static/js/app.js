window.App = {};

var trigger = _.wrap(Backbone.Events.trigger, function() {
    var f = Array.prototype.splice.call(arguments, 0, 1)[0];
    console.log('event', arguments);
    f.apply(this, arguments);
});
// Backbone.Model.prototype.trigger = trigger;
// Backbone.Collection.prototype.trigger = trigger;


App.Entry = Backbone.Model.extend({
    urlRoot: '/api/1/entries'
});


App.EntriesList = Backbone.Collection.extend({
    model: App.Entry,
    url: '/api/1/entries'
});


App.Feed = Backbone.Model.extend({
    defaults: {
        title: '',
    },

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
            this.model.save({ read: true });
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


App.EntriesView = Backbone.View.extend({
    initialize: function(options) {
        _.bindAll(this, 'render', 'addOne');
        this.listenTo(this.collection, 'add', this.addOne);
        // this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(this.collection, 'reset', this.render);
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
    }
});


App.NavigationView = Backbone.View.extend({
    events: {
        'click .refresh': 'refresh',
    },

    initialize: function() {
        _.bindAll(this, 'render');
        this.subscriptionWidget = new App.SubscriptionWidget();
        this.showReadWidget = new App.ShowReadWidget({model: App.settings});
        this.render();
    },

    render: function() {
        this.$el.children().detach();
        this.$el.append(this.subscriptionWidget.render().$el);
        this.$el.append(this.showReadWidget.render().$el);
        this.$el.append($('<li><a class="refresh" href="">Refresh</a></li>'));
        this.$el.append($('<li><a class="show_all" href="/">All entries</a></li>'));
        this.$el.append($('<li><a class="show_starred" href="starred">Show starred</a></li>'));
        return this;
    },

    refresh: function() {
        App.router.refreshPage(true);
        return false;
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

    showRead: function(e) {
        this.model.save({show_read: true});
        return false;
    },

    hideRead: function(e) {
        this.model.save({show_read: false});
        return false;
    }
});


App.SubscriptionWidget = Backbone.View.extend({
    tagName: 'li',

    link_template: _.template('<a href="#">Subscribe to feed...</a>'),

    form_template: _.template($('#subscription-form').html()),

    events: {
        'click a': 'onClick'
    },

    initialize: function() {
        _.bindAll(this, 'render', 'onClick');
    },

    render: function() {
        this.$el.html(this.link_template());
        return this;
    },

    onClick: function() {
        var modalForm = $(this.form_template());
        modalForm.on('hidden', function(e) {
            modalForm.remove();
        });
        modalForm.on('shown', function(e) {
            modalForm.find('#url').focus();
        });
        modalForm.find('form').submit(function(e) {
            // TODO: validate enetered url, both on client and server?
            if (modalForm.find('#url').is(':invalid')) {
                return false;
            }
            App.feeds.create({
                url: modalForm.find('#url').val()
            });
            modalForm.modal('hide');
        });
        modalForm.modal('show');
    }
});


App.FeedsView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'render', 'addOne');
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(this.collection, 'add', this.addOne);
    },

    template: _.template('<li><a href="feeds/<%= id %>"><%- title || url %></a></li>'),

    render: function() {
        this.$el.empty();
        this.collection.forEach(this.addOne);
        return this;
    },

    addOne: function(m) {
        link_el = this.template(m.toJSON());
        this.$el.append(link_el);
    }
});


App.MainRouter = Backbone.Router.extend({
    routes: {
        "": "index",
        "feeds/:id": "showFeed",
        "starred": "showStarred",
    },

    initialize: function() {
        _.bindAll(this, 'refreshPage', 'navigate');
    },

    index: function() {
        App.entries.fetch({reset: true});
    },

    showFeed: function(id) {
        App.entries.fetch({reset:true, data: {feed_id: id}});
    },

    showStarred: function() {
        App.entries.fetch({
            reset:true,
            data: {starred_only: true, show_read: true}
        });
    },

    refreshPage: function(options) {
        this.navigate(document.location.hash, options);
    },

    navigate: function(fragment, options) {
        Backbone.history.fragment = null;
        Backbone.history.navigate(fragment, options);
    }
});


$(function() {
    App.globalEvents = _.extend({}, Backbone.Events);
    App.settings = new App.Settings();
    App.entries = new App.EntriesList();
    App.feeds = new App.FeedsList();

    App.entriesView = new App.EntriesView({
        el: $('#entries'),
        collection: App.entries
    });
    App.navigationView = new App.NavigationView({
        el: $('#navigation'),
        collection: App.entries
    });
    App.feedsView = new App.FeedsView({
        el: $('#feeds'),
        collection: App.feeds
    });
    App.router = new App.MainRouter();
    $(document).on('click', 'a[href]:not([data-bypass])', function(e) {
        var href = {prop: $(this).prop('href'), attr: $(this).attr('href')};
        var root = location.protocol + '//' + location.host;// + app.root;
        if (href.prop.slice(0, root.length) === root) {
            e.preventDefault();
            App.router.navigate(href.attr, true);
        }
    });
    Backbone.history.start();

    App.settings.fetch({reset: true});
    App.feeds.fetch({reset: true});
});
