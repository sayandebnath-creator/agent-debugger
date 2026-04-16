import threading  # safer timeout mechanism

def run_code(code: str):
    result = {"success": False, "error": None}

    # basic sandbox safety filter
    banned = ["import os", "import sys", "subprocess", "open("]
    for b in banned:
        if b in code:
            return False, "Unsafe code detected"

    def target():
        try:
            exec_globals = {}  # isolated execution scope
            exec(code, exec_globals)
            result["success"] = True
        except Exception as e:
            result["error"] = str(e)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout=2)  # 2-second timeout

    if thread.is_alive():
        return False, "Timeout"

    return result["success"], result["error"]