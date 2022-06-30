import locale
import sys
from os import path, chdir

import pandas
from .lib.constants import *
from .lib.calculadora import Calculadora

__version__ = '1.0.0'

# Module arguments.
arguments = {}
positionals = []
for arg in sys.argv[1:]:
    if '--' == arg[:2]:
        if '=' in arg:
            key, val = [x.strip() for x in arg[2:].split('=', 1)]
        else:
            key, val = arg[2:], True
        arguments[key] = val
    else:
        positionals.append(arg)


def run():
    chdir(path.abspath(path.dirname(__file__)))
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.width', None)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    pandas.options.display.float_format = '{:n}'.format
    # pandas.options.display.float_format = 'R$ {:,.2f}'.format
    try:
        if len(sys.argv) > 2 + 1:
            print(
                f"Somente é possível passar dois argumentos: "
                f"<opções> </diretório/dos/extratos>", )
        elif len(sys.argv) < 2 + 1:
            print(
                f"É necessário passar dois argumentos: "
                f"<opções> </diretório/dos/extratos>", )
        else:
            if sys.argv[1] == 'calcular':
                print(Calculadora().run())
            else:
                print(f'Command not valid!')
    except IndexError as e:
        print(e)
