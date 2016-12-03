'''
image_generator.py

Generates novel image through overlaying component images with varying
transparencies.
'''
from __future__ import unicode_literals
import random, os
from PIL import Image

MAX_SIZE = (1080, 1080)

class image_generator(object):

    def __init__(self, bkgd_path, back_overlay_path, overlay_path, vector_path, dest_path):
        self.bkgd_path = bkgd_path
        self.back_overlay_path = back_overlay_path
        self.overlay_path = overlay_path
        self.vector_path = vector_path
        self.dest_path = dest_path

    def __call__(self):

        bkgd = self.__get_src_img(self.bkgd_path).convert("RGBA")
        bkgd.thumbnail(MAX_SIZE, Image.ANTIALIAS)

        # Overlay images
        for i in range(random.randint(0,2)):
            back_overlay = self.__get_src_img(self.back_overlay_path)
            self.__resize(back_overlay, bkgd, random.uniform(2,5)/5)
            back_overlay = self.__alter_opacity(back_overlay)
            self.__paste_image(bkgd, back_overlay, 1.5/2)

        for i in range(random.randint(1,2)):
            overlay = self.__get_src_img(self.overlay_path)
            self.__resize(overlay, bkgd, random.uniform(1,4)/5)
            overlay = self.__alter_opacity(overlay)
            self.__paste_image(bkgd, overlay, 1)

        for i in range(random.randint(0,4)):
            vector = self.__get_src_img(self.vector_path)
            self.__resize(vector, bkgd, 1/random.uniform(1,4))
            vector = self.__alter_opacity(vector)
            self.__paste_image(bkgd, vector, 1.5/2)

        # bkgd.show() # Uncomment to show preview
        try:
            filename = max([int(files.split('.')[0]) \
                            for files in os.listdir(self.dest_path) if files.endswith('.png')])
        except ValueError:
            filename = 0

        filename += 1
        gen_url = os.path.join(self.dest_path, str(filename)+".png")
        bkgd.save(gen_url, "PNG")
        return str(filename)+".png"


    def __get_src_img(self, path):
        path = os.path.join(path)
        img = random.choice(os.listdir(path))
        path = os.path.join(path, img)
        return Image.open(path)


    def __resize(self, img, bkgd, ratio):
        img.thumbnail( (int(ratio*bkgd.width), \
                        int(ratio*bkgd.height)), \
                        Image.ANTIALIAS )


    def __alter_opacity(self, img):
        opacity = random.triangular(0, 1, 0.9)
        bands = list(img.split())
        if len(bands) == 4:
            bands[3]= bands[3].point(lambda x: x*opacity)
            return Image.merge(img.mode, bands)
        return img


    def __paste_image(self, base, img, ratio):
        try:
            base.paste(img, (random.randint(0,base.width-int(ratio*img.width)), \
                             random.randint(0,base.height-int(ratio*img.height))),\
                             img)
        except ValueError:
            base.paste(img, (random.randint(0,base.width-int(ratio*img.width)), \
                             random.randint(0,base.height-int(ratio*img.height))))