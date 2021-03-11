import logging
import json

from pynput import keyboard
from rich.logging import RichHandler


class Essentials:

    def __init__(self):
        self._hotkey_thread = None
        self._logfile = None
        self._logfile_handler = None
        self._previous_log_level = None

        self.get_logger()

        self._hotkeys = {
            '<ctrl>+<alt>+d': self._toggle_debug_logging,
            '<ctrl>+<alt>+l': self._display_hotkeys
        }

    def get_logger(self, name: str=None, logfile: str=None):
        """Return a logger with the specified name and logfile, creating it if necessary.

        If no name is specified, return the root logger.

        If no logfile is specified, do not log to file.

        Args:
            name (str, optional): Logger name, if not provided use root logger. Defaults to None.
            logfile (str, optional): Logfile path, if not provided do not log to file. Defaults to None.
        """
        if not logging.getLogger(name=name).hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[RichHandler(rich_tracebacks=True)]
            )
            self.logger = logging.getLogger(name=name)

        if logfile:
            if self._logfile and logfile != self._logfile:
                self.logger.removeHandler(self._logfile_handler)
                self._logfile_handler = None
                self._logfile = None

            if not self._logfile:
                fh = logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
                self.logger.addHandler(fh)
                self._logfile_handler = fh
                self._logfile = logfile

        return self.logger

    def register_hotkeys(self, hotkeys: dict):
        """Registers hotkeys to be used with the hotkey listener.

        This can only be done before the hotkey listener is enabled.

        Args:
            hotkeys (dict): Hotkeys in a {'hotkey': function} format.
        """
        if self._hotkey_thread:
            self.logger.error('Cannot register hotkeys after hotkeys have been enabled.')
            return

        for key in hotkeys:
            if key in self._hotkeys:
                self.logger.warning('Replacing default hotkey %s', key)
            self._hotkeys[key] = hotkeys[key]
            self.logger.info('Registered hotkey "%s" with function "%s"', key, hotkeys[key].__name__)

    def enable_hotkeys(self):
        """Enables the hotkey listener
        """
        if self._hotkey_thread:
            return

        self.logger.info('Enabling hotkey listener')
        self._hotkey_thread = keyboard.GlobalHotKeys(self._hotkeys)
        self._hotkey_thread.start()

    def disable_hotkeys(self):
        """Disables the hotkey listener
        """
        if not self._hotkey_thread:
            return

        self.logger.info('Disabling hotkey listener')
        self._hotkey_thread.stop()
        self._hotkey_thread = None

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
        self.logger.info(json.dumps(self.get_hotkeys(), indent=2))
