# -*- coding: utf-8 -*-
# Copyright (c) 2013, 9T9iT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
        columns = get_columns()
        #sales_data = frappe.db.sql('''select COALESCE(sum(st.total),0),COALESCE(sum(si.total_taxes_and_charges),0)
        #        from `tabSales Taxes and Charges` st inner join `tabSales Invoice` si on si.name = st.parent
        #                 where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and st.rate > 0'''.format(filters.get("from_date"),filters.get("to_date")))

	sales_data = frappe.db.sql('''select COALESCE(sum(net_total),0),COALESCE(sum(total_taxes_and_charges),0)
                from `tabSales Invoice` si inner join `tabSales Taxes and Charges` tx on si.name=tx.parent
                        where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and tx.rate > 0'''.format(filters.get("from_date"),filters.get("to_date")))


	zero_sales_data = frappe.db.sql('''select COALESCE(sum(net_total),0),COALESCE(sum(total_taxes_and_charges),0)
                from `tabSales Invoice` si inner join `tabSales Taxes and Charges` tx on si.name=tx.parent
                        where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and tx.rate = 0'''.format(filters.get("from_date"),filters.get("to_date")))

	purchase_data = frappe.db.sql('''select COALESCE(sum(net_total),0),COALESCE(sum(total_taxes_and_charges),0)
                from `tabPurchase Invoice` si inner join `tabPurchase Taxes and Charges` tx on si.name=tx.parent
                        where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and tx.rate > 0'''.format(filters.get("from_date"),filters.get("to_date")))

	zero_purchase_data = frappe.db.sql('''select COALESCE(sum(net_total),0),COALESCE(sum(total_taxes_and_charges),0)
                from `tabPurchase Invoice` si inner join `tabPurchase Taxes and Charges` tx on si.name=tx.parent
                        where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and tx.rate = 0'''.format(filters.get("from_date"),filters.get("to_date")))
	#purchase_data = frappe.db.sql('''select COALESCE(sum(pt.total),0),COALESCE(sum(si.total_taxes_and_charges),0) from `tabPurchase Taxes and Charges` pt inner join `tabPurchase Invoice` si on si.name=pt.parent where date(si.posting_date) BETWEEN "{}" and "{}" and si.docstatus = 1 and pt.rate > 0'''.format(filters.get("from_date"),filters.get("to_date")))
	#lst_description = ["Standard rated sales","Sales to registered customers in other GCC States","Sales subject to domestic reverse charge mechanism","Zero rated domestic sales","Exports","Exempt sales","Total sales","Standard rated domestic purchases","Imports subject to VAT either paid at customs or deferred","Imports subject to VAT accounted for through reverse charge mechanis","Purchases subject to domestic reverse charge mechanism","Purchases from non-registered taxpayers, zero-rated/ exempt purchases","Total purchases","Total VAT due for current period","Corrections from previous period (between BHD ±5,000)","VAT credit carried forward from previous period(s)","Net VAT due (or reclaimed)"]
	#frappe.msgprint(frappe.as_json(sales_data[0][0]))
	#data = [[lst_description[0],sales_data[0][0],0.00,sales_data[0][1]],[lst_description[1],0,0,0],[lst_description[2],0,0,0],[lst_description[3],0,0,0],[lst_description[4],0,0,0],[lst_description[5],0,0,0],[lst_description[6],sales_data[0][0],0,sales_data[0][1]],[lst_description[7],purchase_data[0][0],0,purchase_data[0][1]],[lst_description[8],0,0,0],[lst_description[9],0,0,0],[lst_description[10],0,0,0],[lst_description[11],0,0,0],[lst_description[12],purchase_data[0][0],0,purchase_data[0][1]],[lst_description[13],0,0,0],[lst_description[14],0,0,0],[lst_description[15],0,0,0],[lst_description[16],0,0,0]]
	
	

	lst_description = ["Standard Rated Sales","Exempt Sales","<b>Total Sales</b>","Standard Rated Domestic Purchases","Exempt Purchase","<b>Total Purchase</b>","<b>Net Totals</b>"]
	data = [[lst_description[0],sales_data[0][0],sales_data[0][1]],[lst_description[1],zero_sales_data[0][0],0.00],[lst_description[2],sales_data[0][0]+zero_sales_data[0][0],sales_data[0][1]],[lst_description[3],purchase_data[0][0],purchase_data[0][1]],[lst_description[4],zero_purchase_data[0][0],0.00],[lst_description[5],zero_purchase_data[0][0]+purchase_data[0][0],purchase_data[0][1]],[lst_description[6],sales_data[0][0]-purchase_data[0][0]+zero_sales_data[0][0]-zero_purchase_data[0][0],sales_data[0][1]-purchase_data[0][1]]]
	
        return columns, data

def get_columns():
        return [
                _("Description") + ":Data:400",
                _("Amount") + ":Currency:120",
                _("Vat Amount") + ":Currency:120"
            ]

