odoo.define('bi_ecomerce.cart', function (require) {
    'use strict';
    publicWidget.registry.websiteSaleCartLink = publicWidget.Widget.extend({

    template:'product_buy_now1',    
        
    init: function () {
        this._super.apply(this, arguments);
        this._popoverRPC = null;
    },
    /**
     * @override
     */
    start: function () {
        this._super();
    },
    

    }) 
    
    
});    