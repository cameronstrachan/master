import zipfile36

with zipfile.ZipFile("master2.zip","r") as zip_ref:
    zip_ref.extractall("unzipped")