import subprocess
import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

IGNORED_DIRS = {"__pycache__", ".git", "venv", ".idea", ".vscode"}
RESTART_DELAY = 1.0  # segundos de espera antes de reiniciar

class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = self.start_process()
        self.restart_timer = None

    def start_process(self):
        print("🚀 Iniciando aplicação...")
        return subprocess.Popen([sys.executable] + self.command)

    def stop_process(self):
        if self.process:
            print("🛑 Parando aplicação...")
            self.process.kill()
            self.process.wait()

    def restart_process(self):
        self.stop_process()
        self.process = self.start_process()

    def schedule_restart(self):
        if self.restart_timer:
            self.restart_timer.cancel()
        self.restart_timer = Timer(RESTART_DELAY, self.restart_process)
        self.restart_timer.start()

    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".py"):
            return
        # Ignorar diretórios não relevantes
        if any(ignored in event.src_path for ignored in IGNORED_DIRS):
            return

        print(f"🔁 Alteração detectada em: {event.src_path}")
        self.schedule_restart()

def main():
    path = "."
    command = ["main.py"]

    event_handler = RestartOnChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    print("👀 Monitorando alterações em arquivos .py...")
    try:

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Encerrando monitoramento...")
        observer.stop()
        event_handler.stop_process()
    observer.join()

if __name__ == "__main__":
    main()
