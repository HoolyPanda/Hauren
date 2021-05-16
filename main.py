import numpy as np

from preparation import built_results, check_results
from update_df import update_pioners, update_masters
from distribute import calculate_results, distribute_photos

from df_manager import DBManager

import os


if __name__ == '__main__':

    # Папки куда выводить
    masters = 'masters'
    pioners = 'pioners'
    results = 'results'
    stock = 'stock'

    # Папки с фотографиями
    photos_m = 'photos/masters'
    photos_p = 'photos/pioners'
    photos = 'photos/shots'

    # Сбор баз данных - 0
    m_df = DBManager(masters)
    p_df = DBManager(pioners)

    # Обновляем имена - 1
    if os.path.isdir(results):
        masters_set, pioners_set = check_results(results, m_df, p_df)
    else:
        built_results(results, stock)
        masters_set = set()
        pioners_set = set()

    # Обновляем базы данных - 2
    update_masters(photos_m, results, m_df, masters_set, stock)
    update_pioners(photos_p, results, m_df, p_df, masters_set, pioners_set, stock)

    # Обрабатываем фото
    distribute_photos(photos, results, m_df, p_df, masters_set, pioners_set, stock)

    # Обрабатываем результаты
    names, sizes = calculate_results(results)
    m_df.save()
    p_df.save()

    print(names[np.argmin(sizes)])
