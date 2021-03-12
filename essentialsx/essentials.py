import logging
import json

from typing import Callable

import keyboard

from rich.logging import RichHandler
from rich.traceback import install


class Essentials:

    def __init__(self):
        self._hotkeys_enabled = False
        self._logfile = None
        self._logfile_handler = None
        self._logconsole_handler = None
        self._previous_log_level = logging.INFO

        self.get_logger(name='essentialsx')

        self._hotkeys = {
            'ctrl+alt+d': (self._toggle_debug_logging, None, {}),
            'ctrl+alt+l': (self._display_hotkeys, None, {})
        }
        self._registered_hotkeys = {}

        # Install traceback rendering
        install()

    def get_logger(self, name: str=None, logfile: str=None, loglevel: str=None):
        """Return a logger with the specified name and logfile, creating it if necessary.

        This logger is configured with "%(message)s" format and a "[%X]" date format.
        A `rich.logging.RichHandler` is registered as a handler with rich tracebacks enabled.

        - If no name is specified, return the root logger.
        - If no logfile is specified, do not log to file.
        - If no loglevel is specified, use INFO.

        Args:
            name (str, optional): Logging name to use. Defaults to None.
            logfile (str, optional): Logfile path for file handler. Defaults to None.
            loglevel (str, optional): Loglevel (DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to None.
        """
        formatter = logging.Formatter(fmt='%(message)s', datefmt='[%m-%d-%y %X]')

        self.logger = logging.getLogger(name=name)

        if not logging.getLogger(name=name).hasHandlers():
            self._logconsole_handler = RichHandler(rich_tracebacks=True)
            self._logconsole_handler.setFormatter(formatter)
            self.logger.addHandler(self._logconsole_handler)


        if logfile:
            if self._logfile and logfile != self._logfile:
                self.logger.removeHandler(self._logfile_handler)
                self._logfile_handler = None
                self._logfile = None

            if not self._logfile:
                self._logfile = logfile
                self._logfile_handler = logging.FileHandler(
                    self._logfile,
                    mode="w",
                    encoding=None,
                    delay=False
                )
                self._logfile_handler.setFormatter(formatter)
                self.logger.addHandler(self._logfile_handler)

        self.logger.setLevel(logging.INFO if not loglevel else loglevel)

        return self.logger

    def register_hotkey(self, hotkey: str, func: Callable, args: tuple=None, **kwargs):
        """Registers a hotkey to be used with the hotkey listener.

        This function is a wrapper for the `keyboad.add_hotkey()` function, any kwargs used in `keyboard.add_hotkey()`
        can also be passed through this function. Hotkey will not be available until `Essentials.enable_hotkeys()` is called.

        Args:
            hotkey (str): Key
            func (Callable): [description]
            args (tuple, optional): Optional list of arguments to pass to the callback during each invocation. Defaults to None.
            suppress (bool, optional): If true, successful triggers should block the keys from being sent to other programs. Defaults to False.
            timeout (int, optional): Amount of seconds allowed to pass between key presses. Defaults to 1.
            trigger_on_release (bool, optional): if true, the callback is invoked on key release instead of key press. Defaults to False.

        Example:
        ```
            def foo(bar=None):
                print(bar)

            register_hotkey('ctrl+alt+f', foo)
            >> None

            register_hotkey('ctrl+alt+f', foo, args=('bar',))
            >> bar
        ```
        """
        args = (args,) if not isinstance(args, tuple) else args
        kwargs = kwargs.get('kwargs', {})

        if hotkey in self._hotkeys:
            self.logger.warning('Replacing hotkey "%s"', hotkey)
        self._hotkeys[hotkey] = (func, args, kwargs)

        self.logger.info('Registered hotkey "%s" with function "%s"', hotkey, func.__name__)

    def enable_hotkeys(self):
        """Enables all registered hotkeys
        """
        if self._hotkeys_enabled:
            self.logger.error('Hotkeys already enabled.')
            return

        self.logger.info('Enabling hotkey listener')
        for k, v in self._hotkeys.items():
            func, args, kwargs = v
            self.logger.debug('Adding hotkey "%s" with function "%s" (args="%s", kwargs="%s")', k, func.__name__, args, kwargs)
            keyboard.add_hotkey(k, func, args=args, **kwargs)

        self._hotkeys_enabled = True

    def disable_hotkeys(self):
        """Disables all enabled hotkeys
        """
        self.logger.info('Disabling all hotkeys')
        keyboard.unhook_all_hotkeys()
        self._hotkeys_enabled = False

    def get_hotkeys(self):
        """Get a dictionary of all registered hotkeys

        Returns:
            dict: key value pairs of all registerd hotkeys

                {
                    'hotkey1': function,
                    'hotkey2': function
                }
        """
        hotkeys = {}
        for key, value in self._hotkeys.items():
            hotkeys[key] = value.__name__

        return hotkeys

    def _toggle_debug_logging(self):
        self.logger.info('Toggling debug logging')
        if self.logger.level != logging.DEBUG:
            self._previous_log_level = self.logger.level
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel(self._previous_log_level)

    def _display_hotkeys(self):
        for k, v in self._hotkeys.items():
            func, args, kwargs = v
            self.logger.info('Hotkey "%s" is registered with function "%s" (args="%s", kwargs="%s")', k, func.__name__, args, kwargs)
