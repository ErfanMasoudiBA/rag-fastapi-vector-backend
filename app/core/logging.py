import logging
import sys

def setup_logging():
    # it is setup the basic log configs
    logging.basicConfig(
        # INFO, WARNING, ERROR, CRITICAL
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)], # This said where the logs go
    )