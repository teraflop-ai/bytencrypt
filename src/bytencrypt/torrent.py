import os
import time

import libtorrent as lt
from tqdm import tqdm


class Torrent:
    SETTINGS = {
        "listen_interfaces": "0.0.0.0:6881",
        "out_enc_policy": lt.enc_policy.forced,
        "in_enc_policy": lt.enc_policy.forced,
        "allowed_enc_level": lt.enc_level.rc4,
    }

    def __init__(self, save="downloads", **settings):
        self.save = save
        os.makedirs(save, exist_ok=True)
        self.ses = lt.session({**self.SETTINGS, **settings})

    def add(self, src):
        if src.startswith("magnet:"):
            p = lt.parse_magnet_uri(src)
        else:
            p = lt.add_torrent_params()
            p.ti = lt.torrent_info(src)
        p.save_path = self.save
        return self.ses.add_torrent(p)

    @staticmethod
    def wait(h, interval=1):
        s = h.status()
        with tqdm(total=s.total_wanted, unit="B", unit_scale=True, desc=s.name) as bar:
            while not s.is_seeding:
                time.sleep(interval)
                s = h.status()
                bar.total = s.total_wanted
                bar.update(s.total_wanted_done - bar.n)
                bar.set_postfix(peers=s.num_peers, refresh=False)

    def files(self, h):
        fs = h.torrent_file().files()
        paths = (
            os.path.join(self.save, fs.file_path(i)) for i in range(fs.num_files())
        )
        return [p for p in paths if os.path.isfile(p)]

    def download(self, src):
        h = self.add(src)
        self.wait(h)
        return self.files(h)
