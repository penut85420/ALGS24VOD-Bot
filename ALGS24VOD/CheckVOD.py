import os

import psutil


class CheckVOD:
    def __init__(self):
        self.process = self.locate()
        self.refresh()

    def locate(self, name="potplayer"):
        pid = None

        for proc in psutil.process_iter():
            if name in proc.name().lower():
                pid = proc.pid

        if pid is None:
            return None

        return psutil.Process(pid)

    def refresh(self):
        self.file_list = set()

        if self.process is None:
            return

        for item in self.process.open_files():
            path = os.path.realpath(item.path)
            self.file_list.add(path)

    def check(self, fpath):
        fpath = os.path.realpath(fpath)
        if fpath in self.file_list:
            return True
        return False

    def check_dir(self, target_dir_path):
        for dir_path, _, file_list in os.walk(target_dir_path):
            for file_name in file_list:
                full_path = os.path.join(dir_path, file_name)
                if self.check(full_path):
                    fn, _ = os.path.splitext(file_name)
                    return fn
        return "Not Playing"
