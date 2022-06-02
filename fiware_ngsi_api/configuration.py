from pathlib import Path

import configparser
import logging


class NgsiConfiguration:
    DEFAULT_HOST = "https://tektrain-cloud.ddns.net"
    DEFAULT_USERNAME = ""
    DEFAULT_PASSWORD = ""

    def __init__(self, file_path=None, section=None):
        self._file_path = None
        if file_path is not None:
            self._file_path = file_path

        self._conf_section = None
        if section is not None:
            self._conf_section = section

        self._logger = logging.getLogger(__name__)

        self._host = NgsiConfiguration.DEFAULT_HOST
        self._username = NgsiConfiguration.DEFAULT_USERNAME
        self._password = NgsiConfiguration.DEFAULT_PASSWORD

        self._api_key = {}
        self._api_key_prefix = {}
        self._refresh_api_key_hook = {}

        self._load_configuration()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, new_host):
        self._host = new_host

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    def _load_configuration(self):
        try:
            path = Path(self._file_path)

            if path.is_file():
                config = configparser.ConfigParser()
                config.read(self._file_path)

                if self._conf_section is None:
                    self._conf_section = 'DEFAULT'

                try:
                    self.host = config[self._conf_section]['Host']
                except KeyError as e:
                    self._logger.warning(
                        f'Configuration file does not contain key: {e}')

                try:
                    self.username = config[self._conf_section]['Username']
                except KeyError as e:
                    self._logger.warning(
                        f'Configuration file does not contain key: {e}')

                try:
                    self.password = config[self._conf_section]['Password']
                except KeyError as e:
                    self._logger.warning(
                        f'Configuration file does not contain key: {e}')
            else:
                self._logger.warning(
                    f"Configaration file path [{self._file_path}] is invalid!")
        except Exception as e:
            self._logger.warning(
                f'Error occured while parsing configuration file: {e}')

    def __str__(self):
        return f"Configuration: host=[{self.host}], username=[{self.username}], password=[{self.password}]"


if __name__ == "__main__":
    conf = NgsiConfiguration("settings.conf")
    print(conf)
