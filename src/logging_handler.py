import logging,tempfile,os
from logging.handlers import TimedRotatingFileHandler

TMP_FOLDER=tempfile.gettempdir()+"/"
LOGS_FOLDER="dange-pdf-logs/"
LOGS_FILENAME="dange-pdf.log"
def create_logging_handler():
    if not os.path.exists(TMP_FOLDER+ LOGS_FOLDER):
        os.makedirs(TMP_FOLDER+ LOGS_FOLDER)

    log = logging.getLogger("DangePDF Log")
    log.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = TimedRotatingFileHandler(TMP_FOLDER +LOGS_FOLDER+LOGS_FILENAME,
                                        when="d",
                                        interval=1,
                                        backupCount=5)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log