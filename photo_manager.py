from PIL import Image, ImageDraw
from shutil import copyfile

import os


def create_folder(folder, from_folder, photo, place):
    """
    :param folder: Путь до папки с фаилом
    :param from_folder: Из какой папки брать фото
    :param photo: Имя фото
    :param place: Рамка фото
    :param stock: Место для всех фото
    """
    os.mkdir(folder)
    img = Image.open(from_folder + '/' + photo)
    dr = ImageDraw.Draw(img)
    dr.rectangle((place[3], place[0], place[1], place[2]))
    img.save(folder + "/reference.jpg")
    copyfile(from_folder + '/' + photo, folder + '/' + photo)
