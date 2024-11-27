def fileRead(fileName:str):
    with open(fileName,'r',encoding='utf-8') as f:
        ret = f.readlines()
    return ret

def fileAppend(fileName:str, writeStr:str, overLap:bool=True):
    if overLap:
        with open(fileName,'a',encoding='utf-8') as f:
            f.write(f'{writeStr}\n')
    else:
        with open(fileName,'r',encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if line.rstrip('\n') == writeStr:
                return
        with open(fileName,'a',encoding='utf-8') as f:
            f.write(f'{writeStr}\n')
