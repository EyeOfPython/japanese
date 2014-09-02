#!C:\Users\ruckt\workspace\japanese\env\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'waitress==0.8.9','console_scripts','waitress-serve'
__requires__ = 'waitress==0.8.9'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('waitress==0.8.9', 'console_scripts', 'waitress-serve')()
    )
