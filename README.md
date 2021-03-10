# Python Essentials

This project has reusable essentials for python projects, such as:

* Logger (enhanced with rich logging)
* Hotkey monitoring (e.g. enable debug logging on the fly)

## Example Usage

```python
from essentials import Essentials


def custom_function():
    print('I am using my custom function!')

if __name__ == '__main__':
    essentials = Essentials()

    # Create a logger easily
    log = essentials.get_logger()

    # Or create a logger with a logfile
    log = essentials.get_logger(logfile='/tmp/mylogfile.log')

    # Register custom hotkeys
    essentials.register_hotkeys({'<ctrl>+<alt>+c': custom_function})

    # Get all registered hotkeys
    print(essentials.get_hotkeys())

    # Enable hotkey monitoring
    essentials.enable_hotkeys()

    # Disable hotkey monitoring
    essentials.disable_hotkeys()
```
