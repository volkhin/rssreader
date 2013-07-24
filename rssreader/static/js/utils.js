define([
    'jquery',
    'jquery-color'
], function($) {
    var highlight = function(obj) {
        if (obj.attr('data-basecolor') !== undefined)
            return;
        obj.attr('data-basecolor', obj.css('background-color'));
        obj
        .css({'background-color': '#ffff99'})
        .animate({
            'background-color': obj.attr('data-basecolor')
        }, 1000, 'linear', function() {
            obj.removeAttr('data-basecolor');
        });
    }

    return {
        highlight: highlight
    };
});
