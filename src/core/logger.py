import logging

logging.getLogger("requests").setLevel(logging.ERROR)
log = logging
log.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s \t: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')