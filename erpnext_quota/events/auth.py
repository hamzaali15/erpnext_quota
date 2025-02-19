import frappe
from frappe import _
from frappe.utils.data import today, date_diff, get_datetime_str
import json

def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """
    with open(frappe.get_site_path('quota.json')) as jsonfile:
        parsed = json.load(jsonfile)
    
    valid_till = parsed['valid_till']
    diff = date_diff(valid_till, today())
    if diff < 0:
        frappe.throw(_("You site is suspended. Please contact Sales"), frappe.AuthenticationError)

    warning_before_days = parsed['warning_before_days']
    if diff < warning_before_days:
        frappe.msgprint(_("Your subscription has expired. To keep using App without intruption activate it before '{0}' DAYS").format(diff))