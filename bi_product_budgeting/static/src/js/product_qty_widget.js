odoo.define('bi_product_budgeting.ProductQtyWidget', function (require) {
    "use strict";
    
    var core = require('web.core');
    var QWeb = core.qweb;
    
    var Widget = require('web.Widget');
    var widget_registry = require('web.widget_registry');
    var utils = require('web.utils');
    
    var _t = core._t;
    var time = require('web.time');
    
    var ProductQtyWidget = Widget.extend({
        template: 'bi_product_budgeting.ProductQtyWidget',
        events: _.extend({}, Widget.prototype.events, {
            'click .fa-info-circle': '_onClickButton',
        }),
    
        /**
         * @override
         * @param {Widget|null} parent
         * @param {Object} params
         */
        init: function (parent, params) {
            this.data = params.data;
            this._details = [];
            this._super(parent);
        },
    
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
               self._setPopOver();
            });
        },
    
        updateState: function (state) {
            this.$el.popover('dispose');
            var candidate = state.data[this.getParent().currentRow];
            if (candidate) {
                this.data = candidate.data;
                this.renderElement();
    
            }
        },
        _getBranchData: function () {
            var self = this;
            if (this.data.product_id){
            return self._rpc({
                model: 'bi.material.issue.diesel.line',
                method: 'get_product_details',
                args: [{'arg1': this.data.product_id['data']['id']}],
                kwargs: {},
            })
        }
        },
        
        _setPopOver: function () {
            var self = this;
            var x = self._getBranchData();
            if (this.data.product_id){
            x.then(function (value) {
                self._details = value;
                var $content = $(QWeb.render('bi_product_budgeting.QtyAvailablePopOver', {
                details:self._details,
            }));
            var options = {
                content: $content,
                html: true,
                placement: 'left',
                title: _t('Available Quantity'),
                trigger: 'focus',
                delay: {'show': 0, 'hide': 100 },
            };
            self.$el.popover(options);
            });
        }
        },
    
        _onClickButton: function () {
            this.$el.find('.fa-info-circle').prop('special_click', true);
            this._setPopOver();
        },
    });
    
    widget_registry.add('product_qty_widget', ProductQtyWidget);
    
    return ProductQtyWidget;
    });
    