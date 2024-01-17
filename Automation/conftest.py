'''
Created on 16 Jan 2023

@author: yusuf
'''

import os
import platform
import webbrowser

def pytest_unconfigure(config):
    if platform.system() in ['Darwin', 'Windows']:
        html_report_path = os.path.join(config.invocation_dir.strpath, config.option.htmlpath)
        webbrowser.open("file://%s" % html_report_path)