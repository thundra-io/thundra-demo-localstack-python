from uuid import uuid4
import time, subprocess

def generate_uuid():
    return str(uuid4())

def generate_short_uuid():
    return generate_uuid()[:8]

def delay(ms):
    time.sleep(ms)

def execute_command(cmd_str, opts={}):
    cmd_list = cmd_str.strip().split(" ")
    res = subprocess.run(cmd_list, capture_output=True, **opts)
    return res

def get_current_time():
    return int(time.time())