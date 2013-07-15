define([
    'jquery',
    'underscore',
    'backbone',
    'bootstrap',
    'jquery-upload'
], function($, _, Backbone) {
    var SubscriptionWidget = Backbone.View.extend({
        el: $('#subscription-form'),

        events: {
            'submit #url-form': 'submitUrl',
            'change #opml-form :file': 'submitOpml',
            'shown': 'onFormShown'
        },

        initialize: function(options) {
            _.bindAll(this, 'show', 'submitUrl', 'submitOpml');
        },

        onFormShown: function() {
            this.$('#url').focus();
        },

        submitUrl: function() {
            // TODO: validate enetered url, both on client and server?
            var self = this;
            if (this.$('#url').is(':invalid')) {
                return false;
            }
            self.collection.create({
                url: self.$('#url').val()
            }, {
                wait: true
            });
            this.$el.modal('hide');
            return false;
        },

        submitOpml: function() {
            // FIXME: user relative url, not /upload_opml
            this.$('input:file').upload('/upload_opml', function(res) {
            });
            this.$el.modal('hide');
            return false;
        },

        show: function() {
            this.$el.modal('show');
        }
    });

    return SubscriptionWidget;
});
