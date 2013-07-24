define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var Mediator = _.extend({}, Backbone.Events);

    /* Mediator.on('all', function(e, args) {
        console.log('mediator on:', e, args);
    }); */

    return Mediator;
});
