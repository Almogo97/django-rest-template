from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_title = site_header = 'Django'
