from bytencrypt.downloader import Downloader
from bytencrypt.vault import Vault

d = Downloader(out="papers", pw=Vault(env="prod").get("DOWNLOAD_PW"))
d.get("magnet:?xt=...")
