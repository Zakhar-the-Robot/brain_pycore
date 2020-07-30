import pprint
import logging
import time
import os

CONFIG_LOG_FORMAT = "%(relativeCreated)8d [%(levelname).1s] %(name)-s:  %(message)s"
CONFIG_DONT_PRINT_TO_FILES = True

pp = pprint.PrettyPrinter(indent=4, width=60, depth=30)

def get_logger(name, log_level = logging.INFO):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logger = logging.getLogger(name=name)
    formatter = logging.Formatter(CONFIG_LOG_FORMAT)
    # stream
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if not CONFIG_DONT_PRINT_TO_FILES:
        # file
        handler = logging.FileHandler("logs/" + name + '.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        #union file
        handler = logging.FileHandler("logs/" + 'zk.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(log_level)
    return logger


def strf(s):
    return pp.pformat(s)

def list2strf(l, cell_size, in_hex = False):
    s = "[ "
    cell = ""
    for i in l:
        if in_hex:
            cell = hex(i)[2:]
        else:
            cell = str(i)
        c_l = len(cell)
        if c_l > cell_size:
            cell = cell[:cell_size-1] + "?"
        if c_l < cell_size:
            cell = " " * (cell_size - c_l) + cell
        s = s + cell + " "
    s = s + "]"
    return s

if __name__ == "__main__":
    d = {'a': 12, 'b': 32, 'hello': "there", "aa": "test"}
    lt = [0, 0, 0, 0, 0, 0, 0, 253, 253, 253, 252, 251, 253, 8240, 65280, 65280, 65280, 65280, 65280, 65280]
    print(list2strf(lt,4))

    # pp.pprint(lt)
    # pp.pprint("hello!")
    # l = get_logger("Logger")
    # l.debug("dict : %s" % strf(1223))
    # time.sleep(2)
    # l.info("test2")
