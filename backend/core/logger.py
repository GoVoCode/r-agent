import logging
import sys
from pathlib import Path
from datetime import datetime


class LoggerFactory:
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = cls._create_logger(name)
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def _create_logger(cls, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        log_dir = Path("logs/backend")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger


def get_logger(name: str) -> logging.Logger:
    return LoggerFactory.get_logger(name)

