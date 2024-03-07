import logging

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'logs/app.log',
            'mode': 'a',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
    },
    'loggers': {
        'src.app': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'werkzeug': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'src.services': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'src.tasks': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    }
}

# from logging.config import dictConfig
# # Apply the configuration
# dictConfig(LOGGING_CONFIG)

# # Example usage
# logger1 = logging.getLogger('src.services.task_scheduler')

# logger1.info("asdfsf.")
