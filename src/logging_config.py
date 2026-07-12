import logging
import sys


def setup_logging(
    level: str = "INFO",
) -> None:  # show all logs: INFO, WARNING, ERROR, CRITICAL
    """Setup global config"""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",  # define how log shows
        handlers=[  # where to send logs?
            logging.StreamHandler(sys.stdout)  # sys.stdout - standard output (console)
        ],
        force=True,  # overwrite configuration
    )


# Source - https://stackoverflow.com/a/41304693
# Posted by theotheo, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-08, License - CC BY-SA 4.0

# import logging.config
#
# DEFAULT_LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'loggers': {
#         '': {
#             'level': 'INFO',
#         },
#         'another.module': {
#             'level': 'DEBUG',
#         },
#     }
# }
#
# logging.config.dictConfig(DEFAULT_LOGGING)
#
# logging.info('Hello, log')
