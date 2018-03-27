# import winreg
# import platform
# import time
#
# os = platform.system()
#
# if (os == 'Windows'):
#
#     INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
#         r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
#         0, winreg.KEY_ALL_ACCESS)
#
#     def set_key(name, value):
#         _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
#         winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
#
#     set_key('ProxyEnable', 1)
#     # set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
#     set_key('ProxyServer', u'167.99.61.206:3128')
#
#
# time.sleep(20)
#
# if (os == 'Windows'):
#     set_key('ProxyEnable', 0)
#
# print("Proxy disabled")

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
