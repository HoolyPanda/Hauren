import numpy as np

from preparation import built_results, check_results
from update_df import update_pioners, update_masters
from distribute import calculate_results, distribute_photos

from df_manager import DBManager

import pandas as pd

import os
import vk_api
import random

if __name__ == '__main__':
    bot = vk_api.VkApi(token=open('./token.cred', 'r').readline().replace('\n', ''))
    bot._auth_token()

    # Папки куда выводить
    masters = './results/masters'
    pioners = './results/pioners'
    results = './results'
    stock = './stock'

    # Папки с фотографиями
    photos_m = './photos/masters'
    photos_p = './photos/pioners'
    photos = './photos/shots'

    # Сбор баз данных - 0
    m_df = DBManager('masters')
    p_df = DBManager('pioners')

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
    names[np.argmin(sizes)]
    pioners = dict(zip(names, sizes))
    for i in range((len(p_df.df))):
        el = p_df.df.loc[i]
        for n in pioners.keys():
            if p_df.df.loc[i]['name'] == n:
                p_df.df.at[i, 'total_photos'] = pioners[n]

    a = np.argmin(pioners.values())
    
    photographers = pd.read_sql_table('photographers', p_df.engine)

    sum = 0
    for k,v in enumerate(pioners):
        sum += pioners[v]
    avg = sum/len(pioners)

    for p_id in range(len(p_df.df)):
        if p_df.df.loc[p_id]['total_photos'] < avg:
            for ph_id in range(len(photographers)):
                if photographers.loc[ph_id]['corpus'] == p_df.df.loc[p_id]['corpus']:
                    msg = f"Привет, {photographers.loc[ph_id]['name']}!\nКажется, {p_df.df.loc[p_id]['name']} недофоткан. Я насчитал у него {p_df.df.loc[p_id]['total_photos']} фоток, в то время, как среднее арифметическое фоток на ребенка составляет {avg}"
                    try:
                        bot.method('messages.send', {'user_id': photographers.loc[ph_id]['vk_id'], 'message': msg, 'random_id':random.randint(1,1000000000000000000)})
                    except Exception as e:
                        print(e)

            b = 0
            

    # bot.method()
    m_df.save()
    p_df.save()

