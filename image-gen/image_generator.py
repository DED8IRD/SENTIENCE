''' 
image_generator.py

Generates novel image through overlaying component images with varying 
transparencies.
'''
import random, os
from PIL import Image, ImageFilter

if __name__ == '__main__':

    max_size = (1080, 1080)
    bkgd = Image.open( "src/bkgd/" + random.choice(os.listdir("src/bkgd")) )
    bkgd = bkgd.convert("RGBA")

    # Resize the images according to max_size and the background img size
    bkgd.thumbnail(max_size, Image.ANTIALIAS)

    # Overlay images
    for i in range(random.randint(0,2)):
        back_overlay = Image.open( "src/back overlays/" \
                     + random.choice(os.listdir("src/back overlays")) )
        back_overlay.thumbnail((random.randint(2,5)*bkgd.width/5, \
                                random.randint(2,5)*bkgd.height/5), \
                                Image.ANTIALIAS)
        try:
            bkgd.paste(back_overlay, \
                (random.randint(0, bkgd.width-1.5*back_overlay.width//2), \
                 random.randint(0, bkgd.height-1.5*back_overlay.height//2)),\
                 back_overlay)
        except ValueError:
            bkgd.paste(back_overlay, \
                (random.randint(0, bkgd.width-1.5*back_overlay.width//2), \
                 random.randint(0, bkgd.height-1.5*back_overlay.height//2)))

    for i in range(random.randint(1,2)):
        overlay = Image.open( "src/" + random.choice(os.listdir("src")) )
        overlay.thumbnail((random.randint(2,5)*bkgd.width/5, \
                           random.randint(2,5)*bkgd.height/5), \
                           Image.ANTIALIAS)
        try:
            bkgd.paste(overlay, \
                      (random.randint(0, bkgd.width-overlay.width), \
                       random.randint(0, bkgd.height-overlay.height)), \
                       overlay)
        except ValueError:
            bkgd.paste(overlay, \
                      (random.randint(0, bkgd.width-overlay.width), \
                       random.randint(0, bkgd.height-overlay.height)))

    for i in range(random.randint(0,4)):
        vector = Image.open( "src/vectors/" \
                            + random.choice(os.listdir("src/vectors")) )
        vector.thumbnail((bkgd.width/random.randint(2,5), \
                          bkgd.height/random.randint(2,5)), \
                          Image.ANTIALIAS)
        try:
            bkgd.paste(vector, \
                      (random.randint(0, bkgd.width-1.5*vector.width//2), \
                       random.randint(0, bkgd.height-1.5*vector.height//2)),\
                       vector)
        except ValueError: 
            bkgd.paste(vector, \
                      (random.randint(0, bkgd.width-1.5*vector.width//2), \
                       random.randint(0, bkgd.height-1.5*vector.height//2)))

    bkgd.show() # Uncomment to show preview
    filename = max([int(files.split('.')[0]) \
                    for files in os.listdir(".") if files.endswith('.png')])
    filename += 1
    bkgd.save(str(filename)+".png", "PNG")