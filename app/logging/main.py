import threading
from datetime import datetime
from queue import Queue
from threading import Thread
from time import sleep

from app.logging.model.log_model import LogModel
from app.market_trading.api import get_trading


class LogSender:
    stop_thread: bool
    log_queue: Queue[list[int, int, int, str]]
    Thread: Thread

    def __init__(self):
        self.log_queue = Queue()
        self.Thread = threading.Thread(target=self.inserting_log, args=(lambda: self.stop_thread,))
        self.stop_thread = False
        self.run_thread()

    def run_thread(self) -> None:
        self.Thread.start()

    def inserting_log(self, stop_thread) -> None:
        sleep(1)
        while True:
            try:
                user_id, trading_id, title, text = self.log_queue.get(timeout=1)

                temp = LogModel()
                trading = get_trading(trading_id)
                temp.user_id = user_id
                temp.trading_id = trading.id
                temp.title = title
                temp.text = text
                temp.insert()
                self.log_queue.task_done()
            except:
                if stop_thread():
                    break
            sleep(1)

    def restart_thread(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.Thread = threading.Thread(target=self.inserting_log, args=(lambda: self.stop_thread,))
            self.Thread.start()

    def stop_func(self) -> None:
        self.stop_thread = True
        self.Thread.join()

    def start_func(self) -> None:
        self.stop_thread = False
        self.restart_thread()

    def check(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.restart_thread()


log_sender = LogSender()