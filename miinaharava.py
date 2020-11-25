'''
Hassun hauska peli

TEKIJÄ: OTTO LOUKKOLA
'''

import time
import datetime
import random
import haravasto

tietoja_sanakirja = {
    "koko_x": 15,
    "koko_y": 15,
    "miinat": 45

}
vuoro = 0
loukkis = ""
aika = 0
koko_aika = 0
aloitus_aika = 0
kentta = []

jaljella = []

nakyva = []
pelijatkuu = True

def kysy_asioita():
    '''
    Valitaan mitä käyttäjä haluaa tehdä.
    '''
    while True:
        w = input("Mitä haluat tehdä? Valitse peli (P), lopetus (L) tai tilastot (T): ")
        if w == "P":
            #Valitsee pelin.
            break
        elif w == "T":
            #Valitsee tilastot.
            break
        elif w == "L":
            #Valitsee lopettamisen.
            break
        else:
            print("Valitse niistä vaihtoehdoista, jotka siinä ovat tarjolla!!!")
    return w

def tee_asioita():
    '''
    Funktio, jossa asetetaan kaikki lukuarvot ja tarkistetaan, että ne  ovat "laillisia".
    '''
    while True: #pyörittäjä
        try:
            x_ruudut = int(input("Montako x-ruutua (positiivinen)? ")) #kysytään montako ruutua
            tietoja_sanakirja["koko_x"] = x_ruudut
        except ValueError:
            print("Yritä uudelleen!") #pyydetään käyttäjää yrittämään uudelleen
        else:
            if x_ruudut > 0:
                break
    while True:
        try:
            y_ruudut = int(input("Montako y-ruutua (positiivinen)? ")) 
            #kysytään lisää infoa ruuduista
            tietoja_sanakirja["koko_y"] = y_ruudut
        except ValueError:
            print("Yritä uudelleen!")
        else:
            if y_ruudut > 0:
                break
    while True:
        try:
            miina_maara = int(input("Monatako miinaa laitetaan (> 0 ja pienempi kuin kentän ruutujen määrä)? "))
            tietoja_sanakirja["miinat"] = miina_maara
        except ValueError:
            print("Yritä uudelleeen!")
        else:
            if miina_maara in range(1, tietoja_sanakirja["koko_x"] * tietoja_sanakirja["koko_y"]):
                break

def kentan_listan_luominen():
    '''
    Luodaan halutun kokoinen kenttä listana.
    '''
    for i in range(tietoja_sanakirja["koko_y"]):
        rivi = [" "] * tietoja_sanakirja["koko_x"]
        kentta.append(rivi)

def nakyva_listan_luominen():
    '''
    Luodaan halutun kokoinen kenttä listana.
    '''
    for i in range(tietoja_sanakirja["koko_y"]):
        rivi = [" "] * tietoja_sanakirja["koko_x"]
        nakyva.append(rivi)

def miinoita(lista, vapaat, n):
    """
    Miinoittaa kentän satunnaisesti halutulla määrällä miinoja.
    """
    for i in range(n):
        arvottu = random.randint(0, len(vapaat) - 1)
        x, y = vapaat[arvottu]
        vapaat.pop(arvottu)

        lista[y][x] = "x"

def hiiren_vasenta_painetaan_miinan_kohdalla():
    '''
    Tämä funktio menee päälle, jos käyttäjä painaa hiiren vasemmalla kohtaa jossa on miina.
    '''
    global aika
    global koko_aika
    global loukkis
    global pelijatkuu
    for y, y_sisalto in enumerate(kentta):
        for x, x_sisalto in enumerate(y_sisalto):
            if kentta[y][x] == "x":
                nakyva[y][x] = x_sisalto
            else:
                pass
    pelijatkuu = False
    print("Hävisit pelin :(")
    lopetus_aika = time.time()
    koko_aika = lopetus_aika - aloitus_aika
    aika = datetime.datetime.now()
    print("Peli pelattiin ajassa: {:.2f} sekunttia".format(koko_aika))
    print("Peli pelattiin aikaan: " + str(aika))
    loukkis = "häviö"
    ajat_ja_voitto_tai_havio_tilastoihin()

def kasittele_hiiri(x, y, nappi, muokkausnappi):
    """
    Tätä funktiota kutsutaan, kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Sisältää eri vaihtoehdot kullekin napille (pelissä käytetään vain hiiren vasenta ja oikeaa).
    """
    global vuoro
    global aika
    global loukkis
    global pelijatkuu
    global koko_aika
    if pelijatkuu:
        sanakirja = {
            haravasto.HIIRI_VASEN: "vasen",
            haravasto.HIIRI_OIKEA: "oikea",
            haravasto.HIIRI_KESKI: "keski"
        }
        e = int(x / 40)
        f = int(y / 40)
        if nappi == haravasto.HIIRI_VASEN:
            if kentta[f][e] == "x":
                vuoro = vuoro + 1
                hiiren_vasenta_painetaan_miinan_kohdalla()
            elif kentta[f][e] == " ":
                vuoro = vuoro + 1
                tulvataytto(kentta, e, f)
                for k in range(tietoja_sanakirja["koko_y"]):
                    for l in range(tietoja_sanakirja["koko_x"]):
                        if kentta[k][l] == "0":
                            nakyva[k][l] = kentta[k][l]
                            nollan_tarkistaja(kentta)
            else:
                vuoro = vuoro + 1
                nakyva[f][e] = kentta[f][e]
        elif nappi == haravasto.HIIRI_OIKEA:
            if nakyva[f][e] == "f":
                nakyva[f][e] = " "
            else:
                nakyva[f][e] = "f"
        else:
            pass

        if voiton_tarkistus():
            pelijatkuu = False
            print("Jipii!!!!!")
            lopetus_aika = time.time()
            koko_aika = lopetus_aika - aloitus_aika
            aika = datetime.datetime.now()
            print("Peli pelattiin ajassa: {:.2f} sekuntia".format(koko_aika))
            print("Peli pelattiin aikaan: " + str(aika))
            loukkis = "voitto"
            ajat_ja_voitto_tai_havio_tilastoihin()

def numero_funktio(lista):
    """
    Laskee miinoja ympäriltä ja numeroita tulee. Hakee numeron kentta-listasta, 
    kun ruutu avataan, eli numero on "valmiina" siellä, se vain siirretään nakyva-listaan.
    """
    lkm = 0
    for y, y_sisalto in enumerate(lista):
        for x, x_sisalto in enumerate(y_sisalto):
            lkm = 0
            for i in range(-1, 2):
                y_koordinaatti = y + i
                if y_koordinaatti < 0:
                    continue
                for j in range(-1, 2):
                    x_koordinaatti = x + j
                    if x_koordinaatti < 0:
                        continue
                    try:
                        o = lista[y_koordinaatti][x_koordinaatti]
                    except:
                        pass
                    else:
                        if o == "x":
                            lkm = lkm + 1

            if lista[y][x] != "x" and lkm != 0:
                lista[y][x] = str(lkm)
    return lkm

def nollan_tarkistaja(lista):
    '''
    Avaa ruutuja nollien vierestä kun tulvatäyttöä käytetään.
    '''
    lkm = 0
    for y, y_sisalto in enumerate(lista):
        for x, x_sisalto in enumerate(y_sisalto):
            lkm = 0
            for i in range(-1, 2):
                y_koordinaatti = y + i
                if y_koordinaatti < 0:
                    continue
                for j in range(-1, 2):
                    x_koordinaatti = x + j
                    if x_koordinaatti < 0:
                        continue
                    try:
                        o = lista[y_koordinaatti][x_koordinaatti]
                    except:
                        pass
                    else:
                        if o == "0":
                            lkm = lkm + 1

            if lista[y][x] != "x" and lkm != 0:
                nakyva[y][x] = x_sisalto
    return lkm

def voiton_tarkistus():
    '''
    Suoritetaan aina, 
    kun pelaaja laittaa lipun tai avaa tyhjän 
    tai numeroidun ruudun.
    '''
    moka1 = False
    moka2 = False


    for y, rivi in enumerate(kentta):
        for x, merkki in enumerate(rivi):
            if merkki == "x":
                if nakyva[y][x] != "f":
                    moka1 = True


    for y, rivi in enumerate(kentta):
        for x, merkki in enumerate(rivi):
            if merkki != "x":
                if nakyva[y][x] == " ":
                    moka2 = True

    if moka1 and moka2:
        return False

    return True

def laske_tyhjat(x, y, lista):
    tyhja = " "
    tyhjat = []
    for rivi in range(y - 1, y + 2):
        for sarake in range(x - 1, x + 2):
            if rivi >= len(lista) or rivi < 0:
                pass
            elif sarake >= len(lista[0]) or sarake < 0:
                pass
            elif tyhja in lista[rivi][sarake] and (rivi != y or sarake != x):
                tyhjat.append((sarake, rivi))
            else:
                pass
    return tyhjat

def tulvataytto(lista, x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    Turvallinen alue tarkoittaa tässä tapauksessa aluetta, 
    jossa ei ole edes numeroita.
    """
    aloitus = [(x, y)]
    while aloitus:
        if lista[y][x] == "x":
            break
        x, y = aloitus.pop()
        lista[y][x] = "0"
        aloitus.extend((laske_tyhjat(x, y, lista)))

def aika_funktio():
    '''
    Alkaa mittamaan peliin kuluvaa aikaa.
    '''
    global aloitus_aika
    aloitus_aika = time.time()

def tilasto_funktio():
    '''
    Avaa tilastoja, jos käyttäjä haluaa niitä katsoa.
    '''
    with open("tiedosto.pringles") as tieto:
        for rivi in tieto.readlines():
            print(rivi)

def lopetus_funktio():
    '''
    Lopettaa hommat.
    '''
    pass

def ajat_ja_voitto_tai_havio_tilastoihin():
    '''
    Siirtää asioita tilastoihin kivasti.
    '''
    koko_aika_minuutteina = koko_aika / 60
    try:
        with open("tiedosto.pringles", "a") as kohde:
            kohde.write(str(koko_aika_minuutteina) + " minuuttia " + str(aika) + " " +
                        loukkis + " vuoroja oli " + str(vuoro) +
                        " " + str(tietoja_sanakirja["koko_x"]) + "X" +
                        str(tietoja_sanakirja["koko_y"]) +
                        " kokoisella kentällä miinoja oli " +
                        str(tietoja_sanakirja["miinat"]) + "\n")
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")


def piirra_kentta():
    '''
    Piirtää (näkyvän) kentän mainissa luotuun sopivan kokoiseen ikkunaan.
    '''
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(nakyva):
        for x, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, 40 * x, 40 * y)
    haravasto.piirra_ruudut()

def peli_funktio():
    '''
    Alkaa pyörittämään peliä, jos käyttäjä on sen valinnut.
    '''
    try:
        haravasto.lopeta()
    except:
        pass

    tee_asioita()
    global pelijatkuu
    pelijatkuu = True
    kentan_listan_luominen()
    nakyva_listan_luominen()
    for x in range(tietoja_sanakirja["koko_x"]):
        for y in range(tietoja_sanakirja["koko_y"]):
            jaljella.append((x, y))
    miinoita(kentta, jaljella, tietoja_sanakirja["miinat"])
    numero_funktio(kentta)
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(40 * tietoja_sanakirja["koko_x"], 40 * tietoja_sanakirja["koko_y"])
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    aika_funktio()
    haravasto.aloita()

def main():
    '''
    Koko homman yhteenlaittaminen.
    '''
    e = kysy_asioita()
    if e == "P":
        peli_funktio()
    elif e == "T":
        tilasto_funktio()
    elif e == "L":
        lopetus_funktio()
    else:
        pass

main()
