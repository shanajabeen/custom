odoo.define('pos_widget_override.screens', function (require) {
    "use strict";
    
   
    var Screens=require('pos_hr.screens')
     Screens.LoginScreenWidget.include({
        template: 'LoginScreenWidget',
        
        /**
         * @override
         */
        show: function() {
            var self = this;
            this.$('.select-employee').click(function() {
                self.gui.select_employee({
                    'security': true,
                    'current_employee': self.pos.get_cashier(),
                    'title':_t('Change Cashier'),})
                .then(function(employee){
                    self.pos.set_cashier(employee);
                    self.chrome.widget.username.renderElement();
                    self.unlock_screen();
                });
            });

            this.$('.close-session').click(function() {
                self.gui.close();
            });

            this._super();
        },

        /**
         * @override
         */
        barcode_cashier_action: function(code) {
            var self = this;
            return this._super(code).then(function () {
                self.unlock_screen();
            });
        },

        unlock_screen: function() {
            var screen = (this.gui.pos.get_order() ? this.gui.pos.get_order().get_screen_data('previous-screen') : this.gui.startup_screen) || this.gui.startup_screen;
            this.gui.show_screen(screen);
        }
    });

});