// var trigger = _.wrap(Backbone.Events.trigger, function() {
    // var f = Array.prototype.splice.call(arguments, 0, 1)[0];
    // console.log('event', arguments);
    // f.apply(this, arguments);
// });
// Backbone.Model.prototype.trigger = trigger;
// Backbone.Collection.prototype.trigger = trigger;


define([
    'jquery',
    'underscore',
    'backbone',
    'router'
], function($, _, Backbone, MainRouter) {
    var initialize = function() {
        // Starting router
        var router = new MainRouter();
        Backbone.history.start();
    };

    return {
        initialize: initialize
    };
});
