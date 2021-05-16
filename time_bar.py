import time


def print_time(sz, i, st_time, now_time, inf='', fin=False):
    if fin:
        print("\r" + inf + " Finished")
        return 0

    dif = int((now_time - st_time) * (sz - i) / (i + 0.01))
    if dif > 60:
        time_str = str(dif // 60) + 'm ' + str(dif % 60) + 's '
    else:
        time_str = str(dif % 60) + 's '

    print("\r" + inf + ' processed: ' + str(i) + '/' + str(sz) + "| " + time_str, end='')
    return 0
