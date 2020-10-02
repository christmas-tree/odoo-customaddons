# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessDenied


class HrWebsite(http.Controller):
    @http.route('/employee/employee/', auth='user', website=True)
    def index(self, **kw):
        Employees = http.request.env['hr.employee']
        current_user = http.request.env.user
        employees_list = []

        if http.request.env.is_admin():
            employees_list = Employees.search([])
        else:
            employees_list = Employees.search([('department_id', '=', current_user.employee_id.department_id.id)])

        return http.request.render('hr_website.listing_employees', {
            'employees': employees_list,
            'is_admin': http.request.env.is_admin(),
            'current_employee_id': current_user.employee_id.id,
        })

    @http.route('/employee/employee/info/', auth='user', website=True)
    def list(self, **kw):
        current_user = http.request.env.user
        return http.local_redirect('/employee/employee/{}'.format(current_user.employee_id.id))

    @http.route('/employee/employee/<model("hr.employee"):employee>/', auth='user', website=True)
    def individual(self, employee):
        current_user = http.request.env.user

        if http.request.env.is_admin() or employee.id == current_user.employee_id.id:
            return http.request.render('hr_website.individual_employee', {
                'employee': employee,
            })

        raise AccessDenied("This is an access denied http test")
