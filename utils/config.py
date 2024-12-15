import os
import configparser
import logging
from pathlib import Path

class ConfigManager:
    """
    Manages configuration settings for the test framework
    Supports reading from .ini or .env files
    """
    def __init__(self, config_path=None):
        self.config = configparser.ConfigParser()
        
        # Default config paths
        default_paths = [
            Path.home() / '.fe_automation_config.ini',
            Path(os.getcwd()) / 'config.ini'
        ]
        
        # Use provided path or find first existing default path
        if config_path:
            default_paths.insert(0, Path(config_path))
        
        # Load first existing config file
        self._load_config(default_paths)

    def _load_config(self, paths):
        """
        Load configuration from first existing path
        """
        for path in paths:
            if os.path.exists(path):
                self.config.read(path)
                return
        
        # Create default config if no file found
        self._create_default_config()

    def _create_default_config(self):
        """
        Create a default configuration
        """
        self.config['DEFAULT'] = {
            'browser': 'chrome',
            'timeout': '10',
            'screenshot_path': './screenshots',
            'log_level': 'INFO'
        }
        
        self.config['ENVIRONMENTS'] = {
            'prod_url': 'https://24h.pchome.com.tw/',
            'staging_url': 'https://staging.pchome.com.tw/',
        }

    def get(self, section, key, fallback=None):
        """
        Get configuration value
        """
        return self.config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=None):
        """
        Get integer configuration value
        """
        return self.config.getint(section, key, fallback=fallback)