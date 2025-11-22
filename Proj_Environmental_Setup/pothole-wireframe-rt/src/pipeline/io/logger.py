import logging
import os

class Logger:
    def __init__(self, log_file='pipeline.log'):
        self.logger = logging.getLogger('PotholeDetectionLogger')
        self.logger.setLevel(logging.DEBUG)
        
        # Create a file handler
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Create a logger instance
log_file_path = os.path.join(os.path.dirname(__file__), 'pipeline.log')
logger = Logger(log_file=log_file_path)