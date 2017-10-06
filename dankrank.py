from DankSucc import DankSucc

# Succ all the memes
succr = DankSucc("dankmemes,memes", 2)
succr.succ()

# Normalize the images
for d in succr.grab_danks():
    print(d.score)
