import random


def getSubDataSet(src_file, dest_file, rate=0.1, is_random=True):
    """
    rate:the subset size / the origin size
    is_random:choose random line data ,or choose beginning lines 
    """
    with open(src_file) as src:
        lines = src.readlines()
        line_cnt = int(len(lines) * rate)
        with open(dest_file, 'w') as dest:
            if is_random:
                dest.write(lines[0])
                for i in range(line_cnt):
                    dest.write(lines[random.randint(1, len(lines)-1)])
            else:
                dest.writelines(lines[:line_cnt])




