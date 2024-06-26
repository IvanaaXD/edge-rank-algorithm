import pickle
import networkx as nx
import re
import time

from app import pregled_objava, napravi_graf, poredaj_po_bodovima
from parse_files_mine import load_statuses, load_comments, load_shares, load_reactions, load_friends
from trie import Trie

if __name__ == '__main__':

    statuses_path = "dataset/statuses.csv"
    comments_path = "dataset/comments.csv"
    shares_path = "dataset/shares.csv"
    reactions_path = "dataset/reactions.csv"
    friends_path = "dataset/friends.csv"

    sada = time.time()
    statuses = load_statuses(statuses_path)
    comments = load_comments(comments_path)
    shares = load_shares(shares_path)
    reactions = load_reactions(reactions_path)
    friends = load_friends(friends_path)
    sad = time.time()

    # print(sad - sada)

    # graf = nx.DiGraph()
    #
    # d = time.time()
    # napravi_graf(friends, graf, reactions, comments, shares, statuses)
    # f = time.time()
    # print(f - d)

    pickle_file = open("./dataset/picklefile.pickle", "rb")
    graf = pickle.load(pickle_file)
    pickle_file.close()

    # print(graf)

    statusi = {}

    for key in statuses.keys():
        statusi[key] = statuses[key][1]

    trie = Trie()

    for key, message in statusi.items():
        # poruke = re.sub("[^a-z^A-Z]", " ", message).split()
        porukee = re.findall(r'\b\w+\b', message)

        for p in porukee:
            trie.insert(p.lower(), key)

    username = input("Ulogujte se (ime i prezime): ")

    while username not in friends.keys():
        print("Uneseno korisničko ime nije validno. Molimo unesite ispravno korisničko ime.")
        username = input("Ulogujte se (ime i prezime): ")

    neighbors = list(graf.neighbors(username))

    drama = True

    while drama:
        print("1. Pregled objava")
        print("2. Pretraga")
        print("3. Izlazak iz aplikacije")
        choice = input("Izaberite opciju: ")

        if choice == "1":
            pregled_objava(username, neighbors, statuses, graf)
        elif choice == "2":
            unos = input("Unesite sta zelite da pretrazite: ")

            lista = unos.lower().split()

            listica = []
            words_starting_with_prefix = []
            found = False
            for word in lista:
                if word.endswith("*"):
                    found = True
                    prefix = word[:-1]
                    words_starting_with_prefix = trie.pretraga(prefix)
                else:
                    listica.append(word)

            if found:
                print(words_starting_with_prefix)

                unos = input("Unesite sta zelite da pretrazite: ")
                listica.append(unos.lower().split())

            status_ids = trie.search(listica)

            if status_ids:
                poredaj_po_bodovima(graf, username, neighbors, status_ids, statuses)

                # for id in status_ids.keys():
                # print("Status IDs:", id, status_ids[id])
            else:
                print("Ne postoji objava sa trazenim rijecima.")

        elif choice == "3":
            print("Hvala sto ste koristili nasu aplikaciju!")
            drama = False
            exit()
        else:
            print("Greska prilikom unosa! Pokusajte ponovo!")
            choice = input("Izaberite opciju: ")
