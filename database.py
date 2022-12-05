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
    anki.insert({})
    anki_ans.insert({})
    user.insert({})
    dek.insert({})
    time.insert({})
    lst_table.insert({})
    nom.insert({})


def lst_add(name):
    path = lst_table.get(doc_id=1)
    path[name] = {}
    lst_table.update(path)


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


def lst_back(name, deck_name):
    '''qaysi index lari qaytarilishi kerak bo'lgani list qilib qaytaradi'''
    path = lst_table.get(doc_id=1)[name][deck_name]
    return path


def deck_end(first_name, deck_name):
    '''ankida nechta so'z borligini qaytaradi'''
    path = anki.get(doc_id=1)[first_name][deck_name]
    return len(path)


def tim(year, month, day, hour, minute, deck_id, deck_name):
    '''shu vaqtdagi oldin kiritganmi yo'qmi shuni ko'radi'''
    path = time.get(doc_id=1)
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    if vaqt not in path:
        return True
    else:
        return False


def timer(year, month, day, hour, minute, deck_id, deck_name):
    '''vaqti kelganda qaysi dek nomi va index larini kiritib  boradi'''
    path = time.get(doc_id=1)
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    if vaqt not in path:
        path[vaqt] = []
    path[vaqt + 'deck'] = deck_name
    lst = path[vaqt]
    lst.append(deck_id)
    time.update(path)


def times_up(year, month, day, hour, minute):
    '''Vaqt tuganda shu qaysi dek nomi indexlari qaytaradi'''
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    deck_id = time.get(doc_id=1)[vaqt]
    deck_name = time.get(doc_id=1)[vaqt + 'deck']
    return deck_id, deck_name


def pop_time(year, month, day, hour, minute):
    '''O'tib bo'lgan vaqtni bazadan o'chirishi kerak'''
    vaqt = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(
        hour) + ':' + str(minute)
    path = time.get(doc_id=1)
    path[vaqt].pop(0)
    time.update(path)


def user_decks(first_name):
    '''userning deklarini list qilib qaytaradi'''
    lst = []
    dct = anki.get(doc_id=1)[first_name].keys()
    for i in dct:
        lst.append(i)
    return lst


def search_user(name):
    '''userning nechinchi indexdaligini qaytaradi'''
    path = user.get(doc_id=1)
    return path[name]


def search_dek(name):
    '''user qaysi dekda ekanligini qaytaradi'''
    path = dek.get(doc_id=1)
    return path[name]


def change_dek(name, d):
    '''User qaysi dekga kirganini saqlab qoladi'''
    path = dek.get(doc_id=1)
    path[name] = d
    dek.update(path)


def deck_id_quest(x, first_name, name='ajoyib'):
    '''Returns word'''
    ds = anki.get(doc_id=1)[first_name][name][str(x)]['question']
    return ds


def deck_id_ans(x, first_name, name='ajoyib'):
    '''Returns word'''
    ds = anki_ans.get(doc_id=1)[first_name][name][str(x)]['answer']
    return ds


def create_decks(deck_name, first_name):
    '''yangi dek document qo'shadi va agar shu nomli dek bo'lsa qo'shmay false qaytardi '''

    first = anki.get(doc_id=1)
    last = anki_ans.get(doc_id=1)
    if first_name not in first:
        first[first_name] = {}
        last[first_name] = {}
    bir = first[first_name]
    bir[deck_name] = {}
    first[first_name] = bir
    ikki = last[first_name]
    ikki[deck_name] = {}
    last[first_name] = ikki
    anki.update(first)
    anki_ans.update(last)


def quest(question, first_name, name='Decks'):
    '''user ning qaysi dekda ekanligiga qarab shu dek savollarni qo'shadi'''
    dct = anki.get(doc_id=1)
    path = dct[first_name][name]
    last = len(path)
    last += 1
    path[str(last)] = {'question': question}
    dct[first_name][name] = path
    anki.update(dct)


def ans(answer, first_name, name='Decks'):
    '''userning qaysi dekdagi nominiga qarab shunga javoblarini qo'shib ketadi'''
    dct = anki_ans.get(doc_id=1)
    path = dct[first_name][name]
    last = len(path)
    last += 1
    path[str(last)] = {'answer': answer}
    dct[first_name][name] = path
    anki_ans.update(dct)


def add_user(id: int, user_name: str) -> None:
    '''yangi user qo'shadi agar oldindan bo'lsa olindigi qolib ketgan historyni yangilaydi'''

    d = user.get(query.id == id)
    path = dek.get(query.id == id)

    # def your_operation(your_arguments):

    #     def transform(doc):
    #         print(doc)
    #         return transform

    # user.update(your_operation('index'), query.id == id)
    # dek.update(your_operation('index'), query.id == id)
    if d and path:
        d['index'] = 1
        path['index'] = 1
    else:
        d = {'id': id, 'index': 1, 'username': user_name}
        path = {'id': id, 'index': 1, 'username': user_name}
        user.insert(path)
        dek.insert(d)
    user.update(path, where('id') == id)
    dek.update(d, where('id') == id)


def change_user(name, x):
    '''userni indexi yangilab turadi'''
    path = user.get(doc_id=1)
    path[name] = x
    user.update(path)


if __name__ == '__main__':
    start()
    # add_user(1)