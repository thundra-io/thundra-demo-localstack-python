from uuid import uuid4
import time

def generate_uuid():
    return str(uuid4())

def generate_short_uuid():
    return generate_uuid()[:8]

def delay(ms):
    time.sleep(ms)

def execute_command(cmd_str, opts={}):
    exec(cmd_str, opts)

def get_current_time():
    return int(time.time())