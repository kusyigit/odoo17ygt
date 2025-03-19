# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    pbx_username = fields.Char(string="PBX Username")
    pbx_password = fields.Char(string="PBX Password")
    pbx_api_key = fields.Char(string="PBX API Key")

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    internal_num_code = fields.Char(string="Internal Number Code")

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    def action_call_number(self):
        self.ensure_one()
        
        user = self.env.user
        company = user.company_id
        
        if not self.mobile and not self.phone:
            return
        
        phone_number = self.mobile or self.phone
        
        base_url = "http://45.10.253.205/"
        params = {
            'username': company.pbx_username,
            'password': company.pbx_password,
            'action': 'callnumber',
            'number': phone_number,
            'internal': user.internal_num_code
        }
        
        call_url = base_url + "?" + "&".join(f"{key}={value}" for key, value in params.items())
        
        return {
            'type': 'ir.actions.act_url',
            'url': call_url,
            'target': 'new',
        }
