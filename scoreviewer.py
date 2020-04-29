import json

def getMods(number):
    # https://github.com/NiceAesth/Sunny/blob/master/commons/osu/osuhelpers.py
    mod_list= []
    if number == 0:	mod_list.append('NM')
    if number & 1<<0:   mod_list.append('NF')
    if number & 1<<1:   mod_list.append('EZ')
    if number & 1<<2:   mod_list.append('TD')
    if number & 1<<3:   mod_list.append('HD')
    if number & 1<<4:   mod_list.append('HR')
    if number & 1<<14:  mod_list.append('PF')
    elif number & 1<<5:   mod_list.append('SD')
    if number & 1<<9:   mod_list.append('NC')
    elif number & 1<<6: mod_list.append('DT')
    if number & 1<<7:   mod_list.append('RX')
    if number & 1<<8:   mod_list.append('HT')
    if number & 1<<10:  mod_list.append('FL')
    if number & 1<<12:  mod_list.append('SO')
    if number & 1<<15:  mod_list.append('4K')
    if number & 1<<16:  mod_list.append('5K')
    if number & 1<<17:  mod_list.append('6K')
    if number & 1<<18:  mod_list.append('7K')
    if number & 1<<19:  mod_list.append('8K')
    if number & 1<<20:  mod_list.append('FI')
    if number & 1<<24:  mod_list.append('9K')
    if number & 1<<25:  mod_list.append('10K')
    if number & 1<<26:  mod_list.append('1K')
    if number & 1<<27:  mod_list.append('3K')
    if number & 1<<28:  mod_list.append('2K')
    return mod_list


def osu_data_ext(bmap):
    dmap = {}
    dmap['artist'] = bmap[0]
    dmap['title'] = bmap[2]
    dmap['diff'] = bmap[5]
    return dmap

def osu_data_star(bmap):
    # osu! standard mod
    stars = {}
    for mod in bmap[19]:
        stars[''.join(getMods(mod[0]))] = mod[1]
    return stars

def scores_ext(scores,star_mod_list):
    smap = {}
    smap['score'] = scores[11]
    smap['max combo'] = scores[12]
    smap['modes'] = getMods(scores[14])
    smap['timestamp'] = scores[16]
    c0,c50,c100,c200,c300,cmax = scores[10],scores[7],scores[6],scores[9],scores[8],scores[12]
    points = c50 * 50 + c100 * 100 + c200 * 200 + c300 * 300 + cmax * 300
    total = c0 + c50 + c100 + c200 + c300 + cmax
    smap['acc'] = points / (total * 300)
    
    smod = ''.join(smap['modes'])
    try:
        smap['star'] = star_mod_list[smod]
    except:
        smap['star'] = 0
        print(f'{smod} no found in beatsmap.')
    
    return smap


def jload(fn):
    with open(fn, "r", encoding="utf-8") as rf:
        return json.load(rf)

def jdump(fn,var):
    with open(fn, "w", encoding="utf-8") as wf:
        return json.dump(var, wf)

def sortkey(data,key):
    # new_s_2 = sorted(new_s,key = lambda e:(e.__getitem__('score'),e.__getitem__('no')))
    return sorted(data,key = lambda e:e.__getitem__(key))


def fundumpj(key=None):
    try:
        scoreboard = jload("scoreboard.json")
    except:
        osu_data = jload("osu!.json")
        scores_data = jload("scores.json")

        map_dict = {}
        for bmap in osu_data[6]:
            # get beatsmap meta data dict
            map_dict[bmap[7]] = [osu_data_ext(bmap),osu_data_star(bmap)]

        scoreboard = []
        for scores in scores_data[2]:
            for score in scores[2]:
                try:
                    bmap = map_dict[score[2]][0] # get ext no star 
                except:
                    print(f'{score[2]} no found')
                    continue
                smap = scores_ext(score,map_dict[score[2]][1]) # get _star 
                smap.update(bmap)
                scoreboard.append(smap)
    if key:
        scoreboard=sortkey(scoreboard,key)
        jdump("sorted_scoreboard.json",scoreboard)
    else:
        # cmdline
        import ipdb
        ipdb.set_trace()

def funvis():
    from matplotlib import pyplot as plt
    scoreboard = jload("sorted_scoreboard.json")
    x,y1,y2=[],[],[]
    for i in range(len(scoreboard)):
        x.append(scoreboard[i]['timestamp'])
        y1.append(scoreboard[i]['acc'])
        try:
            y2.append(scoreboard[i]['star'])
        except:
            y2.append(0)
    plt.plot(x,y1);plt.plot(x,y2)
    plt.show()
    
if __name__ == "__main__":
    fundumpj(key='max combo')