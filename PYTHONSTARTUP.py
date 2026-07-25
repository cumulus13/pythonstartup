#!/usr/bin/env python
#author: Hadi Cahyadi
#email: cumulus13@gmail.com
#license: MIT

# from __future__ import print_function
import sys
import os
if os.path.abspath(os.getcwd()).lower() == r"c:\projects":
    os.chdir(f"{os.path.splitdrive(os.getcwd())[0]}" + "\\" if sys.platform == 'win32' else '')
print(f"CURRENT DIR: {os.getcwd()}")
# import rlcompleter
import readline

from typing import Union, Optional, Any

exceptions=['pika', 'urllib3', 'urllib2', 'urllib', 'asyncio']
tprint = None  # type: ignore  
os.environ.update({'PYTHONIOENCODING': 'UTF-8'})
os.environ.pop('LOGGING', None)
os.environ.pop('NO_LOGGING', None)

def Logger():

    if str(os.getenv("LOGGER_SETUP", "0")).lower() in ("1", 'yes", "ok", "on'):
        return True

    try:
        from richcolorlog import setup_logging, print_exception as tprint  # type: ignore
        # sys.excepthook = CTraceback()
        logger = setup_logging(__name__, exceptions = exceptions, show_locals=False)
        # print(f"os.getenv('LOGGING'): {os.getenv('LOGGING')}")
        # print(f"os.getenv('NO_LOGGING'): {os.getenv('NO_LOGGING')}")

        os.environ.update({"LOGGER_SETUP": "1"})
        os.environ.update({"LOGGER_TYPE": "rcl"})
        return logger

    except:
        """
        Create a custom logging level:
            EMERGENCY, ALERT, CRITICAL, ERROR,
            WARNING, NOTICE, INFO, DEBUG,
            SUCCESS, FATAL
        With syslog format + additional SUCCESS and FATAL.
        """

        import logging

        # ============================================================
        # 1. LEVEL DEFINITION (Syslog + Extra)
        # ============================================================

        CUSTOM_LOG_LEVELS = {
            # Syslog RFC5424 severity (0 = highest severity)
            # We map to the top of the Python logging range (10–60)
            "EMERGENCY": 60,   # System unusable
            "ALERT":     55,   # Immediate action required
            "CRITICAL":  logging.CRITICAL,  # 50
            "ERROR":     logging.ERROR,     # 40
            "WARNING":   logging.WARNING,   # 30
            "NOTICE":    25,   # Normal but significant condition
            "INFO":      logging.INFO,      # 20
            "DEBUG":     logging.DEBUG,     # 10

            # Custom level tambahan
            "SUCCESS":   22,   # Operation successful
            "FATAL":     65,   # Hard failure beyond CRITICAL
        }

        # ============================================================
        # 2. LEVEL REGISTRATION TO LOGGING
        # ============================================================

        def register_custom_levels():
            for level_name, level_value in CUSTOM_LOG_LEVELS.items():
                # Register for Python logging
                logging.addLevelName(level_value, level_name)

                # Add method to logging.Logger
                def log_for(level):
                    def _log_method(self, message, *args, **kwargs):
                        if self.isEnabledFor(level):
                            self._log(level, message, args, **kwargs)
                    return _log_method

                # create method lowercase: logger.emergency(), logger.notice(), dll
                setattr(logging.Logger, level_name.lower(), log_for(level_value))


        register_custom_levels()

        # ============================================================
        # 3. FORMATTER DETAIL & PROFESSIONAL
        # ============================================================

        DEFAULT_FORMAT = (
            "[%(asctime)s] "
            "%(levelname)-10s "
            "%(name)s: "
            "%(message)s"
        )

        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


        def get_default_handler():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(DEFAULT_FORMAT, DATE_FORMAT)
            handler.setFormatter(formatter)
            return handler


        # ============================================================
        # 4. FUNCTION TO GET THE LOGGER THAT IS READY
        # ============================================================

        def get_logger(name="default", level=logging.DEBUG):
            logger = logging.getLogger(name)
            logger.setLevel(level)

            if not logger.handlers: # Avoid adding multiple handlers
                logger.addHandler(get_default_handler())

            return logger

        logger = get_logger(__name__)
        for exc in exceptions:
            logging.getLogger(exc).setLevel(logging.CRITICAL)

        os.environ.update({"LOGGER_SETUP": "1"})
        os.environ.update({"LOGGER_TYPE": "logging"})

        return logger

if tprint is None:
    import traceback
    def tprint(*args, **kwargs):
        traceback.print_exc(*args, **kwargs)

# Configure environment
readline.parse_and_bind('tab:complete')  # type: ignore
os.environ.update({'PYTHONIOENCODING': 'UTF-8'})
if not sys.platform == 'win32': os.environ.update({"XDG_SESSION_TYPE": "wayland"})  

def rich_setup():
    # Check for optional dependencies

    if str(os.getenv("RICH_AVAILABLE", False)).lower() in ("0", 'true', 'ok', 'yes', 'on'):
        return True

    try:
        from rich.console import Console
        from rich.syntax import Syntax
        from rich import traceback as rich_traceback
        rich_traceback.install(show_locals=False, theme='fruity', width=os.get_terminal_size()[0])
        os.environ.update({"RICH_AVAILABLE": "1"})
        return True
    except:
        pass

    return False

def rich_available():
    return str(os.getenv('RICH_AVAILABLE', False)).lower() in ("1", 'true', '0', 'yes', 'ok')

# print(f"os.getenv('LOGGING')    [2]: {os.getenv('LOGGING')}")
# print(f"os.getenv('NO_LOGGING') [2]: {os.getenv('NO_LOGGING')}")


def pyread_setup():
    if str(os.getenv("PYREAD_AVAILABLE", False)).lower() in ("0", 'true', 'ok', 'yes', 'on'):
        return True

    try:
        from pyread import CodeAnalyzer  # type: ignore
        os.environ.update({"PYREAD_AVAILABLE": "1"})
        return True
    except ImportError:
        pass

    return False

def pyread_available():
    return str(os.getenv('PYREAD_AVAILABLE', False)).lower() in ("1", 'true', '0', 'yes', 'ok')

# print(f"os.getenv('LOGGING')    [3]: {os.getenv('LOGGING')}")
# print(f"os.getenv('NO_LOGGING') [3]: {os.getenv('NO_LOGGING')}")

def setdebug(debug=None, host=None, traceback_debugger_server=None, reset=False):
    """Set debug environment variables."""
    if reset:
        # Safely remove environment variables
        env_vars = [
            'DEBUG', 'DEBUG_SERVER', 'DEBUGGER_SERVER', 
            'TRACEBACK_DEBUG_SERVER', 'TRACEBACK_DEBUGGER_SERVER'
        ]
        for var in env_vars:
            os.environ.pop(var, None)
        print("Debug environment variables reset")
        return
    
    if debug:
        os.environ['DEBUG'] = str(debug)
    
    os.environ['DEBUG_SERVER'] = '1'
    
    if host:
        os.environ['DEBUGGER_SERVER'] = host
    
    os.environ['TRACEBACK_DEBUG_SERVER'] = '1'
    
    if traceback_debugger_server:
        os.environ['TRACEBACK_DEBUGGER_SERVER'] = str(traceback_debugger_server)
    
    print("Debug environment configured")

# print(f"os.getenv('LOGGING')    [1]: {os.getenv('LOGGING')}")
# print(f"os.getenv('NO_LOGGING') [1]: {os.getenv('NO_LOGGING')}")

def set_debug(debug=None, host=None, traceback_debugger_server=None, reset=False):
    """Alias for setdebug()."""
    setdebug(debug, host, traceback_debugger_server, reset)

def kill_process(pid, sig=None):
    """Kill a process by PID."""
    
    import signal

    sig = sig or signal.SIGTERM

    try:
        os.kill(pid, sig)
        print(f"Process {pid} terminated with signal {sig}")
    except OSError as e:
        print(f"Error killing process {pid}: {e}")

def expand(env=None):
    """Display environment variables."""
    if env:
        value = os.getenv(env)
        if value is not None:
            print(f"{env}={value}")
        else:
            print(f"Environment variable '{env}' not found")
    else:
        for key, value in os.environ.items():
            print(f"{key}={value}")

def now():
    """Get current timestamp."""
    from datetime import datetime
    return datetime.now().ctime()

def get_terminal_width():
    """Get terminal width with fallbacks."""
    width = 111  # Default width
    
    try:
        import shutil
        width = shutil.get_terminal_size()[0]
    except ImportError:
        try:
            import cmdw
            width = cmdw.getWidth()
        except ImportError:
            try:
                width = os.get_terminal_size().columns
            except OSError:
                pass  # Use default width
    
    return width

def get_source(source, real_linenumbers=False, copy_to_clipboard=False, no_lines=False):
    """Display source code with syntax highlighting."""
    import inspect
    rich_setup()
    if sys.version_info.major == 3:
        if not rich_available():
            print("Rich library not available. Install with: pip install rich")
            try:
                print(inspect.getsource(source))
            except OSError as e:
                print(f"Error: Could not retrieve source code. {e}")
            return
        
        try:
            # ⭐ FIX: use real line numbers
            # real line numbers support (works on old rich)
            if real_linenumbers:
                lines, start_line = inspect.getsourcelines(source)
            else:
                lines = inspect.getsource(source).splitlines(True)
                start_line = 1

            # build numbered code manually
            if not no_lines:
                width = len(str(start_line + len(lines) - 1))
                numbered = []

                for i, line in enumerate(lines, start=start_line):
                    numbered.append(f"{str(i).rjust(width)} │ {line}")

                source_code = "".join(numbered)
            else:
                source_code = "".join(lines)

            # get full path
            try:
                file_path = inspect.getsourcefile(source) or inspect.getfile(source)
            except Exception:
                file_path = "Unknown"

            console = Console()  # type: ignore

            console.print(
                f"[#000000 on #FFFF00]FILE:[/] "
                f"[#FFFFFF on #0000FF]{file_path}:{start_line}[/]"
            )

            syntax = Syntax(  # type: ignore
                source_code,
                "python",
                theme='fruity',
                line_numbers=False,   # IMPORTANT
                tab_size=2,
                code_width=get_terminal_width(),
                word_wrap=True
            )

            if copy_to_clipboard:
                import clipboard
                clipboard.copy(source_code)
                print("Source code copied to clipboard")

            console.print(syntax)
            print(f"WIDTH: {get_terminal_width()}")

        except OSError as e:
            print(f"Error: Could not retrieve source code. {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    else:
        try:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__module__, source.__module__, get_terminal_width())
            os.system(cmd)
        except:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__name__, source.__name__, get_terminal_width())
            os.system(cmd)

def get_class_name(item):
    """
    Return class name for all object types with proper error handling
    """
    try:
        # Handle class
        if hasattr(item, '__name__') and not hasattr(item, '__self__'):
            # Check if it's a class or function
            if hasattr(item, '__bases__'):
                return item.__name__  # It's a class
            elif hasattr(item, '__qualname__') and '.' in item.__qualname__:
                # It's a method (bound or unbound)
                return item.__qualname__.split('.')[-2]
            else:
                # It's a regular function
                return 'function'
        
        # Handle instance method (bound method)
        elif hasattr(item, '__self__'):
            return item.__self__.__class__.__name__
        
        # Handle instance
        elif hasattr(item, '__class__'):
            return item.__class__.__name__
        
        else:
            return str(type(item))
            
    except Exception as e:
        # return f"Error: {type(e).__name__}"
        return None

def get_full_method_name(method):
    try:
        # Get the qualname (ex: "Publisher.publish")
        if hasattr(method, '__qualname__'):
            # For methods from classes
            return method.__qualname__
        else:
            # Fallback
            return method.__name__
    except:
        return None

def read_file(file_path: Any, method_or_class: Optional[str] = None) -> Optional[str]:
    """Read and display a Python file with syntax highlighting."""

    rich_setup()
    pyread_setup()

    try:
        from pathlib3 import Path
    except:
        from pathlib import Path

    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: File '{path}' does not exist.")
        return None
    
    if not path.is_file():
        print(f"Error: '{path}' is not a file.")
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not rich_available():
            print("Rich library not available. Displaying plain text:")
            print(content)
            return content
        
        console = Console()  # type: ignore
        
        # Display structure analysis if pyread is available
        if pyread_available():
            try:
                analyzer = CodeAnalyzer()  # type: ignore
                print(f"Path: {path}")
                analyzer.process_file(str(path))
                
                method_name = None

                if method_or_class:
                    class_name = get_class_name(method_or_class)
                    method_name = get_full_method_name(method_or_class)
                    if method_name and method_name == class_name:
                        method_name = None
                    print(f"Class Name: {class_name}")
                    print(f"Method Name: {method_name}") if method_name else None
                    if method_name and '.' in method_name:  # type: ignore
                        class_name, method_name = method_name.split('.', 1)  # type: ignore
                    
                    elements = analyzer.find_code_elements(method_name, class_name)
                    
                    if elements:
                        analyzer.display_multiple_elements(elements, 'fruity')
                    else:
                        if class_name:
                            console.print(f"[red]❌ Method '{method_name}' not found in class '{class_name}'[/]")
                        else:
                            console.print(f"[red]❌ Function/method '{method_name}' not found[/]")
                #     get_source(method_or_class)

                # class_name = get_class_name(method_or_class)
                # print(f"Class Name: {class_name}")
                
                # method_name = get_full_method_name(method_or_class)
                # if method_name and method_name == class_name:
                #     method_name = None
                # # else:
                # print(f"Method Name [1]: {method_name}") if method_name else None
                # if not method_name:
                #     method_name = get_full_method_name(method_or_class)
                # print(f"Method Name [2]: {method_name}") if method_name else None
                # if method_name and '.' in method_name:
                #     class_name, method_name = method_name.split('.', 1)
                #     print(f"Method Name [3]: {method_name}") if method_name else None
                
                analyzer.print_structure(method_name, True)
                if not method_name:
                    get_source(method_or_class)
                print()  # Add spacing
                
            except Exception as e:
                print(f"Warning: Could not analyze file structure: {e}")
                tprint(e, show_emoji=True)  # type: ignore
            return 
        else:
            from warnings import warn
            warn("Pyread library not available. Install with: pip install pyread")
        # Display source code with syntax highlighting
        console.print(f"[bold #00FF88]📄 Complete Source Code:[/] [bold #55FFFF]{path}[/]\n")
        syntax = Syntax(  # type: ignore
            content, 
            "python", 
            theme='fruity', 
            line_numbers=True, 
            tab_size=2, 
            code_width=get_terminal_width(), 
            word_wrap=True
        )
        console.print(syntax)
        
        # return content
        
    except UnicodeDecodeError:
        print(f"Error: Could not decode file '{path}'. Check file encoding.")
        return None
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        return None

def read_module_or_file(path: Any) -> Optional[str]:
    """
    Read either a file path or import a module and display its source.
    
    Args:
        path: File path or module name (with dots for submodules)
        
    Returns:
        Content if successful, None otherwise
    """
    
    import inspect
    
    # First try as a file path
    try:
        if os.path.isfile(path):
            return read_file(path)
    except Exception:
        pass
    
    # Try as a module name
    if path in sys.modules:
        get_source(sys.modules[path])
        return None

    try:
        file_path = inspect.getfile(path)
        return read_file(file_path, path)
    except TypeError:
        pass
    except Exception:
        pass
    
    # Try importing as module
    if "." in path:
        try:
            import importlib
            module = importlib.import_module(path)
            get_source(module)
            return None
        except ImportError as e:
            print(f"Error importing module '{path}': {e}")
            return None
    
    # Try as local Python file
    try:
        from pathlib3 import Path
    except:
        from pathlib import Path

    local_file = Path(f"{path}.py")
    if local_file.exists():
        return read_file(local_file)  
    
    print(f"Error: Could not find file or module '{path}'")
    return None

def kill(pid, sig=None):
    """Kill a process by PID with specified signal."""
    import signal
    return kill_process(pid, sig or signal.SIGTERM)

# Regular function versions
def read(path: str) -> Optional[str]:
    """Read and display a file or module with syntax highlighting."""
    return read_module_or_file(path)

def source(*args, **kwargs):
    """Alias for get_source()"""
    return get_source(*args, **kwargs)

def src(*args, **kwargs):
    """Alias for get_source()"""
    return get_source(*args, **kwargs)

# Setup shell functions for standard Python
def setup_shell_functions():
    """Setup shell-like functions for standard Python interpreter."""
    import builtins
    
    def ls(path=None):
        """List directory contents."""
        if path is None:
            path = os.getcwd()
        try:
            return os.listdir(path)
        except OSError as e:
            print(f"Error: {e}")
            return []
    
    def cd(path = None):
        print(f"path: {path}")
        """Change directory."""
        try:
            os.chdir(path or pwd())
            print(f"Changed to: {os.getcwd()}")
        except OSError as e:
            print(f"Error: {e}")
    
    def mkdir(path):
        """Create directory."""
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
        except OSError as e:
            print(f"Error: {e}")
    
    def cls():
        """Clear screen."""
        if sys.platform == 'win32':
            os.system('cls')  # type: ignore
        else:
            os.system('clear')

    def pwd():
        """Print working directory."""
        cwd = os.getcwd()
        print(cwd)
        return cwd
    
    # Add functions to builtins so they're available globally
    # builtins.ls = ls
    builtins.cd = cd  # type: ignore
    # builtins.mkdir = mkdir
    builtins.cls = cls  # type: ignore
    builtins.pwd = pwd  # type: ignore

# IPython Magic Commands Setup
def setup_ipython_magic():
    """Setup IPython magic commands for easy usage."""
    try:
        from IPython import get_ipython
        from IPython.core.magic import Magics, line_magic, magics_class
        from IPython.core.magic_arguments import magic_arguments, parse_argstring, argument
        
        ip = get_ipython()
        if ip is None:
            return False
        
        @magics_class
        class CodeToolsMagics(Magics):
            
            @line_magic
            def read(self, line):
                """Magic command to read files without quotes.
                
                Usage: %read filename.py
                       %read module.submodule
                """
                if not line.strip():
                    print("Usage: %read filename.py or %read module.name")
                    return
                
                return read_module_or_file(line.strip())
            
            @line_magic
            def src(self, line):
                """Magic command to show source code.
                
                Usage: %src function_name
                       %src ClassName
                """
                if not line.strip():
                    print("Usage: %src function_name")
                    return
                
                # Try to get the object from the user namespace
                try:
                    obj = ip.user_ns.get(line.strip())
                    if obj is None:
                        # Try to evaluate it
                        obj = eval(line.strip(), ip.user_ns)
                    
                    if obj is not None:
                        get_source(obj)
                    else:
                        print(f"Object '{line.strip()}' not found")
                except Exception as e:
                    print(f"Error: {e}")
            
            @line_magic
            def source(self, line):
                """Alias for %src"""
                return self.src(line)
            
            @line_magic
            def lls(self, line):
                """List directory contents.
                
                Usage: %ls
                       %ls /path/to/dir
                """
                path = line.strip() if line.strip() else None
                if path is None:
                    path = os.getcwd()
                try:
                    files = os.listdir(path)
                    for f in files:
                        print(f)
                    return files
                except OSError as e:
                    print(f"Error: {e}")
                    return []
            
            @line_magic
            def cd(self, line):
                """Change directory.
                
                Usage: %cd /path/to/directory
                """
                if not line.strip():
                    print("Usage: %cd /path/to/directory")
                    return
                
                try:
                    os.chdir(line.strip())
                    print(f"Changed to: {os.getcwd()}")
                except OSError as e:
                    print(f"Error: {e}")
            
            @line_magic
            def pwd(self, line):
                """Print working directory."""
                cwd = os.getcwd()
                print(cwd)
                return cwd
            
            @line_magic
            def nkdir(self, line):
                """Create directory.
                
                Usage: %mkdir directory_name
                """
                if not line.strip():
                    print("Usage: %mkdir directory_name")
                    return
                
                try:
                    os.makedirs(line.strip(), exist_ok=True)
                    # import clipboard
                    # clipboard.copy(os.path.realpath(line))
                    print(f"Created directory: {line.strip()}")
                except OSError as e:
                    print(f"Error: {e}")
            
            @line_magic
            def cls(self, line):
                """Clear screen."""
                if sys.platform == 'win32':
                    os.system('cls')  # type: ignore
                else:
                    os.system('clear')

            @line_magic
            def kill(self, line, sig=None):
                """Kill a process by PID with specified signal."""
                import signal
                return kill_process(int(line), sig or signal.SIGTERM)

            @line_magic
            def x(self, line):
                exit()

        
        # Register the magic commands
        # ip.register_magic_function(CodeToolsMagics.read, 'line', 'read')
        # ip.register_magic_function(CodeToolsMagics.src, 'line', 'src')
        # ip.register_magic_function(CodeToolsMagics.source, 'line', 'source')
        # ip.register_magic_function(CodeToolsMagics.ls, 'line', 'ls')
        # ip.register_magic_function(CodeToolsMagics.cd, 'line', 'cd')
        # ip.register_magic_function(CodeToolsMagics.pwd, 'line', 'pwd')
        # ip.register_magic_function(CodeToolsMagics.mkdir, 'line', 'mkdir')
        # ip.register_magic_function(CodeToolsMagics.cls, 'line', 'cls')
        # ip.register_magic_function(CodeToolsMagics.kill, 'line', 'kill')
        ip.register_magics(CodeToolsMagics(ip))
        return True
        
    except ImportError:
        return False

def detect_environment():
    """Detect if running in IPython or standard Python."""
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            print("Running in IPython environment")
            return True
        else:
            print("Running in standard Python interpreter")
            return False
    except ImportError:
        print("Running in standard Python interpreter")
        return False

# Initialize the environment
def initialize():
    """Initialize the environment based on the Python interpreter."""
    print("Python Environment Tool Initialized")
    print("=" * 50)
    
    # rich_setup()
    # pyread_setup()

    # Detect environment
    is_ipython = detect_environment()
    
    if is_ipython:
        # Setup IPython magic commands
        if setup_ipython_magic():
            print("✅ IPython magic commands registered!")
            print("\nAvailable magic commands:")
            print("  %read test3.py        # Read file without quotes")
            print("  %src function_name    # Show source code")
            print("  %source class_name    # Show source code")
            print("  %ls                   # List directory")
            print("  %cd /path             # Change directory")
            print("  %pwd                  # Print working directory")
            print("  %mkdir dirname        # Create directory")
            print("  %cls                  # Clear screen")
            print("  %kill pid             # kill by pid")
            print("\nYou can now use: %read test3.py")
        else:
            print("❌ Failed to setup IPython magic commands")
    else:
        # Setup regular functions for standard Python
        setup_shell_functions()
        print("✅ Shell functions available globally")
    
    # print(f"\nRich syntax highlighting: {'Available' if rich_available() else 'Not available'}")
    # print(f"Code analysis: {'Available' if pyread_available() else 'Not available'}")
    print(f"Terminal width: {get_terminal_width()}")
    
# Run initialization
# if __name__ == "__main__":
#     initialize()
# else:
    # Auto-initialize when imported
initialize()