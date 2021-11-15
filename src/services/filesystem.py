import os
import shutil
from hashlib import blake2b


class FileSystemUtils:
    def is_file_exist(self, path) -> bool:
        if os.path.isfile(path) or os.path.isdir(path):
            return True
        else:
            return False

    def check_dir(self, dir) -> None:
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def delete_file(self, path) -> None:
        if os.path.isfile(path):
            os.remove(path)

    def remove_directory(self, dir) -> None:
        if os.path.isdir(dir):
            shutil.rmtree(dir)

    def file_hash(self, path, digest_size) -> str:
        if os.path.isfile(path):
            h = blake2b(digest_size=digest_size)
            h.update(open(path, 'rb').read())
            return h.hexdigest()

    def move_file(self, src, dst) -> None:
        shutil.move(src, dst)
