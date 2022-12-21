from tinydb import TinyDB, Query, where

db = TinyDB('data.json', indent=4, separators=(',', ': '))

anki = db.table('Anki')
anki_ans = db.table('Anki_ans')
user = db.table('user')
dek = db.table('Dek')
time = db.table('Time')
lst_table = db.table('List')
nom = db.table('Nomer')

query = Query()


def start():
    # anki.insert({})
    # anki_ans.insert({})
    # user.insert({})
    # dek.insert({})
    time.insert({})
    # lst_table.insert({})
    # nom.insert({})


def lst_add(id, name):
    path = lst_table.get(where('id') == id)

    if path:
        path[name] = {}
        lst_table.update(path, where('id') == id)
    else:
        lst_table.insert({'id': id, name: {}})


def dct(name):
    path = lst_table.get(doc_id=1)[name]
    lst = []
    for i in path.keys():
        lst.append(i)
    return lst


def lst_last(name, deck_name):
    '''lst_tableda nechta deck nomi borligini qaytaradi'''
    path = lst_table.get(doc_id=1)[name]
    return len(path)


def no(name, x):
    '''Ko'p list indexlari yangilaydi'''
    path = nom.get(doc_id=1)
    path[name] = x
    nom.update(path)


def no2(name):
    '''Ko'p list indexlari tartib raqamini aniqlaydi'''
    path = nom.get(doc_id=1)
    return path[name]


def lstur(name, deck_name, lst):
    '''yangi kelgan ma'lumotni listga qo'shadi'''
    nm = lst_table.get(doc_id=1)
    path = nm[name]
    if deck_name in path.keys():
        for i in lst:
            path[deck_name].append(i)
    else:
        path[deck_name] = lst
    nm[name] = path
    lst_table.update(nm)


def may(name, deck_name):
    path = lst_table.get(doc_id=1)[name][deck_name]
    if len(path) > 0:
        return True
    else:
        return False


def rem(name, deck_name):
    '''listdagi raqamlarning boshidan o'chirib boradi'''
    nm = lst_table.get(doc_id=1)
    path = nm[name]
    path[deck_name].pop(0)
    nm[name] = path
    lst_table.update(nm)


def lst_pu(name, deck_name, lst):
    '''listga path yaratib  beradi'''
    nm = lst_table.get(doc_id=1)
    path = nm[name]
    path[deck_name] = lst
    nm[name] = path
    lst_table.update(nm)


def lst_up(name, deck_name, lst):
    '''qaysi listlar qaytarilishining indexlarini saqlab turadi'''
    nm = lst_table.get(doc_id=1)
    path = nm[name]
    path[deck_name] = lst
    nm[name] = path
    lst_table.update(nm)


def lst_back(id, deck_name, box='temp'):
    '''qaysi index lari qaytarilishi kerak bo'lgani list qilib qaytaradi'''
    path = time.get(where('user_id') == id)

    if path:
        return path[deck_name][box]
    else:
        raise Exception(f'user {id} doesnt exists')


def deck_end(id, deck_name):
    '''ankida nechta so'z borligini qaytaradi'''
    path = anki.get((where('user_id') == id) & (where('name') == deck_name))
    if path:
        return len(path)
    else:
        raise Exception(f"user_id {id} or deck_name {deck_name} doesnt exists")


def tim(year, month, day, hour, minute, deck_id, deck_name):
    '''shu vaqtdagi oldin kiritganmi yo'qmi shuni ko'radi'''
    path = time.get(doc_id=1)
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    if vaqt not in path:
        return True
    else:
        return False


def timer(id, deck_id, deck_name):
    '''vaqti kelganda qaysi dek nomi va index larini kiritib  boradi'''

    path = time.get(where('user_id') == id)
    if path:
        try:
            path[deck_name]['temp'].append(deck_id)
        except KeyError:
            path[deck_name] = {'temp': [deck_id], 'box': [], 'long': []}
        time.update(path, where('user_id') == id)
    else:
        time.insert({'user_id': id, deck_name: {'temp': [deck_id]}})


def times_up(id, deck_name, box):
    '''Vaqt tuganda shu qaysi dek nomi indexlari qaytaradi'''
    user_deck = time.get(where('user_id') == id)
    if user_deck:
        deck_id = user_deck.get(deck_name).get(box)
    else:
        raise Exception(f'user {id} doenst exists')
    return deck_id


def pop_time(year, month, day, hour, minute):
    '''O'tib bo'lgan vaqtni bazadan o'chirishi kerak'''
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    path = time.get(doc_id=1)
    path[vaqt].pop(0)
    time.update(path)


def user_decks(id):
    '''userning deklarini list qilib qaytaradi'''
    lst = []
    dct = anki.search(where('user_id') == id)
    for i in dct:
        lst.append(i['name'])
    return lst


def search_user(id):
    '''userning nechinchi indexdaligini qaytaradi'''
    path = user.get(where('id') == id)
    if path:
        return path['index']
    raise Exception(f'user {id} doesnt exist')


def search_dek(id):
    '''user qaysi dekda ekanligini qaytaradi'''
    path = user.get(where('id') == id)

    if path:
        return path['dek_name']
    else:
        raise Exception(f'user {id} doesnt exists')


def change_dek(id, d):
    '''User qaysi dekga kirganini saqlab qoladi'''
    path = user.get(where('id') == id)
    if path:
        path['dek_name'] = d
        user.update(path, where('id') == id)
    else:
        raise Exception(f'id {id} doenst exists')


def deck_id_quest(x, name='ajoyib'):
    '''Returns word'''
    ds = anki.get(where('name') == name)
    if ds:
        return ds['data'][str(x)]
    else:
        raise Exception(f'deck {name} doesnt exists')


def deck_id_ans(x, name='ajoyib'):
    '''Returns word'''
    ds = anki_ans.get(where('name') == name)
    if ds:
        return ds['data'][str(x)]
    else:
        raise Exception(f'deck {name} doesnt exists')


def create_decks(id, deck_name):
    '''yangi dek document qo'shadi va agar shu nomli dek bo'lsa qo'shmay false qaytardi '''

    question = anki.get(where('name') == deck_name)
    answer = anki_ans.get(where('name') == deck_name)

    if question and answer:
        raise Exception(
            f'question {question} or answer {answer} does not exists')
    else:
        anki.insert({'name': deck_name, 'user_id': id, 'data': {}})
        anki_ans.insert({'name': deck_name, 'user_id': id, 'data': {}})


def quest(question, name='Decks'):
    '''user ning qaysi dekda ekanligiga qarab shu dek savollarni qo'shadi'''
    # getting deck accordingly
    quest = anki.get(where('name') == name)

    try:
        id = int(list(quest['data'].keys())[-1])
    except IndexError:
        id = 0

    quest['data'][id + 1] = question
    anki.update(quest, where('name') == name)


def ans(answer, name='Decks'):
    '''userning qaysi dekdagi nominiga qarab shunga javoblarini qo'shib ketadi'''
    # getting deck accordingly
    ans = anki_ans.get(where('name') == name)

    try:
        id = int(list(ans['data'].keys())[-1])
    except IndexError:
        id = 0

    ans['data'][id + 1] = answer
    anki_ans.update(ans, where('name') == name)


def add_user(id: int, user_name: str) -> None:
    '''yangi user qo'shadi agar oldindan bo'lsa olindigi qolib ketgan historyni yangilaydi'''

    d = user.get(where('id') == id)
    # path = dek.get(query.id == id)

    if d:
        d['index'] = 1
        # path['index'] = 1
    else:
        d = {
            'id': id,
            'index': 1,
            'previous_index': 1,
            'temp': [],
            'long': [],
            'box': [],
        }
        # path = {'id': id, 'index': 1, 'username': user_name}
        # user.insert(path)
        user.insert(d)
    # user.update(path, where('id') == id)
    user.update(d, where('id') == id)


def change_user(id, index):
    '''userni indexi yangilab turadi'''

    path = user.get(where('id') == id)
    path['index'] = index

    user.update(path, where('id') == id)


if __name__ == '__main__':
    # start()
    # add_user(1)
    quest = anki.get(where('name') == 'qwer')
    print(quest)
    # try:
    #     id = int(list(quest['data'].keys())[-1])
    # except IndexError:
    #     id = 0
    # quest['data'][id + 1] = 'bye'
    # anki.update(quest, where('name') == 'qwer')