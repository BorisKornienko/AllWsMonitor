import csv
from django.shortcuts import render
from django.http import HttpResponse
from win_events.models import System_critical, System_error, System_warning
from win_events.models import App_critical, App_error, App_warning
from win_events.models import Proceed_date

from django.views.generic import TemplateView
from pygal.style import DarkStyle
from .charts import *

import datetime


scales_ws = ('MMK-W-13539.METINVEST.UA', 'MMK-W-13540.METINVEST.UA', 'MMK-Z-0454.METINVEST.UA',\
 'MMK-W-4322.METINVEST.UA', 'MMK-W-4323.METINVEST.UA', 'MMK-W-8887.METINVEST.UA',\
 'MMK-W-4047.METINVEST.UA', 'mmk-w-4038.METINVEST.UA', 'mmk-w-9688.METINVEST.UA', 'MMK-W-9689.METINVEST.UA',\
 'MMK-W-4027.METINVEST.UA', 'MMK-W-6527.METINVEST.UA', 'MMK-W-6528.METINVEST.UA',\
 'MMK-W-6540.METINVEST.UA', 'MMK-W-2951.METINVEST.UA', 'MMK-W-4048.METINVEST.UA', 'MMK-W-10448.METINVEST.UA',\
 'MMK-W-4028.METINVEST.UA', 'MMK-W-9639.METINVEST.UA', 'MMK-W-9840.METINVEST.UA',\
 'MMK-Z-0104.METINVEST.UA', 'MMK-W-4034.METINVEST.UA', 'MMK-W-9839.METINVEST.UA', 'MMK-W-9638.METINVEST.UA',\
 'MMK-W-4049.METINVEST.UA', 'MMK-W-4028.METINVEST.UA', 'MMK-W-10840.METINVEST.UA',\
 'MMK-W-4050.METINVEST.UA', 'MMK-W-6531.METINVEST.UA', 'MMK-W-10839.METINVEST.UA', 'MMK-W-4037.METINVEST.UA',\
 'MMK-W-9738.METINVEST.UA', 'MMK-W-10940.METINVEST.UA', 'MMK-W-4052.METINVEST.UA',\
 'MMK-W-4051.METINVEST.UA', 'MMK-W-3396.METINVEST.UA', 'MMK-W-10941.METINVEST.UA', 'MMK-W-11790.METINVEST.UA',\
 'MMK-W-11789.METINVEST.UA', 'MMK-W-2946.METINVEST.UA', 'MMK-W-9639.METINVEST.UA',\
 'MMK-W-4028.METINVEST.UA', 'MMK-W-2932.METINVEST.UA', 'MMK-W-4039.METINVEST.UA', 'MMK-W-4301.METINVEST.UA',\
 'MMK-W-3544.METINVEST.UA', 'MMK-W-4177.METINVEST.UA', 'MMK-W-4041.METINVEST.UA',\
 'MMK-W-2954.METINVEST.UA', 'MMK-W-4212.METINVEST.UA', 'MMK-W-3459.METINVEST.UA', 'MMK-W-4042.METINVEST.UA',\
 'MMK-W-11452.METINVEST.UA', 'MMK-W-3250.METINVEST.UA', 'MMK-W-4043.METINVEST.UA',\
 'MMK-VES-28-1.METINVEST.UA', 'MMK-VES-28-2.METINVEST.UA', 'MMK-VES-28-3.METINVEST.UA', 'MMK-VES-28-4.METINVEST.UA',\
 'MMK-W-4034.METINVEST.UA', 'MMK-W-10389.METINVEST.UA',\
 'MMK-W-10388.METINVEST.UA', 'MMK-W-10316.METINVEST.UA', 'MMK-W-9938.METINVEST.UA', 'MMK-W-4045.METINVEST.UA',\
 'MMK-Z-0154.METINVEST.UA', 'MMK-W-11352.METINVEST.UA', 'MMK-W-9939.METINVEST.UA',\
 'MMK-W-4046.METINVEST.UA', 'MMK-Z-0155.METINVEST.UA', 'MMK-W-19689.METINVEST.UA', 'MMK-W-16340.METINVEST.UA',\
 'MMK-W-9840.METINVEST.UA', 'MMK-W-9638.METINVEST.UA', 'MMK-W-4038.METINVEST.UA')

def raw_csv_sys(request):
    # create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw_powerbi-sys.csv"'
    # create csv content
    sys_er = System_error.objects.all()
    sys_w = System_warning.objects.all()
    sys_crit = System_critical.objects.all()
    writer = csv.writer(response)
    for line in sys_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system error'])
    for line in sys_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system warning'])
    for line in sys_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system critical'])
    
    return response

def raw_csv_sys_2w(request):
    """raw system data for Power BI at least two weeks"""
    two_weeks = datetime.date.today() - datetime.timedelta(days=14)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw-powerbi-sys-2w.csv"'
    sys_er = System_error.objects.filter(event_date__gt=two_weeks)
    sys_w = System_warning.objects.filter(event_date__gt=two_weeks)
    sys_crit = System_critical.objects.filter(event_date__gt=two_weeks)
    writer = csv.writer(response)
    for line in sys_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system error'])
    for line in sys_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system warning'])
    for line in sys_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system critical'])
    
    return response

def raw_csv_app(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw-powerbi-app.csv"'
    app_er = App_error.objects.all()
    app_w = App_warning.objects.all()
    app_crit = App_critical.objects.all()
    writer = csv.writer(response)
    for line in app_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app error'])
    for line in app_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app warning'])
    for line in app_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app critical'])

    return response

def raw_csv_app_2w(request):
    """raw application data for Power BI at least two weeks"""
    two_weeks = datetime.date.today() - datetime.timedelta(days=14)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw-powerbi-app-2w.csv"'
    app_er = App_error.objects.filter(event_date__gt=two_weeks)
    app_w = App_warning.objects.filter(event_date__gt=two_weeks)
    app_crit = App_critical.objects.filter(event_date__gt=two_weeks)
    writer = csv.writer(response)
    for line in app_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app error'])
    for line in app_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app warning'])
    for line in app_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app critical'])

    return response

def raw_csv_sys_2w_scales(request):
    """raw sys data for PowerBI at last two weeks for scales WS"""
    two_weeks = datetime.date.today() - datetime.timedelta(days=14)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw-powerbi-sys-2w_sc.csv"'
    sys_er = System_error.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    sys_w = System_warning.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    sys_crit = System_critical.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    writer = csv.writer(response)
    for line in sys_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system error'])
    for line in sys_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system warning'])
    for line in sys_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'system critical'])

    return response

def raw_csv_app_2w_scales(request):
    """raw application data for Power BI at least two weeks for scales ws"""
    two_weeks = datetime.date.today() - datetime.timedelta(days=14)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename = "raw-powerbi-app-2w_sc.csv"'
    app_er = App_error.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    app_w = App_warning.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    app_crit = App_critical.objects.filter(event_date__gt=two_weeks).filter(machine_name__in=scales_ws)
    writer = csv.writer(response)
    for line in app_er:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app error'])
    for line in app_w:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app warning'])
    for line in app_crit:
        writer.writerow([line.event_id, line.event_source, line.event_description,
        line.machine_name, line.events_count, line.event_user, line.event_date, 'app critical'])

    return response


class IndexView(TemplateView):
    template_name = 'win_events/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        # Instantiate our chart. We'll keep the size/style/etc.
        # config here in the view instead of `charts.py`.
        cht_syswarn = SystemWarningPieChart(
            height=400,
            width=600,
            explicit_size=True,
            style=DarkStyle
        )

        cht_syserr = SystemErrorPieChart(
            height=400,
            width=600,
            explicit_size=True,
            style=DarkStyle
        )

        cht_syscrit = SystemCriticalPieChart(
            height=400,
            width=600,
            explicit_size=True,
            style=DarkStyle            
        )

        # ========================MAKE IT AS DEF!=================================
        sys_warn_QS = System_warning.objects.filter(event_id__in=cht_syswarn.get_data().keys()).filter(event_date__gte=yesterday)
        sys_warn_list = list(sys_warn_QS)
        sys_warn_yesterday = {}
        for s_w in sys_warn_list:
            sys_warn_yesterday[s_w.event_id] = s_w
        sys_warn_yesterday = list(sys_warn_yesterday.values())
        
        sys_err_QS = System_error.objects.filter(event_id__in=cht_syserr.get_data().keys()).filter(event_date__gte=yesterday)
        sys_err_list = list(sys_err_QS)
        sys_err_yesterday = {}
        for s_e in sys_err_list:
            sys_err_yesterday[s_e.event_id] = s_e
        sys_err_yesterday = list(sys_err_yesterday.values())

        sys_crit_QS = System_critical.objects.filter(event_id__in=cht_syscrit.get_data().keys()).filter(event_date__gte=yesterday)
        sys_crit_list = list(sys_crit_QS)
        sys_crit_yesterday = {}
        for s_c in sys_crit_list:
            sys_crit_yesterday[s_c.event_id] = s_c
        sys_crit_yesterday = list(sys_crit_yesterday.values())
        # ========================MAKE IT AS DEF!=================================END

        # Call the `.generate()` method on our chart object
        # and pass it to template context.
        context['cht_syswarn'] = cht_syswarn.generate()
        context['cht_syserr'] = cht_syserr.generate()
        context['cht_syscrit'] = cht_syscrit.generate()
        context['sys_warns_ystd'] = sys_warn_yesterday
        context['sys_errs_ystd'] = sys_err_yesterday
        context['sys_crits_ystd'] = sys_crit_yesterday
        return context