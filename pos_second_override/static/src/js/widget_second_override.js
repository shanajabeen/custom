odoo.define('pos_second_override.widget_second_override', function (require) {
    "use strict";

var screens = require('point_of_sale.screens');

var models = require('point_of_sale.models');
models.load_fields('product.template', ['discount']);

var bool=models[discount]



screens.OrderWidget.include({

    start: function() {
        this.applyAccessRights();
        
        this.state.bind('change:mode', this.changedMode, this);
        this.pos.bind('change:cashier', this.applyAccessRights, this);
        this.pos.bind('change:cashier', this.applyAccessRights1, this);
        this.changedMode();
        this.$el.find('.numpad-backspace').click(_.bind(this.clickDeleteLastChar, this));
        this.$el.find('.numpad-minus').click(_.bind(this.clickSwitchSign, this));
        this.$el.find('.number-char').click(_.bind(this.clickAppendNewChar, this));
        this.$el.find('.mode-button').click(_.bind(this.clickChangeMode, this));
        this.order_widget = new OrderWidget(this,{ numpad_state: this.numpad.state,});
        
    },

    set_value: function(val) {
        if(true){
            var order = this.pos.get_order();
            if (order.get_selected_orderline()) {
                var mode = this.numpad_state.get('mode');
                if( mode === 'quantity'){
                    order.get_selected_orderline().set_quantity(val);
                }else if( mode === 'discount'){
                    order.get_selected_orderline().set_discount(val);
                }else if( mode === 'price'){
                    var selected_orderline = order.get_selected_orderline();
                    selected_orderline.price_manually_set = true;
                    selected_orderline.set_unit_price(val);
                }
                if (this.pos.config.iface_customer_facing_display) {
                    this.pos.send_current_order_to_customer_facing_display();
                }
            }
        } 
        this._super();
    },

 

    

    });

    });