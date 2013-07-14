define([
    'jquery',
    'underscore',
    'backbone',
    'bootstrap'
], function($, _, Backbone) {
    var SubscriptionWidget = Backbone.View.extend({
        tagName: 'li',

        link_template: _.template('<a href="#">Subscribe to feed...</a>'),

        form_template: _.template($('#subscription-form').html()),

        events: {
            'click a': 'onClick'
        },

        initialize: function(options) {
            _.bindAll(this, 'render', 'onClick');
            console.log(options, this);
        },

        render: function() {
            this.$el.html(this.link_template());
            return this;
        },

        onClick: function() {
            var self = this;
            var modalForm = $(this.form_template());
            modalForm.on('hidden', function(e) {
                modalForm.remove();
            });
            modalForm.on('shown', function(e) {
                modalForm.find('#url').focus();
            });
            modalForm.find('#url-form').submit(function(e) {
                // TODO: validate enetered url, both on client and server?
                if (modalForm.find('#url').is(':invalid')) {
                    return false;
                }
                self.collection.create({
                    url: modalForm.find('#url').val()
                }, {
                    wait: true
                });
                modalForm.modal('hide');
            });
            modalForm.find('#opml-form').find(':button').click(function(e) {
                // FIXME: user relative url, not /upload_opml
                modalForm.find('#opml').upload('/upload_opml', function(res) {
                });
                modalForm.modal('hide');
                return false;
            });
            modalForm.modal('show');
            return false;
        }
    });

    return SubscriptionWidget;
});
