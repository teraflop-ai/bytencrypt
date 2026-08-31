from downloader import Downloader
from vault import Vault

d = Downloader(out="papers", pw=Vault(env="prod").get("DOWNLOAD_PW"))
d.get("magnet:?xt=...")
