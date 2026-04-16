import signal  # used for timeout control

class TimeoutException(Exception):
    pass


def _handler(signum, frame):
    raise TimeoutException()

signal.signal(signal.SIGALRM, _handler)  # register timeout handler


def run_code(code: str):
    signal.alarm(2)  # enforce 2-second execution timeout

    # basic sandbox safety filter
    banned = ["import os", "import sys", "subprocess", "open("]
    for b in banned:
        if b in code:
            signal.alarm(0)
            return False, "Unsafe code detected"

    try:
        exec_globals = {}  # isolated execution scope
        exec(code, exec_globals)
        signal.alarm(0)
        return True, None
    except TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)