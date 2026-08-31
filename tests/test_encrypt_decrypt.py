from encryption import FileCrypt

fc = FileCrypt("password")
fc.encrypt("tests/2505.09388v1.pdf")
fc.decrypt("tests/2505.09388v1.pdf.enc", remove=False)
