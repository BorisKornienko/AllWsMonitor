"""Getting incoming json-files and put date from it to database, using django context"""
import json
import django
import os
import datetime

from win_events.models import System_critical, System_error, System_warning
from win_events.models import App_critical, App_error, App_warning
from win_events.models import Proceed_date

# path = "c:/distribs/DjangoProject/data_set/"
path = "D:/allwsmonitor_incoming"
for parse_dir in os.listdir(path):
    print(parse_dir)
    path2 = os.path.join(path, parse_dir)
    file_list = os.listdir(path2)
    for parse_file in file_list:
        # именно тут мы прочно привязались к json
        if parse_file.endswith('json'):
                date_proc = parse_file.strip('.json').split("_")
                # тут надо проверить корректность входящей даты
                date_proc = datetime.date(int(date_proc[0]), int(date_proc[1]), int(date_proc[2]))
        else:
            continue
        machine = parse_dir

# Это своеобразная проверка на то, что файлы с этой машины за эту дату еще не были обработаны
        pd = Proceed_date.objects.filter(file_date=date_proc, machine=machine)
        if pd:
            for proc_date in pd:    
                proc_date.file_count = proc_date.file_count + 1
                proc_date.save()
                os.remove(os.path.join(path2, parse_file))
                print("{} removed".format(parse_file))
            continue
        else:
            pd = Proceed_date()
            pd.machine = machine
            pd.file_date = date_proc
            pd.file_count = 1
            pd.save()


        with open((os.path.join(path2, parse_file)), 'r+', encoding='utf-8-sig') as js_file:
            js_file_r = js_file.read()
            if len(js_file_r) == 0:
                pd = Proceed_date()
                pd.machine = machine
                pd.date = datetime.date(1970, 1, 1)
                pd.file_count = 1
                pd.save()
            else:
                try:
                    parsed_js = json.loads(js_file_r)
                except:
                    continue
                parsed_js
                for key, value in parsed_js.items():
                    if key == 'computer' and value.upper() != machine.upper():
                        break
                    if value == 0:
                        continue
                    if key == 'system_warnings':
                        for i_key, i_value in value.items():
                            event = System_warning()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
                    elif key == 'system_errors':
                        for i_key, i_value in value.items():
                            event = System_error()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
                    elif key == 'system_criticals':
                        for i_key, i_value in value.items():
                            event = System_critical()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
                    elif key == 'app_warning':
                        for i_key, i_value in value.items():
                            event = App_warning()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
                    elif key == 'app_errors':
                        for i_key, i_value in value.items():
                            event = App_error()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
                    elif key == 'app_critical':
                        for i_key, i_value in value.items():
                            event = App_critical()
                            event.event_id = str(i_value['id'])
                            event.event_source = str(i_value['source'])
                            event.event_description = str(i_value['description'])
                            event.machine_name = str(i_value['machineName']).upper()
                            event.events_count = i_value['count']
                            event.event_user = str(i_value['user']).upper()
                            event.event_date = date_proc
                            event.save()
