import json
import django
import os
import datetime

from win_events.models import System_critical, System_error, System_warning
from win_events.models import App_critical, App_error, App_warning
from win_events.models import Proceed_date

path = "c:/distribs/DjangoProject/data_set_test/"
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
        # pd = Proceed_date.objects.filter(file_date=date_proc, machine=machine)
        # if pd:
        #     pd.file_count = pd.file_count + 1
        #     pd.save()
        #     os.rename(os.path.join(path2, parse_file), os.path.join(path2, parse_file+'_'))
        #     continue
        # else:
        #     pd = Proceed_date()
        #     pd.machine = machine
        #     pd.file_date = date_proc
        #     pd.file_count = 1
        #     pd.save()


        with open((os.path.join(path2, parse_file)), 'r+', encoding='utf-8-sig') as js_file:
            parsed_js = json.loads(js_file.read())
            for key, value in parsed_js.items():
                if key == 'computer' and value.upper() != machine.upper():
                    break
                if value == 0:
                    continue
                if key == 'system_warnings':
                    for i_key, i_value in value.items():
                        event = System_warning()
                        event.event_id = i_value['id']
                        event.event_source = i_value['source']
                        event.event_description = i_value['description']
                        event.machine_name = i_value['machineName']
                        event.events_count = i_value['count']
                        event.event_user = i_value['user']
                        event.event_date = date_proc
                        event.save()
                elif key == 'system_errors':
                    for i_key, i_value in value.items():
                        event = System_error()
                        event.event_id = i_value['id']
                        event.event_source = i_value['source']
                        event.event_description = i_value['description']
                        event.machine_name = i_value['machineName']
                        event.events_count = i_value['count']
                        event.event_user = i_value['user']
                        event.event_date = date_proc
                        event.save()
                elif key == 'system_criticals':
                    for i_key, i_value in value.items():
                        event = System_critical()
                        event.event_id = i_value['id']
                        event.event_source = i_value['source']
                        event.event_description = i_value['description']
                        event.machine_name = i_value['machineName']
                        event.events_count = i_value['count']
                        event.event_user = i_value['user']
                        event.event_date = date_proc
                        event.save()
