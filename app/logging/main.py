from queue import Queue
from threading import Thread
from time import sleep

from app.logging.model.log_model import LogModel


class LogSender:
    stop_thread: bool
    log_queue: Queue[list[int, int, int, str]]
    thread: Thread

    def __init__(self):
        self.log_queue = Queue()
        self.thread = Thread(target=self.inserting_log, args=(lambda: self.stop_thread,))
        self.stop_thread = False
        self.run_thread()

    def run_thread(self) -> None:
        self.thread.start()

    def inserting_log(self, stop_thread) -> None:
        sleep(1)
        while True:
            try:
                user_id, trading_id, title, text = self.log_queue.get(timeout=1)
                try:
                    temp = LogModel()
                    temp.user_id = user_id
                    temp.trading_id = trading_id
                    temp.title = title
                    temp.text = text
                    temp.insert()
                except Exception as e:
                    print("log model : ", e)
                self.log_queue.task_done()
            except:
                if stop_thread():
                    break
            sleep(1)

    def restart_thread(self) -> None:
        if not (self.thread.is_alive()):
            self.stop_thread = False
            self.thread = Thread(target=self.inserting_log, args=(lambda: self.stop_thread,))
            self.thread.start()

    def stop_func(self) -> None:
        self.stop_thread = True
        self.thread.join()

    def start_func(self) -> None:
        self.stop_thread = False
        self.restart_thread()

    def check(self) -> None:
        if not (self.thread.is_alive()):
            self.stop_thread = False
            self.restart_thread()


log_sender = LogSender()
