import os
import conf

#
#  для работы необходимо создать файл conf.py со следующим содержимым
#  *после копирования убрать 'conf' вначале
#
#  conf.phone_path = '/fo/bar'
#  conf.pc_ip      = 'user@192.168.0.1'
#  conf.pc_path    = '/fo/bar'
#

# получаем список файлов на телефоне (запись включает: полный путь и только имя)
def list_photos(inp_phone_path):
    list_photos = []
    for current_dir, dirs, files in os.walk(inp_phone_path):
        for file in files:
            list_photos.append({'full': current_dir+'/'+file, 'name': file})
    return list_photos

# проверяем на предмет коллизий имен (True - есть коллизия, и просто так сопоставить пути и имена не сможем)
def list_photos_conflict(inp_list_photos):
    for photo1 in inp_list_photos:
        count = 0
        for photo2 in inp_list_photos:
            if photo1['name'] == photo2['name']:
                count += 1
        if count != 1:
            return True
    return False

# запрашиваем список файлов на сервере и выбираем из нашего списка те файлы, которых на сервере нет
def list_photos_filter(inp_pc_ip, inp_pc_path, inp_list_photos):
    sshout = os.popen(f"ssh {inp_pc_ip} -t \"find '{inp_pc_path}' -exec basename '{{}}' ';'\"").read().strip()
    sshout = sshout.split('\n')
    ret = list(filter(lambda x: x['name'] not in sshout, inp_list_photos))
    print('шаг 3 (сверка): ' + repr(ret))
    return ret

# используем scp для отобранных файлов, полученных на предыдущем шаге
def send_list(inp_pc_ip, inp_pc_path, inp_list_photos):
    if len(inp_list_photos) == 0:
        print('шаг 4 отменен, нечего отправлять')
        return
    files = ' '.join(list(map(lambda x: '"'+x['full']+'"', inp_list_photos)))
    sshout = os.popen(f"scp {files} {inp_pc_ip}:{inp_pc_path}/inbox/").read().strip()
    print('шаг 4 (отправка): ' + repr(sshout))

# все это вызываем
list_photos_tmp = list_photos(conf.phone_path)
if list_photos_conflict(list_photos_tmp):
    print('Возник конфликт имен (в разных папках есть файлы, с совпадающим именем)')
else:
    print('Шаги 1 и 2 пройдены (список файлов получен и он валидный)')
    send_list(
        conf.pc_ip,
        conf.pc_path,
        list_photos_filter(
            conf.pc_ip,
            conf.pc_path,
            list_photos_tmp
        )
    )
