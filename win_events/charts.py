import pygal
import datetime

from win_events.models import System_warning, System_error, System_critical

top_events = 16

class SystemWarningPieChart():
    """For render pie chart with top warnings"""
    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'System warnings'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        # two_weeks = datetime.date.today() - datetime.timedelta(days=14)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = {}
        for sys_warn in System_warning.objects.filter(event_date=yesterday):
            if sys_warn.event_id in data.keys():
                data[sys_warn.event_id] += 1
            else:
                data[sys_warn.event_id] = 1
        if len(data) >= top_events:
            # x.items(), key=lambda kv: kv[1]
            data_list = sorted(data.items(), key=lambda kv: kv[1], reverse=True)[:top_events]
            data = {}
            for eventId in data_list:
                data[eventId[0]] = eventId[1] # in this place STRONGLY need comment
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


class SystemErrorPieChart():
    """For pie chart winth top system Errors"""
    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'System errors'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        # two_weeks = datetime.date.today() - datetime.timedelta(days=14)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = {}
        for sys_err in System_error.objects.filter(event_date__gte=yesterday):
            if sys_err.event_id in data.keys():
                data[sys_err.event_id] += 1
            else:
                data[sys_err.event_id] = 1
        if len(data) >= top_events:
            # x.items(), key=lambda kv: kv[1]
            data_list = sorted(data.items(), key=lambda kv: kv[1], reverse=True)[:top_events]
            data = {}
            for eventId in data_list:
                data[eventId[0]] = eventId[1]
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


class SystemCriticalPieChart():
    """For pie chart winth top system Errors"""
    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'System critical errors'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        # two_weeks = datetime.date.today() - datetime.timedelta(days=14)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        data = {}
        for sys_crit in System_critical.objects.filter(event_date__gte=yesterday):
            if sys_crit.event_id in data.keys():
                data[sys_crit.event_id] += 1
            else:
                data[sys_crit.event_id] = 1
        if len(data) >= top_events:
            # x.items(), key=lambda kv: kv[1]
            data_list = sorted(data.items(), key=lambda kv: kv[1], reverse=True)[:top_events]
            data = {}
            for eventId in data_list:
                data[eventId[0]] = eventId[1]
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)