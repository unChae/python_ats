#로그 파일을 만들어보자 상원쿤!
import logging
import logging.handlers
import os
import datetime

now = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)
formatter = logging.Formatter(now+' [ %(levelname)s ] [ %(filename)s:%(lineno)s ] >> %(message)s')



# debug    : 잡내용 code 1
# critical : 에러   code 2 
streamHandler = logging.StreamHandler()
fileHandler_debug = logging.FileHandler('./logs/debug.log')
fileHandler_error = logging.FileHandler('./logs/error.log')

streamHandler.setFormatter(formatter)
fileHandler_debug.setFormatter(formatter)
fileHandler_error.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.setLevel(level=logging.DEBUG)


def createLogs(code, msg):
    if(code == 1):
        logger.addHandler(fileHandler_debug)
        logger.debug(msg)
    else:
        logger.addHandler(fileHandler_error)
        logger.critical(msg)
    