import pickle
import datetime
import sys
from PIL import Image
import glob
import os
import random
from rich.console import Console
from rich.theme import Theme
costum_theme = Theme({"com": "cyan"})
console = Console(theme = costum_theme)
from rich.layout import Layout
layout = Layout()
from rich.panel import Panel
from rich.text import Text

class Einstellungen():
    def __init__(self):
        self.learn_cards_num = 10
        self.compare = False

class Karteikarte():
    def __init__(self, question, answer, picture, q_picture):
        self.question = question
        self.q_picture = q_picture
        self.answer = answer
        self.picture = picture
        self.created = datetime.date.today()
        self.correct = 0
        self.next_time = datetime.date.today()

class Neue_Karteikarten():
    def __init__(self):
        self.settings_file()
        self.kk_list = self.get_karteikarten()
        self.use_kk()
        self.choose_kk = 'null'

    def settings_file(self):
        settings_file = 'settings/settings.pkl'
        if os.path.isfile(settings_file):
            pass
        else:
            with open(settings_file, 'w') as f:
                pass
    
    def get_karteikarten(self):
        kk_list = glob.glob(os.path.join('*.pkl'))
        return kk_list
    
    def use_kk(self):
        self.kk_list = self.get_karteikarten()
        header = "\n---=: Karteikarten :=---\n"+"----"+chr(0x1F393)+" ----" +chr(0x1F393)+" ----"+chr(0x1F393)+" ---"
        header_panel = Panel(Text(header), title = "by majukano", style="green", width=50, height = 5, padding=(0,0,0,0), expand = False, border_style = "green", title_align = "left")
        console.print(header_panel)
        print(datetime.date.today())
        if len(self.kk_list) < 1:
            print('kein Karteikasten gefunden')
            print('Neu anlegen? j/n (beenden mit ende)')
            user_input = input('> ')
            print()
            if user_input == 'j':
                self.new_kk()
            elif user_input == 'ende':
                sys.exit()
        else:
            self.choose_kk()
    
    def choose_kk(self):
        print('Bitte Karteikasten wählen oder neu anlegen:')
        n = 0
        for kk in self.kk_list:
            n+=1
            console.print('[com]{}[/] - {}'.format(n, kk))
        test = True
        while test:
            test = False
            console.print('Nummer eingeben ([com]neu[/] - neu Anlegen, [com]del[/] - löschen, [com]ende[/] - beenden):')
            user_input = input('> ')
            print()
            if user_input == 'abort!':
                print('Abbruch')
                self.use_kk()
            elif user_input == 'neu':
                self.new_kk()
            elif user_input == 'del':
                self.del_kk()
            elif user_input == 'ende':
                test = True
                break
            else: 
                try:
                    user_input = int(user_input)
                    choosen_kk = self.kk_list[int(user_input)-1]
                    break
                except:
                    print('keine gültige Nummer')
                    print('Abbrechen mit abort!')
                    test = True
        if test:
            sys.exit()
        print('{} gewählt'.format(choosen_kk))
        self.start_kk(choosen_kk)
    
    def start_kk(self, choosen_kk):
        self.choosen_kk = choosen_kk
        Main_Karteikarten(choosen_kk)
      
    def new_kk(self):
        console.print('Name des neuen Karteikastens eingeben: (Abbrechen = [com]abort![/])')
        kk_name = input('> ')
        print()
        if kk_name == 'abort!':
            self.use_kk()
        else:
            kk_name = kk_name+'.pkl'
            with open(kk_name, 'w') as f:
                pass
            print('Karteikasten {} erstellt'.format(kk_name))
            self.use_kk()

    def del_kk(self):
        n = 0
        for kk in self.kk_list:
            n+=1
            print('{} - {}'.format(n, kk))
        test = True
        while test:
            test = False
            console.print('Nummer des Karteikasten zum löschen eingeben: (Abbrechen = [com]abort![/])')
            user_input_num = input('> ')
            print()
            if user_input_num == 'abort!':
                print('Abbruch')
                break
            else:
                try:
                    self.kk_list[int(user_input_num)-1]
                except:
                    print('keine gültige Nummer')
                    test = True
            
            if test == False:
                test_2 = True
                while test_2:
                    test_2 = False            
                    console.print('Es soll sicher Karteikasten [red]{}[/] gelöscht werden? [com]j[/]/[com]n[/]'.format(self.kk_list[int(user_input_num)-1]))
                    user_input = input('> ')
                    print()
                    if user_input == 'j':
                            delate_kk = self.kk_list[int(user_input_num)-1]
                            os.remove(delate_kk)
                            print('{} gelöscht'.format(delate_kk))
                    elif user_input == 'n':
                        break
                    else:
                        print('Eingabe nicht erkannt')
                        test_2 = True
                if test_2 == False:
                    break
        self.use_kk()
        
class Main_Karteikarten():
    def __init__(self, choosen_kk):
        self.choosen_kk = choosen_kk
        self.KK = []
        self.load_kk()
        self.main()
    
    def load_kk(self):
        try: 
            with open(self.choosen_kk, 'rb') as kk:
                self.KK = pickle.load(kk)
        except:
            print('no data found')
            self.main()
            
    def save_kk(self):
        with open(self.choosen_kk, 'wb') as kk:
                pickle.dump(self.KK, kk, pickle.HIGHEST_PROTOCOL)
 
    def help(self):
        console.print('[com]ende[/]: Beenden des Programms')
        console.print('[com]start[/]: Starten der Karteikartenabfrage')
        console.print('[com]neu[/]: Neue Karteikarte anlegen')
        console.print('[com]info[/]: Informationen zu angelgten Karteikarten und Karteikarten bearbeiten')
        console.print('[com]einstellungen[/]: Einstellungen vornehmen')
        console.print('[com]zurück[/]: Zurück zur Karteikasten Auswahl')
        self.main()
          
    def main(self):
        console.print('Eingabe: [com]hilfe[/], [com]ende[/], [com]start[/], [com]neu[/], [com]info[/], [com]einstellungen[/], [com]zurück[/]')
        user_input = input('> ')
        print()
        if user_input == 'hilfe':
            self.help()
        elif user_input == 'ende':
            sys.exit()
        elif user_input == 'neu':
            self.new_kk()
        elif user_input == 'start':
            self.start_kk()
        elif user_input == 'info':
            self.info_kk()
        elif user_input == 'einstellungen':
            self.setup_kk()
        elif user_input == 'zurück':
           K1 = Neue_Karteikarten()    
        else:
            print('Eingabe nicht erkannt')
            self.main()

    def setup_kk(self):
        pass

    def info_kk(self):
        print('Anzahl der Karteikarten: {}'.format(len(self.KK)))
        next_time = []
        for card in set(self.KK):
            next_time.append(card.next_time)
        for time in set(next_time):
            number = next_time.count(time)
            print('{}: {}'.format(time, number))
        if len(self.KK) != 0:
            change = True
            while change:
                console.print('Karte bearbeiten? [com]j[/]/[com]n[/]')
                user_input = input('> ')
                print()
                if user_input == 'j':
                    print('Karteikartennummer?')
                    test = True
                    while test:
                        test = False
                        user_input = input ('> ')
                        if user_input == 'abort!':
                            test = True
                            break
                        try:
                            user_input = int(user_input)-1
                            break
                        except:
                            print('keine oder falsche Kartenzahl eingegeben')
                            print('Abbrechen mit - abort!')
                            test = True
                    if test:
                        break
                    else:
                        self.print_card(user_input)
                        self.correct_question(self.KK[user_input])
                else:
                    break
        self.main()
    
    def print_card(self, number):
        print(self.KK[number].question)
        print(self.KK[number].answer)
        print(self.KK[number].picture)
        try:
            print(self.KK[number].q_picture)
        except:
            print("kein Bild zur Frage evtl. eine alte Karte")
        print(self.KK[number].correct)
        print(self.KK[number].next_time)
    
    def new_kk(self):
        console.print('Abbrechen mit [com]abort![/]')
        print('Frage eingeben:')
        input_question = input('> ')
        print()
        if input_question == 'abort!':
            self.main()
        else:
            question = input_question
        # pictur to question
        print('Falls ein Bild zur Frage vorhanden ist, Name eingeben: name.xxx:')
        print('Bild mit entsprechendem Namen bitte unter Ordner - picture - speichern')
        input_q_picture = input('> ')
        print()
        if input_q_picture == 'abort!':
            self.main()
        else:
            q_picture = input_q_picture
        print('Antwort eingeben:')
        input_answer = input('> ')
        if input_answer == 'abort!':
            self.main()
        else:
            answer = input_answer
        print('Falls Bild zur Antwort vorhanden ist, Name eingeben: name.xxx')
        print('Bild mit entsprechendem Namen bitte unter Ordner - picture - speichern')
        input_picture = input('> ')
        print()
        if input_picture == 'abort!':
            self.main()
        else:
            picture = input_picture
        print('Zusammenfassung:')
        print('Frage: {}'.format(question))
        print('Bild zur Frage: {}'.format(q_picture))
        print('Antwort: {}'.format(answer))
        print('Bild zur Antwort: {}'.format(picture))
        console.print('Speichern? - [com]j[/]/[com]n[/] - ([com]abort![/])')
        save = input('> ')
        print()
        if save == 'abort!':
            self.main()
        elif save == 'j':
            self.creat_kk(question, answer, picture, q_picture)
        elif save == 'n':
            self.new_kk()
        
    def creat_kk(self, question, answer, picture, q_picture):
        KK = Karteikarte(question, answer, picture, q_picture)
        self.KK.append(KK)
        self.save_kk()
        self.main()
    
    def start_kk(self):
        start = True
        test = False
        while start:
            if len(self.KK) <= 0:
                console.print('Keine Karteikarten gefunden. Mit -[com]neu[/]- neue Karten anlegen')
                break
            else:
                c_n = 0
                for card in self.KK:
                    if card.next_time <= datetime.date.today():
                        c_n += 1
                if c_n > 0:
                    random.shuffle(self.KK)
                    for card in self.KK:
                        if card.next_time <= datetime.date.today():
                            c_n = 0
                            for card_t in self.KK:
                                if card_t.next_time <= datetime.date.today():
                                    c_n += 1
                            print('{} übrige Karten'.format(c_n))
                            start = True
                            question = card.question
                            question_panel = Panel(Text(question), title = "Frage", style="green", width=50, padding=(0,0,0,0), expand = True, border_style = "green", title_align = "left")#  width=50, height = 5,
                            console.print(question_panel)
                            try:
                                image = Image.open('picture/'+ card.q_picture)
                                image.show()
                            except:
                                print('kein Bild zur Frage gefunden')
                            print('Entertaste zur Auflösung drücken:')
                            user_input = input()
                            print()
                            print('Antwort:')
                            answer = card.answer
                            answer_panel = Panel(Text(answer), title = "Antwort", style="green" ,width=50 ,padding=(0,0,0,0), expand = True, border_style = "green", title_align = "left")#  width=50, height = 5
                            console.print(answer_panel)
                            try:
                                image = Image.open('picture/'+ card.picture)
                                image.show()
                            except:
                                print('kein Bild zur Antwort gefunden')
                            self.q_correct(card)
                            test = True
                            while test:
                                test = False
                                console.print('Nächste Frage? [com]j[/]/[com]n[/]')
                                user_input = input('> ')
                                print()
                                if user_input == 'j':
                                    break
                                elif user_input == 'n':
                                    test = True
                                    break
                                else:
                                    test = True
                                    print('Anwort nicht verstanden')
                            if test:
                                start = False
                                print('Vorzeitig beendet')
                                break
                            else:
                                start = True
                                pass
                    if start == False:
                        break
                else:
                    start = False
                    print('Keine Karten für heute')
                    break    
        print('zurück zu start')
        self.main()
    
    def q_correct(self, card):
        test = True
        while test:
            test = False
            console.print('Richtig? [com]j[/] - ja, [com]n[/] - nein, [com]a[/] - abbrechen, [com]c[/] - Werte korrigieren')
            user_input = input('> ')
            print()
            if user_input == 'j':
                card.correct = card.correct + 1
                card.next_time = datetime.date.today() + datetime.timedelta(days=card.correct)
                self.save_kk()
            elif user_input == 'n':
                card.correct = 0
                card.next_time = datetime.date.today() + datetime.timedelta(days=card.correct)
                self.save_kk()
            elif user_input == 'a':
                print('Zurück zu start')
                self.main()
            elif user_input == 'c':
                self.correct_question(card)
            else:
                print("Antwort nicht erkannt")
                test = True
        print('{} mal in Folge richtig geantwortet'.format(card.correct))
        print('Die Frage muss am {} zum nächsten mal beantwortet werden.'.format(card.next_time))
        
    def correct_question(self, card):
        console.print('Ändern: [com]a[/] - Antwort, [com]q[/] - Frage, [com]c[/] - Anzahl korrekter Antworten, [com]bf[/] - Bild zur Frage, [com]ba[/] - Bild zur Antwort, [com]d[/] - Löschen, [com]n[/] - nichts')
        user_input = input('> ')
        print()
        if user_input == 'a':
            print('alte Antwort:')
            print(card.answer)
            answer = input('neu: ')
            print()
            card.answer = answer
            self.save_kk()
            self.correct_question(card)
        elif user_input == 'q':
            print('alte Frage:')
            print(card.question)
            question = input('neu: ')
            print()
            card.question = question
            self.save_kk()
            self.correct_question(card)
        elif user_input == 'bf':
            print('altes Bild zur Frage:')
            try:
                print(card.q_picture)
            except:
                print("Kein Bild zur Frage evtl. eine alte Karte")
            q_picture = input('neu: ')
            print()
            card.q_picture = q_picture
            self.save_kk()
            self.correct_question(card)
        elif user_input == 'ba':
            print('altes Bild zur Antwort:')
            print(card.picture)
            picture = input('neu: ')
            print()
            card.picture = picture
            self.save_kk()
            self.correct_question(card)
        elif user_input == 'c':
            print('alte Anzahl korrekter Antworten:')
            print(card.correct)
            correct = input('neu: ')
            print()
            card.correct = int(correct)
            card.next_time = datetime.date.today() + datetime.timedelta(days=card.correct)
            self.save_kk()
            self.correct_question(card)
        elif user_input == 'd':
            print(card.question)
            print(card.q_picture)
            print(card.answer)
            print(card.picture)
            print(card.correct)
            console.print('Löschen? [com]j[/]/[com]n[/]')
            user_input = input('> ')
            print()
            if user_input == 'j':
                self.KK.remove(card)
                self.save_kk()
        elif user_input == 'n':
            pass
        else:
            self.correct_question(card)

        
if __name__ == '__main__':
    K1 = Neue_Karteikarten()
    #Main_Karteikarten(K1)


    
