#!/usr/bin/env python
import urllib.request
import re
import tkinter
import io
from argparse import ArgumentParser
from PIL import Image
from PIL import ImageTk


def request_htmlbody():
    request = urllib.request.Request("https://www.qwertee.com/", headers={'User-Agent': "Magic Browser"})
    return urllib.request.urlopen(request).read().decode("utf-8").replace('\r', '').replace('\n', '')


def find_image_tags(html_body):
    divs = re.compile(r'<div class="mens-dynamic-image design-dynamic-image.*?</div>').findall(html_body)

    img_src_pattern = re.compile(r'<img src=".*?">')

    images_tags = []

    for div in divs:
        images_tags.append(img_src_pattern.findall(div)[0])

    return images_tags


def strip_img_urls(images):
    return ["https:" + s.replace(r'<img src="', '',).replace(r'">', '') for s in images]


def get_imagetk_from_url(url):
    request = urllib.request.Request(url,headers={'User-Agent': "Magic Browser"})
    raw_data = urllib.request.urlopen(request).read()
    return ImageTk.PhotoImage(Image.open(io.BytesIO(raw_data)))


def close_window(event):
    root.destroy()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--borderless', '-b', type=int, default=1)
    parser.add_argument('--positionX', '-x', type=int, default=0)
    parser.add_argument('--positionY', '-y', type=int, default=0)

    args = parser.parse_args()

    html_body = request_htmlbody()
    image_urls = strip_img_urls(find_image_tags(html_body))

    root = tkinter.Tk()
    root.title("Qwertee shirts")
    root.bind('<Escape>', close_window)
    root.overrideredirect(args.borderless)
    root.geometry('+{:d}+{:d}'.format(args.positionX, args.positionY))

    img = get_imagetk_from_url(image_urls[0])
    img2 = get_imagetk_from_url(image_urls[1])
    img3 = get_imagetk_from_url(image_urls[2])

    photo_label = tkinter.Label(image=img)
    photo_label2 = tkinter.Label(image=img2)
    photo_label3 = tkinter.Label(image=img3)

    photo_label.pack(side=tkinter.LEFT)
    photo_label2.pack(side=tkinter.LEFT)
    photo_label3.pack(side=tkinter.LEFT)

    root.mainloop()
