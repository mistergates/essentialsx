import logging
import threading

from pynput import keyboard
from rich.logging import RichHandler


class Essentials:

    def __init__(self):
        self.hotkey_thread = None
        self.hotkey_thread_stop_event = None
        self.logfile = None
        self.logfile_handler = None

        self.get_logger()

        self.hotkeys = {
            '<ctrl>+<alt>+d': self._toggle_debug_logging
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
            if self.logfile and logfile != self.logfile:
                self.logger.removeHandler(self.logfile_handler)
                self.logfile_handler = None
                self.logfile = None

            if not self.logfile:
                fh = logging.FileHandler(logfile, mode="w", encoding=None, delay=False)
                self.logger.addHandler(fh)
                self.logfile_handler = fh
                self.logfile = logfile

        return self.logger

    def register_hotkeys(self, hotkeys: dict):
        """Registers hotkeys to be used with the hotkey listener.

        This can only be done before the hotkey listener is enabled.

        Args:
            hotkeys (dict): Hotkeys in a {'hotkey': function} format.
        """
        if self.hotkey_thread:
            self.logger.error('Cannot register hotkeys after hotkeys have been enabled.')
            return

        for key in hotkeys:
            if key in self.hotkeys:
                self.logger.warning('Replacing default hotkey %s', key)
            self.hotkeys[key] = hotkeys[key]
            self.logger.info('Registered hotkey "%s" with function "%s"', key, hotkeys[key].__name__)

    def enable_hotkeys(self):
        """Enables the hotkey listener
        """
        if self.hotkey_thread:
            return

        self.logger.info('Enabling hotkey listener')
        
        self.hotkey_thread_stop_event = threading.Event()
        self.hotkey_thread = threading.Thread(target=self._hotkey_listener, args=(self.hotkeys,), daemon=True)
        self.hotkey_thread.start()

    def disable_hotkeys(self):
        """Disables the hotkey listener
        """
        if not self.hotkey_thread:
            return

        self.logger.info('Disabling hotkey listener')
        self.hotkey_thread_stop_event.set()

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
        for key, value in self.hotkeys.items():
            hotkeys[key] = value.__name__

        return hotkeys

    def _hotkey_listener(self, hotkeys):
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

    def _toggle_debug_logging(self):
        self.logger.info('Toggling debug logging')
        if self.logger.level == logging.INFO:
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel('INFO')
