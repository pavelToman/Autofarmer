import copy
import random

#Vytvářím třídu Hrací Karty - Hkarty

class HKarty:
    """
    Hrací karty
    celkem 63ks
    typů 13

    kolo určuje ve kterém kole mohou hýt karty hrány
    Jméno a počet:
    svilec, plíseň, postřik, hnojka, pokos, zloděj po 8 kusech
    final solution, kamoš, varovaní, Samec po 3 kusech
    slunko, bouře, šťára po 1 kusu
    """
    def __init__(self, jmeno, pocet, kolo):
        self.jmeno = jmeno
        self.pocet = pocet
        self.kolo = kolo

#karty - list hracích karet, přidám do něj všech 63 hracích karet, balíček hracích karet
#z_karty list čísel(int) karet (pořadí v karty), které už byly taženy z balíčku karet(karty)  
karty = list() 
z_karty = list() 

#vytvářím jednotlivé typy hracích karet a ukládám je (několikrát podle self.pocet) do balíčku hracích karet(karty)
svilec = HKarty("svilec",8,[1,2])
for i in range(svilec.pocet):
    karty.append(svilec)
plisen = HKarty("plíseň",8,[1,2])
for i in range(plisen.pocet):
    karty.append(plisen)
postrik = HKarty("postřik",8,[1,2,3])
for i in range(postrik.pocet):
    karty.append(postrik)
hnojka = HKarty("hnojka",8,[1,2,3])
for i in range(hnojka.pocet):
    karty.append(hnojka)
pokos = HKarty("pokos",8,[1,2,3])
for i in range(pokos.pocet):
    karty.append(pokos)
zlodej = HKarty("zloděj",8,[1,2])
for i in range(zlodej.pocet):
    karty.append(zlodej)
final_sol = HKarty("final solution",3,[3])
for i in range(final_sol.pocet):
    karty.append(final_sol)
kamos = HKarty("kámoš",3,[3])
for i in range(kamos.pocet):
    karty.append(kamos)
varovani = HKarty("varovaní",3,[3])
for i in range(varovani.pocet):
    karty.append(varovani)
samec = HKarty("samec",3,[3])
for i in range(samec.pocet):
    karty.append(samec)
slunko = HKarty("slunko",1,[3])
karty.append(slunko)
boure = HKarty("boure",1,[3])
karty.append(boure)
stara = HKarty("stara",1,[3])
karty.append(stara)

#vytvářím třídu Hráč - Hrac
class Hrac:
    """
    hjmeno = jméno hráče, které si vybírá na začátku hry, str
    hporadi = zapíše se zde, kolik si hráč hodil na kostce v rozstřelu, int
    hzahrada = slovník, který obsahuje informace o hráčově zahradě, listy s klíči: "k"-čísla kytek v zahradě, "s"-čísla kytke se svilec, "p"-čísla kytek s plísní, "sam"-čísla kytek, které jsou samec, dict
    hkytek = slovník, kde je klíč číslo kytky a hodnota jsou body dané kytky, dict
    hsemen = počet semen, které může hráč zasadit, int
    hkarty = seznam hracích karet, které má hráč v ruce, list
    hbody = hráčovi body
    """
    def __init__(self, hjmeno, hporadi, hzahrada, hkytek, hsemen, hkarty, hbody):
        self.hjmeno = hjmeno
        self.hporadi = hporadi
        self.hkytek = hkytek
        self.hsemen = hsemen
        self.hkarty = hkarty
        self.hbody = hbody
        self.hzahrada = hzahrada
    
    #funkce pro určení, kolik jednotliví hráči hodili na kostce, aby určili, v jakém pořadí budou hrát. Zapíše se do Hrac(poradi)
    def hod_poradi(self):
        global hody #měním hody, takže global
        while True:
            hod = random.randint(1,6)
            if hod not in hody: #pokud už někdo hodil stejné číslo na kostce(číslo už je obsaženo v hody), tak hází znovu
                hody.append(hod) #hod přidám do hody, abych mohl ověřovat, zde už to někdo nehodil
                self.hporadi = hod
                print(self.hjmeno,"hodila/a",hod)
                break
            else:
                continue

    #funkce pro určení toho, kolik má jednotlivý hráč semen a kytek
    def pocet_kytek_semen(self):
        hod1 = random.randint(2,12)
        hod2 = random.randint(2,12)
        hod = [hod1, hod2]
        hod.sort() #první-menší číslo v hod (hod[0]) je teď počet zasazených kytek, druhé-větší je počet semen
        for i in range(1,hod[0]+1):
            self.hkytek[i]=40 #přidávám do přehledu hráčových kytek (slovníku hkytek) <číslo kytky>:<body>, ze začátku jsou body 40, od kytky 1 do kytky hod[0] včetně (takže v range+1) 
        self.hsemen = hod[1]-hod[0] #počet zbylých semen, která mohu použít ve hře
        for i in range(1,hod[0]+1): #do zahrady (listu "k" v self.hzahrada) přidávám všechny kytky
            self.hzahrada["k"].append(i)
        print(self.hjmeno,"získal", hod[1], "semen\n a z toho zasadil", hod[0], "kytek.\nZbývá ti", self.hsemen,"semínek!\n")

    #funkce pro vybrání jedné hrací karty z balíčku (list karty) a připsání do hráčových karet (self.hkarty)
    def dej_kartu(self):
        global z_karty #musím global jinak změny co provedu v z_karty se do ní nezapíší globálně (hodí to error), list karty neměním jen na něj odkazuji
        
        if (len(z_karty)==63): #kontrola, jestli už není balíček tažených karet (z_karty) plný, pokud ano, znovu zamíchat karty = vyprázdnit z_karty
            z_karty = list()
            
        while True:
            k1 = random.randint(0,62) #k1 je číslo karty z balíčku karty vybrané náhodně
            if k1 not in z_karty: #pokd není k1 v balíčku již tažených karet, tak ji tam dát
                z_karty.append(k1)
                break
            else: #pokud je k1 v z_karty, znamená to, že již byla tažena, takže se musí vybrat nová karta, která ještě tažena nebyla
                continue
        self.hkarty.append(karty[k1]) #do self.hkarty přidám vybranou kartu k1 z balíčku karet(karty)
        print("Tady máš:\n",  karty[k1].jmeno)
        

    #Zahoď kartu kterou nechceš- funkce pro výměnu hrací karty
    def zahod_kartu(self):
        for j, i in enumerate(self.hkarty):
	        print((j+1), i.jmeno)
        v = int(input("Kterou kartu měníš?\n"))
        del self.hkarty[(v-1)]
        print("Zbyli ti:")
        for b in self.hkarty:
            print(b.jmeno)
        print("\n")

    #definuj Hraj kartu
    def hraj_kartu(self):
        while True:   
            if (len(self.hkarty))==0: #pokud hráč nemá hrací kartu, tak už nehraje
                print("Nemáš už žádnou kartu, kterou bys zahrál! Končíš svoji hru.\n")
                break
            else:
                print("0 žádnou") 
                for i,j in enumerate(self.hkarty):
                    print(i+1, j.jmeno)
                a = (int(input("Kterou kartu chces zahrát?\n")))-1
                if a == -1: #pokud zadá hráč 0 tedy a=0-1, tak nechce hrát kartu 
                    print("Ok, končíš svoji hru!\n")
                    break
                else: #pokud hráč zvolí, kartu kterou chce zahrát, tak spustí zahrání karty (play Karta)
                    #Svilec
                    if hrac.hkarty[a] is svilec:
                        if kolo in svilec.kolo: #zkontroluj jestli je vhodné kolo pro svilec
                            hrac.pSvilec()
                            continue
                        else:
                            print("Svilec v tomto kole nelze zahrát!")
                            continue
                    #Plíseň
                    elif hrac.hkarty[a] is plisen:
                        if kolo in plisen.kolo:
                            hrac.pPlisen()
                            continue
                        else:
                            print("Plíseň v tomto kole nelze zahrát!")
                            continue
                    #Postřik
                    elif hrac.hkarty[a] is postrik:
                    #postřik lze hrát v jakémkoli kole, nemusím hlídat
                        hrac.pPostrik()
                        continue
                    #Hnojka
                    elif hrac.hkarty[a] is hnojka:
                        hrac.pHnojka()
                        continue
                    #Pokos
                    elif hrac.hkarty[a] is pokos:
                        hrac.pPokos()
                        continue
                    #Zloděj
                    elif hrac.hkarty[a] is zlodej:
                        if kolo in zlodej.kolo:
                            hrac.pZlodej()
                            continue
                        else:
                            print("Zloděje v tomto kole nelze zahrát!")
                            continue
                    #Final sol
                    elif hrac.hkarty[a] is final_sol:
                        if kolo in final_sol.kolo:
                            hrac.pFinal_sol()
                            continue
                        else:
                            print("Final solution v tomto kole nelze zahrát!")
                            continue
                    #Kámoš
                    elif hrac.hkarty[a] is kamos:
                        if kolo in kamos.kolo:
                            hrac.pKamos()
                            continue
                        else:
                            print("Kámoše v tomto kole nelze zahrát!")
                            continue
                    #Varování
                    elif hrac.hkarty[a] is varovani:
                        if kolo in varovani.kolo:
                            hrac.pVarovani()
                            continue
                        else:
                            print("Varování v tomto kole nelze zahrát!")
                            continue
                    #Samec
                    elif hrac.hkarty[a] is samec:
                        if kolo in samec.kolo:
                            hrac.pSamec()
                            continue
                        else:
                            print("Samce v tomto kole nelze zahrát!")
                            continue
                    #Slunko
                    elif hrac.hkarty[a] is slunko:
                        if kolo in slunko.kolo:
                            hrac.pSlunko()
                            continue
                        else:
                            print("Slunko v tomto kole nelze zahrát!")
                            continue
                    #Bouře
                    elif hrac.hkarty[a] is boure:
                        if kolo in boure.kolo:
                            hrac.pBoure()
                            continue
                        else:
                            print("Bouři v tomto kole nelze zahrát!")
                            continue
                    #Šťára
                    elif hrac.hkarty[a] is stara:
                        if kolo in stara.kolo:
                            hrac.pStara()
                            continue
                        else:
                            print("Šťáru v tomto kole nelze zahrát!")
                            continue
    
    #funkce skliď kytku - pro předčasné sklizení kytky pokosem
    def sklid_kytku(self):
        b=self.hkytek
        bb=self.hzahrada
        for j,k in b.items():#vypisuju jaké má hráč kytky
            print(j,k)
        c = int(input("Kterou kytku chceš sklidit?\n"))
        #ověření, zda kytka není napadena nemocí = nejde sklidit
        if c in bb["s"]:
            print(f"Nemůžeš sklidit kytku {c}!\nJe na ní svilec!\n")
            self.sklid_kytku()
        elif c in bb["p"]:
            print(f"Nemůžeš sklidit kytku {c}!\nJe na ní plíseň!\n")
            self.sklid_kytku()
        elif c in bb["sam"]:
            print(f"Nemůžeš sklidit kytku {c}!\nJe to samec!\n")
            self.sklid_kytku()
        else:
            if kolo==1 or kolo==2: # v 1. a 2. kole ztrácí předčasně sklizená kytka 20 bodů
                e = b[c]-20
                self.hbody += e
                print(f"Sklidil jsi kytku {c} a získla jsi za ni {e} bodů!")
                del b[c]
                bb["k"].remove(c)
            elif kolo==3:
                self.hbody += b[c]
                print(f"Sklidil jsi kytku {c} a získla jsi za ni {b[c]} bodů!")
                del b[c]
                bb["k"].remove(c)
            print("Aktuálně máš",self.hbody,"bodů!\n")

    #funkce pro šíření nemocí na konci hráčovi hry
    def sireni_nemoci(self):
        a = self.hzahrada
        b = self.hkytek
        if (len(a["p"]) != 0) or (len(a["s"]) != 0): #pokud máš v zahradě nemoc, tak působí
            print(self.hjmeno, "šíří se ti nemoci!")
        #první se šíří plísně - mají přednost, plíseň zabije kytku na které je a přemístí se na nejsilnější kytku
        if (len(a["p"]) != 0):
            y = a["p"]
            print(f"Na kytce {y} máš plíseň a ta se šíří!\n")
            for i in range(1, (len(a["p"]))+1): #zahrát plíseň tolikrát, kolikrát je v zahradě 
                c = a["p"][i-1]
                del b[c]
            for i in range(1, (len(a["p"]))+1):
                c = a["p"][0]
                b1 = copy.copy(b)
                while True:
                    d = max(b1, key=b1.get) #najdu nejsilnější kytku
                    if d in a["p"]:
                        del b1[d]
                        continue
                    else:
                        break
                print(f"Tvoji kytku {c} zabila plíseň a přeskočila ti na kytku {d}!\n")
                a["k"].remove(c)
                a["p"].remove(c)
                a["p"].append(d) #plíseň napadá nejsilnější kytku
        #jako druhé se šíří svilušky - zůstanou na kytce a dají -20 bodů nejsilnější kytce v zahradě
        if (len(a["s"]) != 0):
            x = a["s"]
            print(f"Na kytce {x} máš svilec a to je sviňa!\n")
            for i in range(1, (len(a["s"]))+1): #zahrát tolikrát, kolikrát je svilec v zahradě   
                c = max(b, key=b.get)
                b[c] -= 20
                print(f"Tvoje kytka {c} dostala od svilec -20 bodů!\n")
                self.check_kytky() #zkus jestli kytka neumřela
                
        
    #funkce pro zjištění, jestli není kytka mrtvá = má 0 a méně bodů
    def check_kytky(self):
        sh = self.hkytek
        mk = list()
        for i in sh:
            if sh.get(i) <= 0:
                print(f"Umřela ti kytka {i}!\n")
                mk.append(i)
        for i in mk:
            del self.hkytek[i] 
            self.hzahrada["k"].remove(i)
            if i in self.hzahrada["p"]:
                self.hzahrada["p"].remove(i)
            if i in self.hzahrada["s"]:
                self.hzahrada["s"].remove(i)
            if i in self.hzahrada["sam"]:
                self.hzahrada["sam"].remove(i)              

    #funkce pro zahrání kola hry
    def hrej_kolo(self):
        
        #1-1-1: Hráč si bere 3 karty z balíčku hracích karet
        print(f"Haje se {kolo}. kolo a hraje hráč {self.hjmeno}\n")
        print("Hráč", self.hjmeno, "si bere 3 hrací karty")
        for i in range(3): #1.hráč (shraci[0]) dostává 3 hrací karty a ukládá je do self.hkarty, přidají se i do z_karty (tažené karty)  
            self.dej_kartu()
        print(f"\n{self.hjmeno} máš tyto karty:")    
        for i in self.hkarty:
           print(i.jmeno)

        #1-1-2: Zahodí (chce vyměnit) 0 až 3 karty
        vk = int(input("Kolik měníš karet?\n"))
        if vk == 0: #pokud nechce vyměnit karty
            pass
        elif vk > 3: #pokud chce vyměnit víc než 3 karty, nemůže
            print("Můžeš vyměnit max 3 karty!\n")
            vk = 3
            if vk == len(self.hkarty): 
                print("Měníš všechny 3 karty!\n")
                self.hkarty = list()
            else:
                for i in range(vk):
                    self.zahod_kartu()
        elif vk == len(self.hkarty): #pokud jsou to všechny karty v hráčově ruce
            print("Měníš všechny 3 karty!\n")
            self.hkarty = list()
        else:
            for i in range(vk):
                self.zahod_kartu() 

        #1-1-3: Hráč si bere tolik karet, kolik zahodil
        for i in range(vk):
            self.dej_kartu()
        print(self.hjmeno,"máš tyto hrací karty:")    
        for i in self.hkarty:
            print(i.jmeno)

        #1-1-4: Hráč hraje karty
        self.hraj_kartu()

        #1-1-5: Šíření nemocí na hráčově zahradě
        self.sireni_nemoci()

        #1-1-6: Print aktuální stav
        for hrac in shraci:
            print(hrac.hjmeno)
            print(hrac.hzahrada)
            print(hrac.hkytek)
            print("Body:", hrac.hbody)
            print("Semena:", hrac.hsemen)
            print("\n")

#Definice zahrání hracích karet - play Karty
    #play Svilec
    def pSvilec(self):
        #vyber protihráče hráče, kterému chceš dát svilec
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self) #mažu hrajícího hráče ze seznamu
            ph=shraci1[0]
            phrac = shraci1[0].hkytek #ukládám druhéhé hráče a jeho kytky do phrac
            phz = shraci1[0].hzahrada #ukládám ProtiHráčovuZahradu do phz
        else: #pokud hraje více než 2 hráči, tak vyber který protihráč dostane svilec
            shraci1 = copy.copy(shraci) #okopíruji shraci, protože ho nechci měnit globálně ale teď to potřebuju
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše jména hráčů v pořadí od 1 (j+1)
	                print((j+1), i.hjmeno) 
            a = (int(input("Kterému hráči chceš dát svilec?\n")))-1
            ph = shraci1[a] #vybranemu protihráči(ph) ukladám kytky do phrac, zahradu do phz
            phrac = shraci1[a].hkytek 
            phz = shraci1[a].hzahrada
        #dej vybranému protihráči na kytku svilec 
        for j,k in phrac.items():#vypisuju jaké má vybraný protihráč kytky
            print(j, k)
        b = int(input("Na kterou kytku chceš dát svilec?\n")) #vybírám kartu na kterou dám svilec  
        if b in phz["p"] or b in phz["s"]: #pokud je na kytce nemoc, tak tam další dát nemohu
            print("Na této kytce už nemoc je, vyber jinou!")
            self.pSvilec()
        else:
            phrac[b]-=20 #dávám na vybranou kytku -20
            phz["s"].append(b) #do protihráčovi zahrady vkládám kytku napadenou svilušama
            ph.check_kytky() #zkouším, jestli mu kytka neumřela
            (self.hkarty).remove(svilec) #odebrat svilec z ruky hráče
        
    #play Plisen
    def pPlisen(self):
        #vyber hráče, kterému chceš dát plisen
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím shraci copy.copy do shraci1, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phrac = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j,i in enumerate(shraci1): #vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš dát plíseň?\n")))-1 
            phrac = shraci1[a].hkytek #vybranemu protihraci ukladám hkytek do phrac, hzahrada do phz
            phz = shraci1[a].hzahrada
        #dej mu na kytku plíseň
        for j,k in phrac.items():#vypisuju jaké má vybraný hráč kytky
            print(j,k)
        b = int(input("Na kterou kytku chceš dát plíseň?\n")) #vybírám kartu na kterou dám plíseň
        if b in phz["p"] or b in phz["s"]: #pokud je kytka nemocná, nemůžu sem plíseň dát
            print("Na této kytce už nemoc je, vyber jinou!")
            hrac.pPlisen()
        else:
            phz["p"].append(b) #do zahrady vkládám kytku napadenou plísní
            (self.hkarty).remove(plisen) #odebrat plíseň z ruky hráče

    #play Postřik
    def pPostrik(self):
        while True:
            hrac = self.hzahrada #ukládám hráčovu pzahrada do hrac
            if ("s" in hrac.keys()) and (len(hrac["s"])!=0): #pokud má v hzahrada nějáké svilec ("s" existuje and "s" není prázdné), tak vypíše "s", tedy čísla kytek na kterých je svilec
                print("Svilec máš na:")
                for j in hrac["s"]:#vypíše pod sebou čísla kytek, které mají svilec
                    print(j)
            if ("p" in hrac.keys()) and (len(hrac["p"])!=0): #pokud má nějáká kytky plísen (něco je v "p") and "p" není prázdné
                print("Plíseň máš na:")
                for j in hrac["p"]: #tak vypíše kytky s plísní pod sebe
                    print(j)
            if (len(hrac["s"])==0) and (len(hrac["p"])==0):
                print("Nemáš ani svilec ani plíseň, seš slepý?")
                break       
            a = int(input("Na kterou kytku chceš dát postřik?\n")) # do a se zapíše číslo kytky, kterou chce postříkat
            if a in hrac["p"]:# pokud je číslo kytky v "p", tedy má plíseň, tak ho z tohoto listu smaže
                hrac["p"].remove(a)
                (self.hkarty).remove(postrik)
                break
            else: #pokud a není v "p" tak je tedy v "s" a smaže a v listu "s", tedy odstraní svilec
                hrac["s"].remove(a)
                (self.hkarty).remove(postrik)
                break
        

    #definuj play Hnojka - dodělat - pokud nemám kytku, tak nemůžu zahnojit
    def pHnojka(self):
        #zasadit nebo zahnojit
        print("1  Zasadit semínko\n",
            "2  Zahnojit kytku")
        a = int(input("Co chceš s hnojkou dělat?\n"))
        if a==1:
            #počekovat jestli mám semeno
            if self.hsemen > 0:
                print(f"Máš {self.hsemen} semínek")
                if kolo==1 or kolo==2:
                    #přidat další kytku do hkytek 
                    b = self.hkytek
                    bb= self.hzahrada
                    c = bb["k"]
                    c.sort()
                    d = c[-1]
                    b[d+1]=40
                    c.append(d+1)
                    self.hsemen-=1
                    print("Zasazeno!\nMáš",len(c),"kytek a", self.hsemen,"semínek!")
                    (self.hkarty).remove(hnojka)
                elif kolo==3: #pokud je 3. kolo tak jen kytka s 20 body
                    b = self.hkytek
                    bb= self.hzahrada
                    c = bb["k"]
                    c.sort()
                    d = c[-1]
                    b[d+1]=20
                    c.append(d+1)
                    self.hsemen-=1
                    print("Zasazeno, ale jen s 20 body!\nMáš",len(c),"kytek a", self.hsemen,"semínek!")
                    (self.hkarty).remove(hnojka)
            else:
                print("Nemáš semínko!")
                self.pHnojka()    
        elif a==2:
            b = self.hkytek
            for j,k in b.items():#vypisuju jaké má hráč kytky
                print(j,k)
            c = int(input("Kterou kytku chceš zahnojit?\n"))
            b[c]+=20
            print("Kytka je zahnojená, máš na ni +20 bodů!\n")
            print(b[c])
            (self.hkarty).remove(hnojka)
    
    #Definuj play Pokos
    def pPokos(self):
        if len(self.hzahrada["k"])==0:
            print("Nemáš kytky, co bys kosil?\n")
        else:    
            print("1 Zab jednu kytku\n",
                "2 Skliď až 2 kytky\n")
            a = int(input("Co chceš s pokosem dělat?\n"))
            #1 zab kytku
            if a==1:
                b=self.hkytek
                bb=self.hzahrada
                for j,k in b.items():#vypisuju jaké má hráč kytky
                    print(j,k)
                c = int(input("Kterou kytku chceš zabít?\n"))
                del b[c]
                bb["k"].remove(c)
                if c in bb["s"]:
                    bb["s"].remove(c)
                if c in bb["p"]:
                    bb["p"].remove(c)
                if c in bb["sam"]:
                    bb["sam"].remove(c)
                print(f"Zabil sis kytku {c}!")
                (self.hkarty).remove(pokos)
            if a==2:
                #pokud mám víc pokosů než 2xkytek, tak se neptat kterou sklidit
                pp = 0
                p=0
                zk = copy.copy(self.hzahrada["k"])
                for i in self.hzahrada["p"]:
                    zk.remove(i)
                for i in self.hzahrada["s"]:
                    zk.remove(i)
                for i in self.hzahrada["sam"]:
                    zk.remove(i)

                for i in self.hkarty:
                    if i==pokos:
                        p += 1
                        pp += 2
                if len(zk)<=pp:
                    o = int(input("Chceš sklidit všechny kytky v zahradě?\n1 Ano\n2 Ne\n"))
                    if o==1:
                        if kolo==1 or kolo==2:
                            for i in zk:
                                f = (self.hkytek[i])-20
                                self.hbody += f
                                print(f"Sklidil jsi kytku {i} a získla jsi za ni {f} bodů!")
                                self.hzahrada["k"].remove(i)
                                del self.hkytek[i]
                        if kolo==3:
                            for i in zk:
                                f = (self.hkytek[i])
                                if len(self.hzahrada["sam"])>0:
                                    f = f/2
                                    self.hbody += f
                                else:
                                     self.hbody += f
                                print(f"Sklidil jsi kytku {i} a získla jsi za ni {f} bodů!")
                                self.hzahrada["k"].remove(i)
                                del self.hkytek[i]
                        for i in range(p):
                            self.hkarty.remove(pokos)
                    if o==2:
                        pass
                else:
                    self.sklid_kytku()
                    if len(self.hzahrada["k"])==0:
                        print("Další kytku už nemáš...\n")
                        (self.hkarty).remove(pokos)
                    else:
                        o = int(input("Chceš sklidit další kytku?\n1 Ano\n2 Ne\n"))
                        if o==1:
                            self.sklid_kytku()
                        elif o==2:
                            pass
                        (self.hkarty).remove(pokos)
    
    #Definuj play Zloděj
    def pZlodej(self):
        #vyberu hráče
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phrac = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš vzít kytku?\n")))-1
            phrac = shraci1[a].hkytek #vybranemu hraci ukladám hkytek do phrac
            phz = shraci1[a].hzahrada #vybranému ukládám hzahrada do phz (proti_hráč_zahrada)
        #vyberu kytku
        for j,k in phrac.items():#vypisuju jaké má vybraný hráč kytky
            print(j,k)
        a = int(input("Kterou kytku bys chtěl ukrást?\n"))#vybírám kartu na kterou dám plíseň
        #dám si kytku k sobě a protihráči smazat
        b = self.hkytek
        bb= self.hzahrada
        c = bb["k"]
        c.sort()
        if len(c) == 0:
            c.append(1)
            b[1]=phrac[a]
        else:
            d = c[-1]
            b[d+1]= phrac[a]#rovná se hodnotě bodů co měl ten protihráč
            c.append(d+1)        
        del phrac[a]
        phz["k"].remove(a)
        if a in phz["s"]:
            phz["s"].remove(a)
            bb["s"].append(a)   
        if a in phz["p"]:
            phz["p"].remove(a)
            bb["p"].append(a)
       
        (self.hkarty).remove(zlodej)

    #Definuj play Final solutin
    def pFinal_sol(self):
        if len(self.hkytek) == 0:
            print("Nemáš kytky, ani final solution tě nezachrání!\n")
            self.hraj_kartu
        else:
            a = self.hkytek
            for b in a:
                a[b]+=10
                print(b,a[b])
            print("Dal jsi si final solution na všechny tvé kytky a ty dostávájí +10 bodů!\n")
            (self.hkarty).remove(final_sol)

    #Definuj play Kámoš
    def pKamos(self):#stejné jak zloděj 
        #vyberu hráče
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phrac = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš vzít kytku?\n")))-1
            phrac = shraci1[a].hkytek #vybranemu hraci ukladám hkytek do phrac
            phz = shraci1[a].hzahrada #vybranému ukládám hzahrada do phz (proti_hráč_zahrada)
        #vyberu kytku
        for j,k in phrac.items():#vypisuju jaké má vybraný hráč kytky
            print(j,k)
        a = int(input("Kterou kytku bys chtěl ukrást?\n"))#vybírám kartu na kterou dám plíseň
        #dám si kytku k sobě a rotihráči smazat
        b = self.hkytek
        bb= self.hzahrada
        c = bb["k"]
        c.sort()
        d = c[-1]
        b[d+1]= phrac[a]#rovná se hodnotě bodů co měl ten protihráč
        c.append(d+1)
        
        del phrac[a]
        phz["k"].remove(a)

        if a in phz["s"]:
            phz["s"].remove(a)
            bb["s"].append(a)
        if a in phz["p"]:
            phz["p"].remove(a)
            bb["p"].append(a)

        (self.hkarty).remove(kamos)

    #Definuj play Varování
    def pVarovani(self):
        #vyberu hráče
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phrac = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš zabít kytku?\n")))-1
            phrac = shraci1[a].hkytek #vybranemu hraci ukladám hkytek do phrac
            phz = shraci1[a].hzahrada #vybranému ukládám hzahrada do phz (proti_hráč_zahrada)
        #pokud nemá protihráč kytky - tak hrát znova
        if len(phz) == 0:
            print("Protihráč nemá žádnou kytku, tak mu těžko nějakou zničíš!\n")
            self.hraj_kartu
        else:
            #vyberu kytku
            for j,k in phrac.items():#vypisuju jaké má vybraný hráč kytky
                print(j,k)
            a = int(input("Kterou kytku bys chtěl zabít?\n"))
            #smazat protihráči kytku
            del phrac[a]
            phz["k"].remove(a)
            
            if a in phz["s"]:
                phz["s"].remove(a)
            if a in phz["p"]:
                phz["p"].remove(a)

            (self.hkarty).remove(varovani)

    #Definuj play Samec
    def pSamec(self):
        #vyber hráče, kterému chceš dát samec
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phrac = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš dát samce?\n")))-1 #ptám se na číslo hráče, kterému chceš dát plíseň
            phrac = shraci1[a].hkytek #vybranemu hraci ukladám hkytky do hrac
            phz = shraci1[a].hzahrada
        #dej mu na ni samca
        for j,k in phrac.items():#vypisuju jaké má vybraný hráč kytky
            print(j,k)
        b = int(input("Na kterou kytku chceš dát samce?\n"))
        
        if b not in phz["k"]:
            print("Takovou kytku v zahradě nemá, vyber jinou!\n")
            hrac.pSamec()
        elif b in phz["sam"]:
            print("Tato kytka už samec je, vyber jinou!")
            hrac.pSamec()
        else:
            phz["sam"].append(b) 
            (self.hkarty).remove(samec) #odebrat plíseň z ruky hráče
    
    #Definuj play Slunko
    def pSlunko(self):
        
        for b in shraci:
            print(b.hjmeno)
            for c in b.hkytek:
                b.hkytek[c]+=10
                print(c,b.hkytek[c])
        print("Dal jsi Slunko a všichni hráči dostali na všechny své kytky +10 bodů!\n")
        (self.hkarty).remove(slunko)

    #Definuj play Bouře
    def pBoure(self):
        for b in shraci:
            print(b.hjmeno)
            for c in b.hkytek:
                b.hkytek[c]-=20
            # print(c,b.hkytek[c]) nefunguje mi toto
            b.check_kytky()
        print("Dal jsi Bouři a všichni hráči ztratili na všech svých kytkách -20 bodů!\n")

        (self.hkarty).remove(boure)

    #Definuj play Šťára
    def pStara(self):
         #vyber hráče, kterému chceš dát šťáru
        if len(shraci)==2:#pokud hrají jen 2 tak toho druhého vybrat do hrac dat jeho hkytky
            shraci1 = copy.copy(shraci) #musím copy.copy shraci, jinak se mi změní shraci!!!
            shraci1.remove(self)
            phr = shraci1[0].hkytek
            phz = shraci1[0].hzahrada
        else:
            shraci1 = copy.copy(shraci)
            shraci1.remove(self)
            for j, i in enumerate(shraci1):#vypíše hráče jmény s pořadím od 1 (j+1)
	            print((j+1), i.hjmeno)
            a = (int(input("Kterému hráči chceš dát šťáru?\n")))-1 #ptám se na číslo hráče, kterému chceš dát plíseň
            phr = shraci1[a].hkytek #vybranemu hraci ukladám hkytky do hrac
            phz = shraci1[a].hzahrada
        
        if len(phz["k"])<6:
            print("Tento hráč má málo kytek na šťáru!\n")
            z=int(input("Chceš hrát stále šťáru?\n1 Ano\n2 Ne\n"))
            if z == 1:
                self.pStara()
            elif z == 2:
                pass
        else:
            phr.clear() #vymazat kytky z hkytek
            for a in phz: #vymazat všechny listy v pzahrada
                phz[a]=[]
            (self.hkarty).remove(stara)

#0-0: Číslo hry

#0-1: Počet hráčů

while True:
    pocet_hracu = input("Kolik lidí hraje? Může hrát 2 - 5 hráčů!\n") #ptám se kolik bude hrát lidí (2-5)
    try:
        pocet_hracu = int(pocet_hracu) #pocet_hracu = počet hráčů, je int s počtem hráčů
    except:
        print("zadej čílso!!!")
        continue
    if pocet_hracu > 1 and pocet_hracu < 6:
        break
    else:
        print("špatně zadaný počet!!!")
        continue
print(f"Počet lidí ve hře je {pocet_hracu}")

#0-2: Vytvoření hráčů a jejich jména Hrac.hjmeno
#(hjmeno, hporadi, hzahrada, hkytek, hsemen, hkarty, hbody):

hraci=list() #vytvořím list hraci, kde mám uložené všechny Hrace
for i in range(1,(pocet_hracu+1)): #musím počítat od jedné, jinak budu mít navíc hráče 0
    hrac = Hrac(input(f"Jméno hráče {i}?\n"), 0, {"k":[],"s":[],"p":[],"sam":[]}, {}, 0, [], 0) #každý hráč zadá své jméno, uloženo do self.hjmeno
    hraci.append(hrac)
    print(f"Jméno {i}. hráče je", hrac.hjmeno)

#0-3: Pořadí hráčů
global hody 
hody = list() #vytvářím list hodů pro hod_poradi
for hrac in hraci:
    hrac.hod_poradi()#hod na kostce ze zapsal do Hrac.hporadi

shraci = list() #list pro uložení Hračů podle toho, kolik hodili (Hrac.hporadi)

for hrac in hraci:#Hrace z hraci přidám do shraci (seřazení hráči) a seřadím je tam podle Hrac.hporadi
    shraci.append(hrac)
    shraci = sorted(shraci, key=lambda hrac: hrac.hporadi, reverse=True)#reverse, protože začíná ten s nejvišším hozeným číslem

for i in range(1,(pocet_hracu+1)): #popořadě vypíšu který hráč hraje první a dále
    print(f"{i}. hraje", shraci[i-1].hjmeno)

#0-4: Házení počet semen a kytek

for hrac in shraci: #hodí si každý o počet semen a kytek, uloženo v Hrac.hkytek jako dict
    hrac.pocet_kytek_semen()
    #print(hrac.hkytek)

#HRA

for kolo1 in range(1,4):
    kolo = kolo1
    print("Začíná", kolo1,". kolo")
    for hrac in shraci:
        hrac.hrej_kolo()

#Konec hry:
#přepočítat kytky na body u každého hráče
for hrac in shraci:
    a = hrac.hkytek
    #odstranit nemocné a samce
    if (len(hrac.hzahrada["s"])>0):
        for i in hrac.hzahrada["s"]:
            del a[i]
    if (len(hrac.hzahrada["p"])>0):
        for i in hrac.hzahrada["p"]:
            del a[i]
    if (len(hrac.hzahrada["sam"])>0):
        for i in hrac.hzahrada["sam"]:
            del a[i]
    b = sum(a.values())
    if (len(hrac.hzahrada["sam"])>0):
        b = b/2
    hrac.hbody += b
#seřadit hráče v shraci podle počtu bodů
shraci.sort(key=lambda shraci: shraci.hbody, reverse = True)
for c in range(1, len(shraci)+1):
    print(f"{c}. je hráč {shraci[c-1].hjmeno}, který získal {shraci[c-1].hbody} bodů!\n")


##MAM: asi se špatně tahají hrací karty z balíku - v jedné hře došlo 2x slunko
##ASI MAM: pokos všech nefunguje - když dám sklidit všechny tak to sklidilo jen 1 ze 2

##MAM: stara mega error: line 753, vypíše milionkrát Tento hráč má málo kytek na šťáru! a dá RecursionError: maximum recursion depth exceeded while calling a Python object
#ASI MAM: bouře nebere kytkám body, ale nepadá
##MAM: při výměně karet, když má hráč stejně karet jako mění, tak se ho neptat které mění
##pokud mám víc pokosu než kytek tak se neptat kterou sklidit

##MAM: štára- vymaže se pouze hzahrada "k", ale ne hkytek
##MAM: při pokosu když vyberu kytku, kterou sklidit, tak se to nesekne ale nedá mi to body ani to tu kytku nesklidi
##ASI MAM:Bouře Error: line 733, in pBoure, for c in b: TypeError: 'Hrac' object is not iterable

##opravit šíření nemocí
    ## ASI MAM:když se šíří svilec tak se pak už nešíří plíseň
    #?toto mi vyskočilo: Tvoje kytka -18 dostala od svilec -20 bodů!
    ##ASI MAM: line 300, in sireni_nemoci
        ##print(f"Tvoje kytka {b[c]} zabila plíseň a přeskočila ti na kytku {d}!\n")KeyError: 1
##ASI MAM:opravit výměnu karet, když vyměním 3 tak mě taky nechat vybrat, protože v dalších kolech můžu mít více jak 3
##ASI MAM:opravit výpočet bodů na koci - musím oddělat napadené kytky
##MAM: u final solution když nemám kytky tak nic nehnojit
##ASI MAM:opravit konec hry (shraci.sort(key=shraci.hbody))
##MAM: změnit získal x semen a má zasazeno y kytek - na kolik má kytek a kolik mu zbylo semen
#ASI MAM:dodělat samec a půlka bodů
## ASI MAM:chyba ve hnojce: když dám zasadit semínko a nemám ho a pak dám zahnojit tak se to nějak posere: 
#?V posledním kole (u 1. hráče, ale možná ne jenom), když dám že už nechci hrát kartu, tak mi to stejně nabídne jestli nechci zahrát kartu
##MAM: opravit varování - pokud protihráč nemá už karty, tak poslat do háje, teď to nabízí zabít z prázdého seznamu kytek protihráče
##MAMopravit Bouře: line 722, in pBoure
    ##a = shraci.hkytek
    ##AttributeError: 'list' object has no attribute 'hkytek'

#Na kytce [1, 2] máš plíseň a ta se šíří!
#Tvoji kytku 1 zabila plíseň a přeskočila ti na kytku 3!
#Tvoji kytku 3 zabila plíseň a přeskočila ti na kytku 4!

#{'k': [2, 4, 5, 6], 's': [], 'p': [2, 4], 'sam': []}
#{3: 40, 4: 40, 5: 40, 6: 40}