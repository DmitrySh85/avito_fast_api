import os
import logging
from logging.handlers import RotatingFileHandler

logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(logs_dir, 'program.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(os.path.join(logs_dir, 'fast_api_log.log'), maxBytes=50000000, backupCount=5)
logger.addHandler(handler)