import os


def check_results(folder, m_df, p_df):

    lst_m = os.listdir(folder + '/masters')
    lst_p = os.listdir(folder + '/pioners')
    pioners_set = set()
    masters_set = set()

    for fold in lst_m:
        if os.path.isdir(folder + '/masters/' + fold):
            info = open(folder + '/masters/' + fold + '/' + 'info.inf', 'r')
            nm = info.readline()
            info.close()
            if nm != fold:
                m_df.change_name(nm, fold)
            masters_set.add(nm)

    for fold in lst_p:
        if os.path.isdir(folder + '/pioners/' + fold):
            info = open(folder + '/pioners/' + fold + '/' + 'info.inf', 'r')
            nm = info.readline()
            if nm != fold:
                p_df.change_name(nm, fold)
                # TODO: English, check this shit
            pioners_set.add(nm)
    # TODO: remove name from df if folder deited
    return masters_set, pioners_set


def built_results(folder, stock):
    try:
        os.mkdir(folder)
    except:
        pass
    try:
        os.mkdir(folder + '/_Unrecognized_')
    except:
        pass
    try:
        os.mkdir(folder + '/pioners')
    except:
        pass
    try:
        os.mkdir(folder + '/masters')
    except:
        pass
    try:
        os.mkdir(folder + '/_Empty_')
    except:
        pass
    try:
        os.mkdir(stock)
    except:
        pass
