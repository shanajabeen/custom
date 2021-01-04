# -*- coding: utf-8 -*-

from odoo import models, fields, api


class internal_transfer(models.Model):
    _name ='internal.transfer'
    _description = "Picking Type"
    
    picking_from_id=fields.Many2one('stock.location',string='source')
    transit_id=fields.Many2one('stock.location',string='transit')
    # customer_id=fields.Many2one('res.partner',string='customer')
    operation_type_id=fields.Many2one('stock.picking.type',string='operation_type')
    scheduled_date=fields.Datetime(string="Date",default=fields.Date.today)
    product_id=fields.Many2one('product.product',string='product')
    qty=fields.Integer(string='quantity to reserve')
    qty2=fields.Integer(string='quantity to destination')
    picking_count = fields.Integer(string="Count")
    inventory_picking_id = fields.Many2one('stock.picking', string="Picking Id")
    name = fields.Char('Operation Type',translate=True)
    # sequence_code = fields.Char('Code', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    move_type = fields.Selection([
        ('direct', 'As soon as possible'), ('one', 'When all products are ready')], 'Shipping Policy')
    description_picking = fields.Text('Description of Picking',default="internal transfer")
    # origin=fields.Char(default="hello") 
    move_lines = fields.One2many('stock.move', 'picking_id', string="Stock Moves", copy=True) 
    picking_id= fields.Many2one('stock.picking', string="Picking Id")  
    move_line_ids = fields.Many2many('stock.move.line') 
    dest_location_id=fields.Many2one('stock.location',string='destination')                 
    def reserve(self):
        record = self.env['stock.picking']
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id':self.product_id.id,
            'product_uom_qty':self.qty,
            'description_picking':self.description_picking,
            'name':self.product_id.name,
            'product_uom': 1,
              }))
        pick = {}
       
        pick = {
            'picking_type_id': self.operation_type_id.id,
            # 'partner_id': self.customer_id.id,
            'name':record.product_id.display_name,
            'location_dest_id': self.transit_id.id,
            'location_id': self.picking_from_id.id,
            'move_ids_without_package':new_lines,
            'move_type':self.move_type,
            'company_id':self.company_id.id,
            # 'origin':self.origin,
            'scheduled_date':self.scheduled_date
            #  'picking_id': picking.id,'sequence_code':self.sequence_code,
           
        }
        picking =record.create(pick)
        
        
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate() 

        
    
        move = self.env['stock.move'].create({
            'name': 'Use on MyLocation',
            'location_id':self.picking_from_id.id,
            'location_dest_id':self.transit_id.id,
            'product_id':self.product_id.id,
            'product_uom':self.product_uom_id.id,
            'product_uom_qty':self.qty,
            # 'picking_id': self.picking_id.id,
            # 'move_lines':self.move_lines
        })
        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({'qty_done':self.qty}) 
        move._action_done()

    def validate(self):
        record = self.env['stock.picking']
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id':self.product_id.id,
            'product_uom_qty':self.qty2,
            'description_picking':self.description_picking,
            'name':self.product_id.name,
            'product_uom': 1,
              }))
        pick = {}
       
        pick = {
            'picking_type_id': self.operation_type_id.id,
            # 'partner_id': self.customer_id.id,
            'name':record.product_id.display_name,
            'location_dest_id': self.dest_location_id.id,
            'location_id': self.transit_id.id,
            'move_ids_without_package':new_lines,
            'move_type':self.move_type,
            'company_id':self.company_id.id,
            # 'origin':self.origin,
            'scheduled_date':self.scheduled_date
            #  'picking_id': picking.id,'sequence_code':self.sequence_code,
           
        }
        picking =record.create(pick)
        
       
        
    
        move = self.env['stock.move'].create({
            'name': 'Use on MyLocation',
            'location_id':self.transit_id.id,
            'location_dest_id':self.dest_location_id.id,
            'product_id':self.product_id.id,
            'product_uom':self.product_uom_id.id,
            'product_uom_qty':self.qty2,
            # 'picking_id': self.picking_id.id,
            # 'move_lines':self.move_lines
        })
        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({'qty_done':self.qty2}) 
        move._action_done()

         
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate() 

       