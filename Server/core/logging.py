import logging
from rich.console import Console
from rich.logging import RichHandler


def setup_logger() -> logging.Logger:
    console = Console(color_system="256", width=120)

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
            )
        ],
    )

    logger = logging.getLogger("app")
    return logger


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s | %(name)s | %(message)s",
        },
    },
    "handlers": {
        "rich": {
            "class": "rich.logging.RichHandler",
            "formatter": "default",
            "rich_tracebacks": True,
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["rich"], "level": "INFO"},
        "uvicorn.error": {"handlers": ["rich"], "level": "INFO"},
        "uvicorn.access": {"handlers": ["rich"], "level": "INFO"},
        "app": {"handlers": ["rich"], "level": "INFO"},
    },
}


logger = setup_logger()
