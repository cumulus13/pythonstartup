from __future__ import print_function
#from cls import cls
import rlcompleter
import readline
readline.parse_and_bind('tab:complete')
import clipboard
import os
import sys
import inspect
os.environ.update({'PYTHONIOENCODING':'UTF-8'})
if not sys.platform == 'win32':
    os.environ.update({"XDG_SESSION_TYPE":"wayland"})
#def copy(data):
#    clipboard.copy(str(data))


try:
    from IPython import get_ipython
    if get_ipython() is not None:
        print("Running in IPython environment")
        
    else:
        print("Running in standard Python interpreter")
        
        def ls(path=None):
            if path == None:
                path = os.getcwd()
            return os.listdir(path)
        
        def cd(path):
            return os.chdir(path)
        
        def mkdir(path):
            return os.makedirs(path)
        
        def cls():
            if sys.platform == 'win32':
                os.system('cls')
            else:
                os.system('clear')
        
        def pwd():
            return os.getcwd()
        
        
except ImportError:
    print("Running in standard Python interpreter")
    
    def ls(path=None):
        if path == None:
            path = os.getcwd()
        return os.listdir(path)
    
    def cd(path):
        return os.chdir(path)
    
    def mkdir(path):
        return os.makedirs(path)
    
    def cls():
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
    
    def pwd():
        return os.getcwd()
    
    

def get_width():
    width = 111
    try:
        import click
        width = click.get_terminal_size()[0]
    except:
        try:
            import cmdw
            width = cmdw.getWidth()
        except:
            pass
    return width

def setdebug(debug=None, host=None, traceback_debugger_server=None, reset=False):
    if debug:
        os.environ.update({'DEBUG':str(debug)})
    os.environ.update({'DEBUG_SERVER':'1'})
    if host:
        os.environ.update({'DEBUGGER_SERVER':host})
    os.environ.update({'TRACEBACK_DEBUG_SERVER':'1'})
    if traceback_debugger_server:
        os.environ.update({'TRACEBACK_DEBUGGER_SERVER':str(traceback_debugger_server)})
    if reset:
        os.environ.pop('DEBUG')	
        os.environ.pop('DEBUG_SERVER')	
        os.environ.pop('DEBUGGER_SERVER')	
        os.environ.pop('TRACEBACK_DEBUG_SERVER')	
        os.environ.pop('TRACEBACK_DEBUGGER_SERVER')	

def set_debug(debug=None, host=None, traceback_debugger_server=None, reset=False):
    setdebug(debug, host, traceback_debugger_server, reset)


def kill(pid):
    return os.kill(pid, pid)

def expand(env=None):
    if env:
        if sys.version[0] == 3:
            print(os.getenv(env))
        else:
            print(str(os.getenv(env)))
    else:
        for i in os.environ:
            if sys.version[0] == 3:
                print(i, "=", os.environ.get(i))
            else:
                print(str(i, "=", os.environ.get(i)))
def now():
    from datetime import datetime
    return datetime.now().ctime()

def get_source(source):
    if sys.version_info.major == 3:
        from rich.console import Console
        from rich.syntax import Syntax

        console = Console()
        console.print(Syntax(inspect.getsource(source), "python", theme = 'fruity', line_numbers=True, tab_size=2, code_width=get_width()))
        print("WIDTH:", get_width())
    else:
        try:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__module__, source.__module__, get_width())
            os.system(cmd)
        except:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__name__, source.__name__, get_width())
            os.system(cmd)




