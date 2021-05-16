from time_bar import print_time
from PIL import Image
from shutil import copyfile

import numpy as np
import face_recognition

import os
import time


def distribute_photos(folder, res_fold, master_db, pioners_db, master_set, pioners_set, stock):
    lst = os.listdir(folder)
    st = time.time()

    i = 0
    for el in lst:
        print_time(len(lst), i, st, time.time(), inf='Processing photos...')
        i += 1

        img = Image.open(folder + '/' + el)
        faces = face_recognition.api.face_locations(np.array(img))

        if len(faces) > 0:
            vectors = face_recognition.api.face_encodings(np.array(img), faces, model='large')

            flag = False
            for vec in vectors:
                name = master_db.find(vec)
                if (name is not None) and (name in master_set):
                    flag = True
                    name = '/masters/' + name + '/'
                else:
                    name = pioners_db.find(vec)
                    if (name is not None) and (name in pioners_set):
                        flag = True
                        name = '/pioners/' + name + '/'

                if name is not None:
                    copyfile(folder + '/' + el, res_fold + name + el)

            if not flag:
                copyfile(folder + '/' + el, res_fold + '/_Unrecognized_/' + el)
        else:
            copyfile(folder + '/' + el, res_fold + '/_Empty_/' + el)

        copyfile(folder + '/' + el, stock + '/' + el)
        os.remove(folder + '/' + el)

    print_time(len(lst), i, st, time.time(), inf='Processing photos...', fin=True)
    return True


def calculate_results(folder):
    lst = os.listdir(folder + '/masters')
    print("Finishing program...", end='')

    for el in lst:
        info = open(folder + '/masters/' + el + '/info.inf', 'w')
        info.write(el)
        info.close()

    lst = os.listdir(folder + '/pioners')
    names = []
    sizes = []

    for el in lst:
        info = open(folder + '/pioners/' + el + '/info.inf', 'w')
        info.write(el)
        info.close()
        sizes.append(len(os.listdir(folder + '/pioners/' + el)) - 2)
        names.append(el)

    print("\rProgram finished")
    return names, sizes
