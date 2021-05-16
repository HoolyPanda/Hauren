from time_bar import print_time
from PIL import Image
from photo_manager import create_folder
from shutil import copyfile

import numpy as np

import os
import time
import random
import string
import face_recognition


def get_random_string(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def update_masters(folder, res_fold, master_db, master_set, stock_fold):
    lst = os.listdir(folder)
    st = time.time()

    i = 0
    for el in lst:
        print_time(len(lst), i, st, time.time(), inf='Processing master photos...')
        i += 1

        img = Image.open(folder + '/' + el)
        faces = face_recognition.api.face_locations(np.array(img))

        if len(faces) > 0:
            vectors = face_recognition.api.face_encodings(np.array(img), faces, model='large')

            for j in range(len(vectors)):
                name = master_db.add(get_random_string(20), vectors[j])
                if name not in master_set:
                    create_folder(res_fold + '/masters/' + name, folder, el, faces[j])
                    master_set.add(name)
                else:
                    copyfile(folder + '/' + el, res_fold + '/masters/' + name + '/' + el)

            copyfile(folder + '/' + el, stock_fold + '/' + el)
            os.remove(folder + '/' + el)
        else:
            print("\r!!!!!!!!! WRONG MASTER PHOTO. FOUND 0 People on " + el)

    print_time(len(lst), i, st, time.time(), inf='Processing master photos...', fin=True)
    return True


def update_pioners(folder, res_fold, master_db, pioners_db, masters_set, pioners_set, stock_fold):
    lst = os.listdir(folder)
    st = time.time()

    i = 0
    for el in lst:
        print_time(len(lst), i, st, time.time(), inf='Processing pioners photos...')
        i += 1

        img = Image.open(folder + '/' + el)
        faces = face_recognition.api.face_locations(np.array(img))

        if len(faces) > 0:
            vectors = face_recognition.api.face_encodings(np.array(img), faces, model='large')

            for j in range(len(vectors)):
                nm = master_db.find(vectors[j])
                if nm is None:
                    name = pioners_db.add(get_random_string(20), vectors[j])

                    if name not in pioners_set:
                        create_folder(res_fold + '/pioners/' + name, folder, el, faces[j])
                        pioners_set.add(name)
                    else:
                        copyfile(folder + '/' + el, res_fold + '/pioners/' + name + '/' + el)
                else:
                    if nm in masters_set:
                        copyfile(folder + '/' + el, res_fold + '/masters/' + nm + '/' + el)
                    else:
                        create_folder(res_fold + '/masters/' + nm, folder, el, faces[j])
                        masters_set.add(nm)

            copyfile(folder + '/' + el, stock_fold + '/' + el)
            os.remove(folder + '/' + el)
        else:
            print("\r!!!!!!!!! WRONG PIONERS PHOTO. FOUND 0 People on " + el)

    print_time(len(lst), i, st, time.time(), inf='Processing pioners photos...', fin=True)
    return True
