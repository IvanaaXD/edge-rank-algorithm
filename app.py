import networkx as nx
import pickle
from datetime import datetime

objave = []

tezine = {
    "likes": 100,
    "loves": 150,
    "wows": 120,
    "hahas": 80,
    "sads": 50,
    "angrys": 30,
    "special": 100,
    "comments": 200,
    "shares": 400,
}

# status_id,status_message,link_name,status_type,status_link,status_published,authornum_reactions,num_comments,num_shares,num_likes,num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special


def izracunaj_tezinu_reakcije(korisnik1, korisnik2, reactions, statuses):

    likes = 0
    loves = 0
    wows = 0
    hahas = 0
    sads = 0
    angrys = 0
    special = 0

    dict_lajkovi = reactions[korisnik1]

    if dict_lajkovi == {}:
        return 0

    broj = 0
    for status_id in dict_lajkovi.keys():
        status = statuses[status_id]

        if status[5] == korisnik2:

            if dict_lajkovi[status_id][0] == "likes":
                likes += 1
            if dict_lajkovi[status_id][0] == "loves":
                loves += 1
            if dict_lajkovi[status_id][0] == "wows":
                wows += 1
            if dict_lajkovi[status_id][0] == "hahas":
                hahas += 1
            if dict_lajkovi[status_id][0] == "sads":
                sads += 1
            if dict_lajkovi[status_id][0] == "angrys":
                angrys += 1
            if dict_lajkovi[status_id][0] == "special":
                special += 1

            broj = izracunaj_vrijeme_raspada_opis_objave(reactions[korisnik1][status_id][1])

    reakcija = likes * tezine["likes"] + loves * tezine["loves"] + wows * tezine["wows"] + hahas * tezine["hahas"] + sads * tezine["sads"] + angrys * tezine["angrys"] + special * tezine["special"] + broj

    return reakcija


def izracunaj_tezinu_komentara(korisnik1, korisnik2, comments, statuses):

    komentari = 0

    if korisnik1 in comments.keys():

        lista_status_id_komentari = comments[korisnik1]
        broj = 0

        for key in lista_status_id_komentari:

            status = statuses[key]

            if status[5] == korisnik2:
                komentari += 1
                broj = izracunaj_vrijeme_raspada_opis_objave(lista_status_id_komentari[key])

        return komentari*tezine["comments"] + broj
    else:
        return 0


def izracunaj_tezinu_dijeljenja(korisnik1, korisnik2, shares, statuses):

    dijeljenja = 0

    if korisnik1 in shares.keys():

        lista_status_id_dijeljenja = shares[korisnik1]
        broj = 0

        for key in lista_status_id_dijeljenja:
            status = statuses[key]

            if status[5] == korisnik2:
                dijeljenja += 1
                broj = izracunaj_vrijeme_raspada_opis_objave(lista_status_id_dijeljenja[key])

        return dijeljenja*tezine["shares"] + broj
    else:
        return 0


def provjeri_prijatelja(korisnik1, korisnik2, friends):

    if korisnik2 in friends[korisnik1]:
        return True


def napravi_graf(friends, graf, reactions, comments, shares, statuses):
    for korisnik1 in friends.keys():
        for korisnik2 in friends.keys():

            if korisnik1 != korisnik2:
                lajkovi = izracunaj_tezinu_reakcije(korisnik1, korisnik2, reactions, statuses)
                komentari = izracunaj_tezinu_komentara(korisnik1, korisnik2, comments, statuses)
                dijeljenja = izracunaj_tezinu_dijeljenja(korisnik1, korisnik2, shares, statuses)

                prijatelj = provjeri_prijatelja(korisnik1, korisnik2, friends)
                broj = 0
                if prijatelj:
                    broj = 10000

                afinitet = lajkovi + komentari + dijeljenja + broj

                if afinitet != 0:
                    graf.add_edge(korisnik1, korisnik2, weight=afinitet)

    pickle_file = open("./dataset/picklefile.pickle", "wb")

    pickle.dump(graf, pickle_file)
    pickle_file.close()


def dodaj_u_graf(friends, graf, reactions, comments, shares, statuses):
    for korisnik1 in friends.keys():
        for korisnik2 in friends.keys():

            if korisnik1 != korisnik2:
                lajkovi = izracunaj_tezinu_reakcije(korisnik1, korisnik2, reactions, statuses)
                komentari = izracunaj_tezinu_komentara(korisnik1, korisnik2, comments, statuses)
                dijeljenja = izracunaj_tezinu_dijeljenja(korisnik1, korisnik2, shares, statuses)

                prijatelj = provjeri_prijatelja(korisnik1, korisnik2, friends)
                broj = 0
                if prijatelj:
                    broj = 10000

                afinitet = lajkovi + komentari + dijeljenja + broj

                if afinitet != 0:
                    graf.add_edge(korisnik1, korisnik2, weight=afinitet)

    pickle_file = open("./dataset/picklefile.pickle", "wb")

    pickle.dump(graf, pickle_file)
    pickle_file.close()


def pregled_objava(username, neighbors, statuses, graf):
    objave_dict = {}

    for i in range(len(neighbors)):
        neighbor = neighbors[i]
        # print(neighbor)

        for status in statuses.keys():

            if statuses[status][5] == neighbor:
                objava = statuses[status]

                afinitet = graf.get_edge_data(username, neighbor)['weight']
                if not afinitet:
                    afinitet = 1

                popularnost = izracunaj_popularnost(objava)

                vrijeme_raspada = izracunaj_vrijeme_raspada(objava)

                rank = edge_rank(afinitet, popularnost, vrijeme_raspada)

                objave_dict[objava[0]] = rank

    sortiranje_objava(objave_dict, statuses)


def sortiranje_objava(objave_dict, statuses):

    sorted_objave = sorted(objave_dict.items(), key=lambda x: x[1], reverse=True)

    top_10_objava = dict(sorted_objave[:10])

    print_objave(top_10_objava, statuses)


def izracunaj_popularnost(objava):

    # status_id,status_message,link_name,status_type,status_link,status_published,author,num_reactions,num_comments,num_shares,num_likes,num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special
    # print(objava[0])

    num_reactions = int(objava[6])
    num_comments = int(objava[7])
    num_shares = int(objava[8])

    broj = num_shares * tezine["shares"] + num_comments * tezine["comments"] + num_reactions

    num_likes = int(objava[9])
    num_loves = int(objava[10])
    num_wows = int(objava[11])
    num_hahas = int(objava[12])
    num_sads = int(objava[13])
    num_angrys = int(objava[14])
    num_special = int(objava[15])

    vrijednost = num_likes * tezine["likes"] + num_loves * tezine["loves"] + num_wows * tezine["wows"] + num_hahas * tezine["hahas"] + num_sads * tezine["sads"] + num_angrys * tezine["angrys"] + num_special * tezine["special"]

    popularnost = broj + vrijednost

    return popularnost


def izracunaj_vrijeme_raspada(objava):

    # vrijeme_string = objava[4]
    # date_format = "%Y-%m-%d %H:%M:%S"
    # vrijeme = datetime.strptime(vrijeme_string, date_format)

    sada = datetime.now()

    razlika = sada - objava[4]

    if razlika.days < 5:
        return 10000
    elif razlika.days < 10:
        return 7000
    elif razlika.days < 20:
        return 3000
    elif razlika.days < 30:
        return 2000
    else:
        return 100


def izracunaj_vrijeme_raspada_opis_objave(vrijeme):

    # date_format = "%Y-%m-%d %H:%M:%S"
    # vrijeme = datetime.strptime(vrijeme_string, date_format)

    sada = datetime.now()

    razlika = sada - vrijeme

    if razlika.days < 5:
        return 10000
    elif razlika.days < 10:
        return 7000
    elif razlika.days < 20:
        return 3000
    elif razlika.days < 30:
        return 2000
    else:
        return 100


def edge_rank(afinitet, popularnost, vrijeme_raspadanja):

    value = afinitet*popularnost*vrijeme_raspadanja
    return value


def print_objave(objave, statuses):
    # status_id,status_message,link_name,status_type,status_link,status_published,author,num_reactions,num_comments,num_shares,num_likes,num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special

    for i, key in enumerate(objave.keys()):
        objava = {
            "status_message": statuses[key][1],
            "link_name": statuses[key][2],
            "status_type": statuses[key][3],
            "status_link": statuses[key][4],
            "status_published": statuses[key][5],
            "authornum_reactions": statuses[key][6],
            "num_comments": statuses[key][7],
            "num_shares": statuses[key][8],
            "num_likes": statuses[key][9],
            "num_loves": statuses[key][10],
            "num_wows": statuses[key][11],
            "num_hahas": statuses[key][12],
            "num_sads": statuses[key][13],
            "num_angrys": statuses[key][14],
            "num_specials": statuses[key][15]
        }

        print()
        print(f"Objava {i + 1}:")
        for key, value in objava.items():
            print(f"{key}: {value}")

        print()


def poredaj_po_bodovima(graf, username, neighbors, status_ids, statuses):
    objave_dict = {}

    for i in status_ids.keys():
        objava = statuses[i]
        autor = objava[5]

        afinitet = 1

        if autor in neighbors:
            afinitet = graf.get_edge_data(username, autor)['weight']

        popularnost = izracunaj_popularnost(objava)

        vrijeme_raspada = izracunaj_vrijeme_raspada(objava)

        rank = edge_rank(afinitet, popularnost, vrijeme_raspada)

        if status_ids[i] > 1:
            print(status_ids[i], popularnost, i)
            value = rank + status_ids[i] * popularnost * 10000
        else:
            value = rank + status_ids[i] * popularnost

        objave_dict[objava[0]] = value

    sortiranje_objava(objave_dict, statuses)
