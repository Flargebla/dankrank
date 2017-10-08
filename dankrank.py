from DankSucc import DankSucc
from PIL import Image

# Succ all the memes
succr = DankSucc("memes")
succr.succ()
succr.persist()

# Normalize the images
for d in succr.grab_danks():
    dank_dir = "danks/"
    img = Image.open(dank_dir+d.filename)
    img = img.resize((1024,1024))
    img.save(dank_dir+d.filename, d.filetype)
