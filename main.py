import conf

#
#  conf.phone_path = '/fo/bar'
#  conf.pc_ip      = '192.168.0.1'
#  conf.pc_path    = '/fo/bar'
#

# получаем список файлов с телефона (полный путь + только имя)
# проверяем на предмет коллизий имен (сможем ли однозначно сопоставить имя и полный путь)
# ssh - передать список имен, и удалить из него те, которые найдем
# ssh - scp всех имен, полученных на предыдущем шаге