import getpass
import os
import tempfile

from encryption import FileCrypt
from torrent import Torrent


class Downloader:
    def __init__(self, out="downloads", pw=None, stage=None, remove=True, **settings):
        self.out, self.remove = out, remove
        self.stage = stage or os.path.join(
            "/dev/shm" if os.path.isdir("/dev/shm") else tempfile.gettempdir(),
            str(os.getuid()),
        )
        os.makedirs(self.stage, 0o700, exist_ok=True)
        self.fc = FileCrypt(pw or getpass.getpass("password: "))
        self.torrent = Torrent(self.stage, **settings)

    def get(self, *srcs):
        handles = [self.torrent.add(s) for s in srcs]
        done = []
        for h in handles:
            self.torrent.wait(h)
            for f in self.torrent.files(h):
                dst = os.path.join(self.out, os.path.relpath(f, self.stage)) + ".enc"
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                done.append(self.fc.encrypt(f, out=dst, remove=self.remove))
        return done
