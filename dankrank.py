from DankSucc import DankSucc
from PIL import Image

# Succ all the memes
succr = DankSucc("me_irl")
succr.succ()
succr.persist()

# Normalize the images
for d in succr.grab_danks():
    dank_dir = "danks/"
    try:
        img = Image.open(dank_dir+d.filename)
        img = img.resize((1024,1024))
        img.save(dank_dir+d.filename, d.filetype)
    except PermissionError:
        print("PermissionError, Failed to open:",dank_dir+d.filename)
        succr.kill_dank(d)
    except OSError:
        print("OSError, Invalid image format:",dank_dir+d.filename) 
        succr.kill_dank(d)
