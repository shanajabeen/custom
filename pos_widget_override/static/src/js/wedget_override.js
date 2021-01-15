odoo.define('pos_widget_override.screens', function (require) {
    "use strict";
    
    var Screens=require('pos_hr.screens')
    Screens.LoginScreenWidget.include({
        template: 'LoginScreenWidget',  
        show: function() {
                       
            this._super();
           
        },

    });

});