#!/usr/bin/env python
#author: Hadi Cahyadi
#email: cumulus13@gmail.com
#license: MIT

from __future__ import print_function
import rlcompleter
import readline
import os
import sys
import inspect
import signal
import importlib
from pathlib import Path
from typing import Union, Optional, Any

# Configure environment
readline.parse_and_bind('tab:complete')
os.environ.update({'PYTHONIOENCODING': 'UTF-8'})
if not sys.platform == 'win32':
    os.environ.update({"XDG_SESSION_TYPE": "wayland"})

# Check for optional dependencies
try:
    from rich.console import Console
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from pyread import CodeAnalyzer
    PYREAD_AVAILABLE = True
except ImportError:
    PYREAD_AVAILABLE = False


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

def set_debug(debug=None, host=None, traceback_debugger_server=None, reset=False):
    """Alias for setdebug()."""
    setdebug(debug, host, traceback_debugger_server, reset)

def kill_process(pid, sig=signal.SIGTERM):
    """Kill a process by PID."""
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

def get_source(source):
    """Display source code with syntax highlighting."""
    if sys.version_info.major == 3:
        if not RICH_AVAILABLE:
            print("Rich library not available. Install with: pip install rich")
            try:
                print(inspect.getsource(source))
            except OSError as e:
                print(f"Error: Could not retrieve source code. {e}")
            return
        
        try:
            source_code = inspect.getsource(source)
            console = Console()
            syntax = Syntax(
                source_code, 
                "python", 
                theme='fruity', 
                line_numbers=True, 
                tab_size=2, 
                code_width=get_terminal_width(), 
                word_wrap=True
            )
            console.print(syntax)
            print(f"WIDTH: {get_terminal_width()}")
            
        except OSError as e:
            print(f"Error: Could not retrieve source code. {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    else:
        try:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__module__, source.__module__, get_width())
            os.system(cmd)
        except:
            cmd = """python3 -c \"import {};import inspect;from rich.console import Console;from rich.syntax import Syntax;console = Console();console.print(Syntax(inspect.getsource({}), 'python', theme = 'fruity', line_numbers=True, tab_size=2, code_width={}))\"""".format(source.__name__, source.__name__, get_width())
            os.system(cmd)


def read_file(file_path: Union[str, Path]) -> Optional[str]:
    """Read and display a Python file with syntax highlighting."""
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
        
        if not RICH_AVAILABLE:
            print("Rich library not available. Displaying plain text:")
            print(content)
            return content
        
        console = Console()
        
        # Display structure analysis if pyread is available
        if PYREAD_AVAILABLE:
            try:
                analyzer = CodeAnalyzer()
                analyzer.process_file(str(path))
                analyzer.print_structure()
                print()  # Add spacing
            except Exception as e:
                print(f"Warning: Could not analyze file structure: {e}")
        else:
            warning
        # Display source code with syntax highlighting
        console.print(f"[bold #00FF88]📄 Complete Source Code:[/] [bold #55FFFF]{path}[/]\n")
        syntax = Syntax(
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


def read_module_or_file(path: str) -> Optional[str]:
    """
    Read either a file path or import a module and display its source.
    
    Args:
        path: File path or module name (with dots for submodules)
        
    Returns:
        Content if successful, None otherwise
    """
    # First try as a file path
    if os.path.isfile(path):
        return read_file(path)
    
    # Try as a module name
    if path in sys.modules:
        get_source(sys.modules[path])
        return None
    
    # Try importing as module
    if "." in path:
        try:
            module = importlib.import_module(path)
            get_source(module)
            return None
        except ImportError as e:
            print(f"Error importing module '{path}': {e}")
            return None
    
    # Try as local Python file
    local_file = Path(f"{path}.py")
    if local_file.exists():
        return read_file(local_file)
    
    print(f"Error: Could not find file or module '{path}'")
    return None


def kill(pid, sig=signal.SIGTERM):
    """Kill a process by PID with specified signal."""
    return kill_process(pid, sig)

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
            os.system('cls')
        else:
            os.system('clear')
    
    def pwd():
        """Print working directory."""
        cwd = os.getcwd()
        print(cwd)
        return cwd
    
    # Add functions to builtins so they're available globally
    # builtins.ls = ls
    builtins.cd = cd
    # builtins.mkdir = mkdir
    builtins.cls = cls
    builtins.pwd = pwd


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
                    clipboard.copy(os.path.realpath(line))
                    print(f"Created directory: {line.strip()}")
                except OSError as e:
                    print(f"Error: {e}")
            
            @line_magic
            def cls(self, line):
                """Clear screen."""
                if sys.platform == 'win32':
                    os.system('cls')
                else:
                    os.system('clear')

            @line_magic
            def kill(self, line, sig=signal.SIGTERM):
                """Kill a process by PID with specified signal."""
                return kill_process(int(line), sig)

        
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
    
    print(f"\nRich syntax highlighting: {'Available' if RICH_AVAILABLE else 'Not available'}")
    print(f"Code analysis: {'Available' if PYREAD_AVAILABLE else 'Not available'}")
    print(f"Terminal width: {get_terminal_width()}")


# Run initialization
if __name__ == "__main__":
    initialize()
else:
    # Auto-initialize when imported
    initialize()