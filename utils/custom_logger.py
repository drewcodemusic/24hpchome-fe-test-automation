import logging
import os
from datetime import datetime

class LoggerManager:
    """
    Custom logging utility with multiple output options
    """
    @staticmethod
    def get_logger(name='fe_automation', 
                   log_level=logging.INFO, 
                   log_to_console=True, 
                   log_to_file=True):
        """
        Create a configured logger
        
        :param name: Logger name
        :param log_level: Logging level
        :param log_to_console: Enable console logging
        :param log_to_file: Enable file logging
        :return: Configured logger
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File Handler
        if log_to_file:
            # Create logs directory if not exists
            logs_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            
            # Generate unique log filename
            log_filename = os.path.join(
                logs_dir, 
                f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            )
            
            file_handler = logging.FileHandler(log_filename)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger