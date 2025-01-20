import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.run_command()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.restart_command()

    def run_command(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

    def restart_command(self):
        print("File changed, restarting...")
        self.run_command()

if __name__ == "__main__":
    path = "./phonenumberextractor"
    command = "poetry run python phonenumberextractor/main.py"
    event_handler = Watcher(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching for changes in {path}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# poetry run python watch_and_run.py