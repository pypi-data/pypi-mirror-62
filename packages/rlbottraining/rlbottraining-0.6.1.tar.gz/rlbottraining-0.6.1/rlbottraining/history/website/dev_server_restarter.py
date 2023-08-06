from subprocess import Popen, PIPE, TimeoutExpired
import atexit
import datetime
import psutil
import sys
import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from rlbot.utils.logging_utils import get_logger

from rlbottraining.paths import _website_dev_server, _website_source
from rlbottraining.paths import HistoryPaths


def KILL(process):
    try:
        process.kill()
    except psutil._exceptions.NoSuchProcess as e:
        return
def kill_proc_tree(pid):
    try:
        parent = psutil.Process(pid)
    except psutil._exceptions.NoSuchProcess as e:
        return
    children = parent.children(recursive=True)
    KILL(parent) # THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE
    for child in children: # THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE
        KILL(child)  # THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE THIS CAN NOT CONTINUE
    gone, still_alive = psutil.wait_procs(children, timeout=5)


class CallOnModified(LoggingEventHandler):
    def __init__(self, callback):
        self.last_modified = datetime.datetime.now()
        self.callback = callback
    def on_modified(self, event):
        if '__pycache__' in event.src_path:  return
        # Rate limit
        now = datetime.datetime.now()
        if now - self.last_modified < datetime.timedelta(seconds=0.5):
            return
        self.last_modified = now

        print()
        get_logger('restarter').info('File modified: ' + event.src_path.lstrip('.\\/'))
        sys.stdout.flush()

        self.callback()

    def on_created(self, event):
        pass
    def on_deleted(self, event):
        pass
    def on_moved(self, event):
        pass

def restart_devserver_on_source_change(history_dir, host, port):
    subprocess_command = f'python {_website_dev_server} {history_dir} {host} {port}'

    child_process = None
    def start_dev_server():
        nonlocal child_process
        if child_process:
            kill_proc_tree(child_process.pid)
        child_process = Popen(
            subprocess_command,
            shell=True,
        )
        get_logger('restarter').info('child started')
        atexit.register(lambda: child_process.kill())  # behave like a daemon

    start_dev_server()

    event_handler = CallOnModified(start_dev_server)
    observer = Observer()
    observer.schedule(event_handler, str(_website_source), recursive=True)

    # Also monitor the additional_aggregators_dir.
    symlink_file = history_dir / HistoryPaths.additional_website_code
    if symlink_file.exists():
        additional_aggregators_dir = symlink_file.read_text().strip()
        observer.schedule(event_handler, additional_aggregators_dir, recursive=True)


    observer.start()
    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        get_logger('restarter').info("Shutting down...")
        observer.stop()
    observer.join()
