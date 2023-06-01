from random import choice

class FrenchDeck:
    deck1 = [rank+suit for suit in [str(n) for n in range(6,11)]+list("JQKA") for rank in "♠ ♣ ♦ ♥".split()]
    deck2 = [rank+suit for suit in [str(n) for n in range(6,11)]+list("JQKA") for rank in "♠ ♣ ♦ ♥".split()]

    def __init__(self):
        self.cards = self.mix()
        self.player, self.bot = self.distribution()
        self.trum = self.cards[-1]
        self.print_inf()
        self.move = self.first_walks()
        self.table = []
        while True:
            if self.ran_game(): break

    def mix(self):
        card = [] 
        while len(self.deck1):
            card.append(choice(self.deck1))
            self.deck1.remove(card[-1])
        return card

    def distribution(self):
        p,b = [],[]
        for _ in range(6):
            p.append(self.cards.pop(0))
            b.append(self.cards.pop(0))
        return p,b
    
    def first_walks(self):
        min,chek = 37,'player'
        for i in range(6):
            if self.player[i][0] == self.trum[0] and self.deck2.index(self.player[i])<min:
                min = self.deck2.index(self.player[i]); chek = 'player'
            if self.bot[i][0] == self.trum[0] and self.deck2.index(self.bot[i])<min:
                min = self.deck2.index(self.bot[i]); chek = 'bot'
        try: print("У", chek, "мінімальний козирь тому він ходить перший!")
        except: print("Козирів немає тому перший ходить ігрок!")
        return chek

    def ran_game(self):
        if self.move == "player":
            while True:
                if self.hod_pleyer():
                    print("Знову ваш ход!"); break
                if input("Підкинути (Y): ").upper()=="Y":
                    if not self.throw_up_player():
                        print("Вам нема чим підкидати!")
                        print("Ходить Бот ви б'єтеся!")
                        self.move = "bot"; break
                else: self.move = "bot"; break
        else:
            while True:
                if self.hod_bot():
                    print("Знову ходить Бот ви б'єтеся!");break
                if not self.throw_up_bot():
                    print("Боту нема що підкидати!")
                    print("Ваш ход!")
                    self.move = "player"; break

        self.table = []; self.new_cards()
        if (self.player==[] or self.bot==[]) and self.cards==[]:
            self.game_over(); return True
        else: self.new_cards()
        self.print_inf(); return False

    def throw_up_bot(self):
        for i in self.bot:
            for j in self.table:
                if i[0]!=self.trum[0] and i[1:] == j[1:]: return True
        return False
    
    def throw_up_player(self):
        for i in self.player:
            for j in self.table:
                if i[1:] == j[1:]: return True
        return False
    
    def new_cards(self):
        while len(self.bot)<6: 
            if not len(self.cards):break
            else: self.bot.append(self.cards.pop(0))
        while len(self.player)<6:
            if not len(self.cards): break
            else: self.player.append(self.cards.pop(0))
            
    def hod_pleyer(self):
        while True:
            p = input("Введіть чим бажаете походити: ")
            if p in self.player: 
                if self.table == []: break
                elif self.check(p): break
        self.player.remove(p)
        self.table.append(p)
        b = self.logick_bot(p)
        if b == False:
            print("Бот не може побити він забирає!")
            self.bot += self.table; self.table = []
            return True
        else:
            self.table.append(b); self.bot.remove(b)
            print("Бот побив картою -", b); self.print_inf()
            return False
    
    def logick_bot(self, p):
        min = 37
        for i in range(len(self.bot)):
            if p[0]==self.bot[i][0] and self.ind(self.bot[i])>self.ind(p): min = self.deck2.index(self.bot[i])
        try: return self.deck2[min]
        except: return self.logik_kill(p)

    def logik_kill(self, p):
        if p[0] != self.trum[0]:
            min = 37
            for i in self.bot:
                if i[0]==self.trum[0] and self.ind(i)<min: min = self.ind(i)
            try: return self.deck2[min]
            except: return False 
        else:
            mas = [self.ind(i)for i in self.bot if i[0]==self.trum[0]and self.ind(p)<self.ind(i)]
            for i in sorted(mas):
                if i>self.ind(p): return self.deck2[i]
            return False

    def hod_bot(self):
        if self.table==[]:
            min = 37
            for i in self.bot:
                if i[0]!=self.trum[0] and self.ind(i)<min: min = self.ind(i)
            try: b = self.deck2[min]
            except:
                for i in self.bot:
                    if self.ind(i)<min: min = self.ind(i)
                b = self.deck2[min]
        else:
            for i in self.bot:
                for j in self.table:
                    if i[0]!=self.trum[0] and i[1:]==j[1:]: b = i
        self.bot.remove(b)
        self.table.append(b)
        print("Бот походив -", b)
        if not self.no_options(b):
            print("Нажаль вам нема чим побити!")
            self.player += self.table; self.table = []
            return True
        else:
            while True:
                p = input("Введіть чим бажаете побити або (З-забрать): ")
                if p.upper() == 'З': 
                    print("Ви забираете карти!")
                    self.player += self.table; self.table = []
                    return True
                if p in self.player:
                    if b[0]==p[0] and self.ind(p)>self.ind(b): break
                    if p[0]==self.trum[0] and b[0]!=self.trum[0] : break
                    if p[0]==self.trum[0] and b[0]==self.trum[0] and self.ind(p)>self.ind(b): break
            self.table.append(p); self.player.remove(p)
            if self.throw_up_bot(): self.print_inf()
            return False

    def no_options(self, b):
        for i in self.player:
            if i[0]==b[0] and self.ind(i)>self.ind(b): return True
        for i in self.player:
            if i[0]==self.trum[0] and self.ind(i)>self.ind(b): return True
        return False

    def game_over(self):
        if self.player == []:
            print("Ти переміг! Вітаю з перемогою!")
        if self.bot == []:
            print("Ти програв. Не засмучуйся!")

    def print_inf(self):
        print("Ващи карти -", self.player)
        print("Бота карти -", self.bot)
        print("Козирь -", self.trum)

    def check(self, x):
        for i in self.table:
            if x[1:] == i[1:]: return True
        return False
    
    def ind(self, x):
        return self.deck2.index(x)

game = FrenchDeck()