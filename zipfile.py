import zipfile36

with zipfile36.GzipFile('master2.zip') as Zip:
  for ZipMember in Zip.infolist():
    Zip.extract(ZipMember, path='unzipped')