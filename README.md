# Python Essentials
![PyPI](https://img.shields.io/pypi/v/essentialsx)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/essentialsx)

* Easily create a logger enhanced with [rich logging handler](https://rich.readthedocs.io/en/stable/logging.html)
* Traceback formatting that you can easily following via [rich Traceback](https://rich.readthedocs.io/en/stable/traceback.html)
* Non-blocking hotkey monitoring via [keyboard](https://pypi.org/project/keyboard/) (e.g. enable debug logging on the fly)

## Example Usage

### Installing
`essentialsx` is registered on pypi and can be installed via pip
```bash
pip install essentialsx
```

### Basic Setup
```python
from essentialsx import Essentials

essentials = Essentials()
```

### Logging
A simple wrapper for creating a logger (uses built-in `logging` module) was created which also adds in the [rich logging handler](https://rich.readthedocs.io/en/stable/logging.html) for a beautiful logging experience. A couple optional parameters exist for this wrapper:

| Parameter | Functionality  |
| --- | --- |
| name | The name space to use for the logger. Uses root by default. |
| logfile | Creates a file handler at this path and logs entries to this file in addition to the console handler. |
| loglevel | The loglevel to be used (INFO, DEBUG, WARNING, ERROR, CRITICAL). Uses INFO by default. |


```python
# Create a basic logger with console handler
log = essentials.get_logger()
log.info('Logging to console works!')

# Create a logger with log file handler
log = essentials.get_logger(logfile='/tmp/logfile.log')
log.info('Logging to console and file works!')
```

### Hotkeys
There are a few wrapper functions for the [keyboard](https://pypi.org/project/keyboard/) hotkey functions, this is to help keep track of hotkeys in use which gives us the opportunity to provide some predefined hotkeys. Hotkeys will need to be registered via the `register_hotkey()` function and will not be active (including the predefined hotkeys) until the `enable_hotkeys()` function is called. To disable hotkeys once they have been enabled, simply call the `disable_hotkeys()` function.

#### Predefined Hotkeys
| Hotkey | Functionality  |
| --- | --- |
| `ctrl+alt+d` | Toggles debug log level |
| `ctrl+alt+l` | Lists all registered hotkeys |

#### Registering Hotkeys
```python
# Register a function with no arguments
def foo():
    print('bar')

essentials.register_hotkey('ctrl+f', foo)
>> bar

# Register a function with arguments
def bar(baz):
    print(baz)

essentials.register_hotkey('ctrl+b', bar, args=('baz',))
>> baz
```
> Note: Registered hotkeys aren't active until `enable_hotkeys()` is called.

#### Enabling / Disabling Hotkeys
```python
# Enable all registered hotkeys
essentials.enable_hotkeys()

# Disable all enabled hotkeys
essentials.disable_hotkeys()
```
