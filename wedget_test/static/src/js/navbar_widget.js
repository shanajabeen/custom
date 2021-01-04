odoo.define('wedget_test.icon', function (require) {
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    
    // Appends Icon template in system tray (navbar)
    var icon = Widget.extend({
        template:'icon',
        events: {
            'click':'clickWidget',
        },
        clickWidget: function(){
            console.log(1000000000000000);
        },
    });
SystrayMenu.Items.push(icon);

});

