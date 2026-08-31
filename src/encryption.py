import os

import nacl.pwhash
import nacl.secret
import nacl.utils


class FileCrypt:
    CHUNK = 1 << 20
    A = nacl.secret.Aead
    KDF = nacl.pwhash.argon2id
    BLOCK = A.NONCE_SIZE + CHUNK + A.MACBYTES

    def __init__(self, pw):
        self.pw = pw.encode() if isinstance(pw, str) else pw

    def _aead(self, salt):
        key = self.KDF.kdf(
            self.A.KEY_SIZE,
            self.pw,
            salt,
            self.KDF.OPSLIMIT_MODERATE,
            self.KDF.MEMLIMIT_MODERATE,
        )
        return self.A(key)

    @staticmethod
    def _aad(i, last):
        return i.to_bytes(8, "big") + bytes([last])

    def encrypt(self, path, out=None, remove=True):
        out = out or path + ".enc"
        salt = nacl.utils.random(self.KDF.SALTBYTES)
        aead = self._aead(salt)
        with open(path, "rb") as f, open(out, "wb") as o:
            o.write(salt)
            i, last = 0, False
            while not last:
                chunk = f.read(self.CHUNK)
                last = len(chunk) < self.CHUNK
                o.write(aead.encrypt(chunk, aad=self._aad(i, last)))
                i += 1
        if remove:
            os.remove(path)
        return out

    def decrypt(self, path, out=None, remove=True):
        out = out or path.removesuffix(".enc")
        with open(path, "rb") as f, open(out, "wb") as o:
            aead = self._aead(f.read(self.KDF.SALTBYTES))
            i, last = 0, False
            while not last:
                block = f.read(self.BLOCK)
                last = len(block) < self.BLOCK
                o.write(aead.decrypt(block, aad=self._aad(i, last)))
                i += 1
        if remove:
            os.remove(path)
        return out
