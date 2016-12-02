''' 
image_generator.py

Generates novel image through overlaying component images with varying 
transparencies.
'''
import random, os
from PIL import Image

def resize(img, bkgd, ratio):
    img.thumbnail( (int(ratio*bkgd.width), \
                    int(ratio*bkgd.height)), \
                    Image.ANTIALIAS )


def alter_opacity(img):
    opacity = random.triangular(0, 1, 0.9)
    bands = list(img.split())
    if len(bands) == 4:
        bands[3]= bands[3].point(lambda x: x*opacity)
        return Image.merge(img.mode, bands)
    return img


def paste_image(base, img, ratio):
    try:
        base.paste(img, (random.randint(0,base.width-int(ratio*img.width)), \
                         random.randint(0,base.height-int(ratio*img.height))),\
                         img)
    except ValueError:
        base.paste(img, (random.randint(0,base.width-int(ratio*img.width)), \
                         random.randint(0,base.height-int(ratio*img.height))))


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
        resize(back_overlay, bkgd, random.uniform(2,5)/5)
        back_overlay = alter_opacity(back_overlay)
        paste_image(bkgd, back_overlay, 1.5/2)

    for i in range(random.randint(1,2)):
        overlay = Image.open( "src/" + random.choice(os.listdir("src")) )
        resize(overlay, bkgd, random.uniform(1,4)/5)
        overlay = alter_opacity(overlay)
        paste_image(bkgd, overlay, 1)

    for i in range(random.randint(0,4)):
        vector = Image.open( "src/vectors/" \
                            + random.choice(os.listdir("src/vectors")) )
        resize(vector, bkgd, 1/random.uniform(1,4))
        vector = alter_opacity(vector)
        paste_image(bkgd, vector, 1.5/2)

    bkgd.show() # Uncomment to show preview
    try:
        filename = max([int(files.split('.')[0]) \
                        for files in os.listdir(".") if files.endswith('.png')])
    except ValueError:
        filename = 0

    filename += 1
    bkgd.save(str(filename)+".png", "PNG")