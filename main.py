from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from operator import attrgetter


class SelectCardWindow(Widget):
    list_of_cards = ListProperty()
    count_cards = StringProperty()
    sum_to_display = StringProperty()

    def add_card(self, state, card):
        if state == 'down':
            if any(card.name == "Nekromanta" and not card.canceled_card for card in self.list_of_cards):
                if len(self.list_of_cards) < 8:
                    self.list_of_cards.append(card)
            else:
                if len(self.list_of_cards) < 7:
                    self.list_of_cards.append(card)
        else:
            for element in self.list_of_cards:
                if card.name == element.name:
                    self.list_of_cards.remove(element)
                    break
        if any(card.name == "Nekromanta" and not card.canceled_card for card in self.list_of_cards):
            self.count_cards = "{}/8".format(str(len(self.list_of_cards)))
        else:
            self.count_cards = "{}/7".format(str(len(self.list_of_cards)))

        # double check because last cards in list can change firsts cards parameters
        self.points_sum()
        self.sum_to_display = str(self.points_sum())

        # reset properties
        for card in self.list_of_cards:
            card.canceled_card = False

    def points_sum(self):
        points_sum = 0
        for card in self.list_of_cards:
            if not card.canceled_card:
                points_sum += card.card_points(card, self.list_of_cards)
        return points_sum

    class KrasnoludzkaPiechota:
        name = "Krasnoludzka Piechota"
        canceled_card = False
        power = 15
        set = "Armia"
        description = "KARA: -2 za każdą inną kartę Armii."

        def __init__(self):
            print('abc')
            SelectCardWindow.points_sum()

        def card_points(self, list_of_cards):

            if any(card.name in ("Zwiadowcy", "Runa ochrony") for card in list_of_cards):
                return self.power
            else:
                penalty = 0
                for card in list_of_cards:
                    if card.set == self.set and not card.canceled_card and card.name != self.name:
                        penalty += 2
                return self.power - penalty

    class ElfiLucznicy:
        name = "Elfi łucznicy"
        canceled_card = False
        power = 10
        set = "Armia"
        description = "PREMIA: +5, jeśli nie masz żadnej karty Pogody."

        def card_points(self, list_of_cards):
            for card in list_of_cards:
                if card.set == "Pogoda" and not card.canceled_card:
                    return self.power
            return self.power + 5

    class Rycerze:
        name = "Rycerze"
        canceled_card = False
        power = 20
        set = "Armia"
        description = "KARA: -8, chyba że masz przynajmniej 1 kartę Przywódcy"

        def card_points(self, list_of_cards):
            if any((card.set == "Przywódca" or card.name == "Runa ochrony") and not card.canceled_card
                   for card in list_of_cards):
                return self.power
            return self.power - 8

    class LekkaKonnica:
        name = "Lekka konnica"
        canceled_card = False
        power = 17
        set = "Armia"
        description = "KARA: -2 za każdą kartę Krainy."

        def card_points(self, list_of_cards):
            penalty = 0
            if not any(card.name == "Runa ochrony" for card in list_of_cards):
                for card in list_of_cards:
                    if card.set == "Kraina" and not card.canceled_card:
                        penalty += 2
            return self.power - penalty

    class Zwiadowcy:
        name = "Zwiadowcy"
        canceled_card = False
        power = 5
        set = "Armia"
        description = "PREMIA: +10 za każdą kartę Krainy. USUWA słowo Armia z kar wszystkich kart."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == "Kraina" and not card.canceled_card:
                    bonus += 10
            return self.power + bonus

    class Bazyliszek:
        name = "Bazyliszek"
        canceled_card = False
        power = 35
        set = "Bestia"
        description = "KARA: ANULUJE wszystkie karty Armii, Przywódcy i innych Bestii."

        def card_points(self, list_of_cards):
            for card in list_of_cards:
                if not any(card.name in ("Władca bestii", "Runa ochrony") for card in list_of_cards):
                    if card.set == "Armia" and not any(card.name == "Zwiadowcy" for card in list_of_cards):
                        card.canceled_card = True
                    if card.set == "Przywódca" or (card.set == "Bestia" and card.name != "Bazyliszek"):
                        card.canceled_card = True
            return self.power

    class Smok:
        name = "Smok"
        canceled_card = False
        power = 30
        set = "Bestia"
        description = "KARA: -40, chyba że masz przynajmniej 1 kartę Czarodzieja"

        def card_points(self, list_of_cards):
            if not any(card.set == "Czarodziej" and not card.canceled_card for card in list_of_cards):
                if not any(card.name in ("Władca bestii", "Runa ochrony") for card in list_of_cards):
                    return self.power - 40
            return self.power

    class Hydra:
        name = "Hydra"
        canceled_card = False
        power = 12
        set = "Bestia"
        description = "PREMIA: +28 z Bagnem."

        def card_points(self, list_of_cards):
            if any(card.name == "Bagno" for card in list_of_cards):
                return self.power + 28
            return self.power

    class Jednorozec:
        name = "Jednorożec"
        canceled_card = False
        power = 9
        set = "Bestia"
        description = "PREMIA: +30 z Księżniczką ALBO +15 z Cesarzową, Królową albo Zaklinaczką."

        def card_points(self, list_of_cards):
            if any(card.name == "Księżniczka" for card in list_of_cards):
                return self.power + 30
            if any(card.name in ("Cesarzowa", "Królowa", "Zaklinaczka") for card in list_of_cards):
                return self.power + 15
            return self.power

    class Rumak:
        name = "Rumak"
        canceled_card = False
        power = 6
        set = "Bestia"
        description = "PREMIA: +14 z dowolną kartą Przywódcy albo Czarodzieja."

        def card_points(self, list_of_cards):
            if any(card.set in ("Przywódca", "Czarodziej") for card in list_of_cards):
                return self.power + 14
            return self.power

    class Swieca:
        name = "Świeca"
        canceled_card = False
        power = 2
        set = "Płomień"
        description = "PREMIA: +100 z Księgą zmian, Dzwonnicą i dowolną kartą Czarodzieja."

        def card_points(self, list_of_cards):
            if any(card.set == "Czarodziej" for card in list_of_cards):
                if any(card.name == "Księga zmian" for card in list_of_cards):
                    if any(card.set == "Dzwonnica" for card in list_of_cards):
                        return self.power + 100
            return self.power

    class ZywiolakOgnia:
        name = "Żywiołak ognia"
        canceled_card = False
        power = 4
        set = "Płomień"
        description = "PREMIA: +15 za każdą inną kartę Płomienia."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == self.set and card.name != self.name:
                    bonus += 15
            return self.power + bonus

    class Kuznia:
        name = "Kuźnia"
        canceled_card = False
        power = 9
        set = "Płomień"
        description = "PREMIA: +9 za każdą kartę Broni i Artefaktu."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set in ("Broń", "Artefakt"):
                    bonus += 9
            return self.power + bonus

    class Blyskawica:
        name = "Błyskawica"
        canceled_card = False
        power = 11
        set = "Płomień"
        description = "PREMIA: +30 z Burzą"

        def card_points(self, list_of_cards):
            if any(card.name == "Burza" for card in list_of_cards):
                return self.power + 30
            return self.power

    class Pozar:
        name = "Pożar"
        canceled_card = False
        power = 40
        set = "Płomień"
        description = "KARA: ANULUJE wszystkie karty z wyjątkiem Płomienia, Czarodzieja, " \
                      "Pogody, Broni, Artefaktu, Gór, Potopu, Wyspy, Jednorożca i Smoka"

        def card_points(self, list_of_cards):
            if not any(card.name == "Runa ochrony" for card in list_of_cards):
                for card in list_of_cards:
                    print(card.set)

                    if not card.set in ("Płomień", "Czarodziej", "Pogoda", "Broń", "Artefakt"):
                        if not card.name in ("Góry", "Potop", "Wyspa", "Jednorożec", "Smok"):
                            card.canceled_card = True
            return self.power

    class FontannaZycia:
        name = "Fontanna życia"
        canceled_card = False
        power = 1
        set = "Powódź"
        description = "PREMIA: Dodaj podstawową siłę dowolnej karty Broni, Powodzi, Płomienia, Krainy albo Pogody"

        def card_points(self, list_of_cards):
            # the most powerful card is Pozar with power 40
            return self.power + 40

    class Potop:
        name = "Potop"
        canceled_card = False
        power = 32
        set = "Powódź"
        description = "KARA: ANULUJE wszystkie karty Armii, wszystkie karty Krainy z wyjątkiem Gór " \
                      "i wszystkie karty Płomienia z wyjątkiem Błyskawicy."

        def card_points(self, list_of_cards):
            if not any(card.name in ("Runa ochrony", "Góry", "Zwiadowcy") for card in list_of_cards):
                for card in list_of_cards:
                    if card.set == "Armia" and not any(card.name == "Okręt" and not card.canceled_card
                                                       for card in list_of_cards):
                        card.canceled_card = True
                    if card.set in ("Kraina", "Płomień"):
                        if card.name not in ("Góry", "Błyskawica"):
                            card.canceled_card = True
            return self.power

    class Wyspa:
        name = "Wyspa"
        canceled_card = False
        power = 14
        set = "Powódź"
        description = "PREMIA: USUWA karę z dowolnej karty Powodzi albo Płomienia"

        def card_points(self, list_of_cards):
            return self.power

    class Bagno:
        name = "Bagno"
        canceled_card = False
        power = 18
        set = "Powódź"
        description = "KARA: -3 za każdą kartę Armii i Płomienia"

        def card_points(self, list_of_cards):
            penalty = 0
            if not any(card.name in ("Runa ochrony", "Góry") for card in list_of_cards):
                for card in list_of_cards:
                    if card.set == "Armia" and not any(card.name == "Okręt" for card in list_of_cards):
                        penalty += 3
                    if card.set == "Płomień":
                        penalty += 3
                return self.power - penalty

    class ZywiolakWody:
        name = "Żywiołak wody"
        canceled_card = False
        power = 4
        set = "Powódź"
        description = "PREMIA: +15 za każdą inną kartę Powodzi."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == self.set and card.name != self.name:
                    bonus += 15
            return self.power + bonus

    class Dzwonnica:
        name = "Dzwonnica"
        canceled_card = False
        power = 8
        set = "Kraina"
        description = "PREMIA: +15 z dowolną kartą Czarodzieja."

        def card_points(self, list_of_cards):
            if any(card.set == "Czarodziej" and not card.canceled_card for card in list_of_cards):
                return self.power + 15
            return self.power

    class Jaskinia:
        name = "Jaskinia"
        canceled_card = False
        power = 6
        set = "Kraina"
        description = "PREMIA: +25 z Krasnoludzką piechotą lub Smokiem. USUWA kary wszystkiech kart Pogody."

        def card_points(self, list_of_cards):
            if any(card.name in ("Krasnoludzka piechota", "Smok") and not card.canceled_card for card in list_of_cards):
                return self.power + 25
            return self.power

    class ZywiolakZiemi:
        name = "Żywiołak ziemi"
        canceled_card = False
        power = 4
        set = "Kraina"
        description = "PREMIA: +15 za każdą inną kartę Krainy."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == self.set and card.name != self.name and not card.canceled_card:
                    bonus += 15
            return self.power + bonus

    class Las:
        name = "Las"
        canceled_card = False
        power = 7
        set = "Kraina"
        description = "PREMIA: +12 za każdą kartę Bestii i Elfich łuczników"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if (card.set == "Bestia" or card.name == "Elfi łucznicy") and not card.canceled_card:
                    bonus += 12
            return self.power + bonus

    class Gory:
        name = "Góry"
        canceled_card = False
        power = 9
        set = "Kraina"
        description = "PREMIA: +50 z Dymem i Pożarem. USUWA kary z wszystkich kart Powodzi."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if (card.set == "Bestia" or card.name == "Elfi łucznicy") and not card.canceled_card:
                    bonus += 12
            return self.power + bonus

    class Cesarzowa:
        name = "Cesarzowa"
        canceled_card = False
        power = 15
        set = "Przywódca"
        description = "PREMIA: +10 za każdą kartę Armii. KARA: -5 za każdą inną kartę Przywódcy."

        def card_points(self, list_of_cards):
            bonus, penalty = 0, 0
            for card in list_of_cards:
                if card.set == "Armia" and not card.canceled_card:
                    bonus += 10
                if not any(card.name == "Runa ochrony" for card in list_of_cards):
                    if card.set == self.set and card.name != self.name and not card.canceled_card:
                        penalty += 5
            return self.power + bonus - penalty

    class Krol:
        name = "Król"
        canceled_card = False
        power = 8
        set = "Przywódca"
        description = "PREMIA: +5 za każdą kartę Armii. ALBO +20 za każdą kartę Armii, jeśli masz Królową"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if any(card.name == "Królowa" and not card.canceled_card for card in list_of_cards):
                    if card.set == "Armia" and not card.canceled_card:
                        bonus += 20
                else:
                    if card.set== "Armia" and not card.canceled_card:
                        bonus += 5
            return self.power + bonus

    class Ksiezniczka:
        name = "Księżniczka"
        canceled_card = False
        power = 2
        set = "Przywódca"
        description = "PREMIA: +8 za każdą kartę Armii, Czarodzieja i innego Przywódcy"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set in ("Armia", "Czarodziej", "Przywódca") and card.name != self.name \
                        and not card.canceled_card:
                    bonus += 8
            return self.power + bonus

    class Krolowa:
        name = "Królowa"
        canceled_card = False
        power = 6
        set = "Przywódca"
        description = "PREMIA: +5 za każdą kartę Armii. ALBO +20 za każdą kartę Armii, jeśli masz Króla"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if any(card.name == "Król" and not card.canceled_card for card in list_of_cards):
                    if card.set == "Armia" and not card.canceled_card:
                        bonus += 20
                else:
                    if card.set == "Armia" and not card.canceled_card:
                        bonus += 5
            return self.power + bonus

    class WielkiWodz:
        name = "Wielki wódz"
        canceled_card = False
        power = 4
        set = "Przywódca"
        description = "PREMIA: Suma podstawowych wartości siły wszystkich kart Armii."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == "Armia" and not card.canceled_card:
                    bonus += card.power
            return self.power + bonus

    class ElfiDlugiLuk:
        name = "Elfi długi łuk"
        canceled_card = False
        power = 3
        set = "Broń"
        description = "PREMIA: +30 z Elfimi łucznikami, Wielkim wodzem albo Władcą bestii."

        def card_points(self, list_of_cards):
            if any(card.name in ("Elfi łucznicy", "Wielki wódz", "Władca bestii") and
                   not card.canceled_card for card in list_of_cards):
                return self.power + 30
            return self.power

    class MagicznaRozdzka:
        name = "Magiczna różdżka"
        canceled_card = False
        power = 1
        set = "Broń"
        description = "PREMIA: +25 z dowolną kartą Czarodzieja."

        def card_points(self, list_of_cards):
            if any(card.set == "Czarodziej" and not card.canceled_card for card in list_of_cards):
                return self.power + 25
            return self.power

    class MieczKetha:
        name = "Miecz Ketha"
        canceled_card = False
        power = 7
        set = "Broń"
        description = "PREMIA: +10 z dowolną kartą Przywódcy ALBO +40 z dowolną kartą Przywódcy i Tarczą Ketha."

        def card_points(self, list_of_cards):
            if any(card.set == "Przywódca" and not card.canceled_card for card in list_of_cards):
                if any(card.name == "Tarcza Ketha" and not card.canceled_card for card in list_of_cards):
                    return self.power + 40
                else:
                    return self.power + 10
            return self.power

    class SterowiecWojenny:
        name = "Sterowiec wojenny"
        canceled_card = False
        power = 35
        set = "Broń"
        description = "KARA: ANULOWANY, chyba że masz przynajmniej 1 kartę Armii. ANULOWANY z dowolną kasrtą pogody."

        def card_points(self, list_of_cards):
            if not any(card.name == "Runa ochrony" for card in list_of_cards):
                if not any(card.name == "Zwiadowcy" and not card.canceled_card for card in list_of_cards):
                    if not any(card.set == "Armia" for card in list_of_cards):
                        self.canceled_card = True
                if any(card.set == "Pogoda" for card in list_of_cards):
                    self.canceled_card = True
            return self.power

    class Okret:
        name = "Okręt"
        canceled_card = False
        power = 23
        set = "Broń"
        description = "KARA: ANULOWANY, chyba że masz przynajmniej 1 kartę Powodzi. " \
                      "USUWA słowo Armia z wszystkich kar wszystkich kart powodzi."

        def card_points(self, list_of_cards):
            if not any((card.set == "Powódź" or card.name == "Runa ochrony") and not card.canceled_card
                       for card in list_of_cards):
                self.canceled_card = True
            return self.power

    class ZywiolakPowietrza:
        name = "Żywiołak powietrza"
        canceled_card = False
        power = 4
        set = "Pogoda"
        description = "PREMIA: +15 za każdą inną kartę Pogody."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == self.set and card.name != self.name and not card.canceled_card:
                    bonus += 15
            return self.power + bonus

    class Sniezyca:
        name = "Śnieżyca"
        canceled_card = False
        power = 30
        set = "Pogoda"
        description = "KARA: ANULUJE wszystkie karty Powodzi. -5 za każdą kartę Armii, Przywódcy, Bestii i Płomienia."

        def card_points(self, list_of_cards):
            penalty = 0
            if not any(card.name in ("Runa ochrony", "Jaskinia") and not card.canceled_card for card in list_of_cards):
                for card in list_of_cards:
                    if card.set == "Powódź":
                        card.canceled_card = True
                    if card.set in ("Przywódca", "Bestia", "Płomień") and not card.canceled_card:
                        penalty += 5
                    if not any(card.name == "Zwiadowcy" and not card.canceled_card for card in list_of_cards):
                        if card.set == "Armia" and not card.canceled_card:
                            penalty += 5
            return self.power - penalty

    class Burza:
        name = "Burza"
        canceled_card = False
        power = 8
        set = "Pogoda"
        description = "PREMIA: +10 za każdą kartę Powodzi. KARA: " \
                      "ANULUJE wszystkie karty Płomienia z wyjątkiem Błyskawicy"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == "Powódź" and not card.canceled_card:
                    bonus += 10
            if not any(card.name in ("Runa ochrony", "Jaskinia") and not card.canceled_card for card in list_of_cards):
                for card in list_of_cards:
                    if card.set == "Płomień" and card.name != "Błyskawica":
                        card.canceled_card = True
            return self.power + bonus

    class Dym:
        name = "Dym"
        canceled_card = False
        power = 27
        set = "Pogoda"
        description = "KARA: Ta kara zostaje ANULOWANA, chyba że masz przynajmniej 1 kartę Płomienia"

        def card_points(self, list_of_cards):
            if not any((card.name in ("Runa ochrony", "Jaskinia") or card.set == "Płomień")
                       and not card.canceled_card for card in list_of_cards):
                self.canceled_card = True
            return self.power

    class Tornado:
        name = "Tornado"
        canceled_card = False
        power = 13
        set = "Pogoda"
        description = "PREMIA: +40 z Burzą i Śnieżycą albo Burzą i Potopem"

        def card_points(self, list_of_cards):
            if any(card.name == "Burza" and not card.canceled_card for card in list_of_cards):
                if any(card.name in ("Śnieżyca", "Potop") and not card.canceled_card for card in list_of_cards):
                    return self.power + 40
            return self.power

    class KsiegaZmian:
        name = "Księga zmian"
        canceled_card = False
        power = 3
        set = "Artefakt"
        description = "PREMIA: Możesz zmienić zestaw do którego należy 1 inna kasta. " \
                      "Jej nazwa, premia i kary pozostają te same."

        def card_points(self, list_of_cards):
            return self.power

    class TarczaKetha:
        name = "Tarcza Ketha"
        canceled_card = False
        power = 4
        set = "Artefakt"
        description = "PREMIA: +15 z dowolną kartą Przywódcy ALBO +40 z dowolną kartą Przywódcy i Mieczem Ketha."

        def card_points(self, list_of_cards):
            if any(card.set == "Przywódca" and not card.canceled_card for card in list_of_cards):
                if any(card.name == "Miecz Ketha" and not card.canceled_card for card in list_of_cards):
                    return self.power + 40
                else:
                    return self.power + 15
            return self.power

    class KlejnotPorzadku:
        name = "Klejnot porządku"
        canceled_card = False
        power = 5
        set = "Artefakt"
        description = "PREMIA: Odnosi się do podstawowej wartości siły, +10 za 3 karty pod rząd itd."

        def card_points(self, list_of_cards):
            score = []
            count = 1
            sorted_list = []
            for card in list_of_cards:
                if not card.canceled_card:
                    sorted_list.append(card)
            sorted_list = sorted(sorted_list, key=attrgetter("power"))
            try:
                for i in range(9):
                    if sorted_list[i+1].power - sorted_list[i].power == 1:
                        count += 1
                    elif sorted_list[i+1].power - sorted_list[i].power == 0:
                        pass
                    else:
                        score.append(count)
                        count = 1
            except IndexError:
                pass
            if max(score) == 3:
                return self.power + 10
            elif max(score) == 4:
                return self.power + 30
            elif max(score) == 5:
                return self.power + 60
            elif max(score) == 6:
                return self.power + 100
            elif max(score) == 7:
                return self.power + 150
            else:
                return self.power

    class DrzewoSwiata:
        name = "Drzewo świata"
        canceled_card = False
        power = 2
        set = "Artefakt"
        description = "PREMIA: +50, jeśli każda nie-ANULOWANA karta pochodzi z innego zestawu."

        def card_points(self, list_of_cards):
            sorted_list = []
            for card in list_of_cards:
                if not card.canceled_card:
                    sorted_list.append(card)
            sorted_list = sorted(sorted_list, key=attrgetter("set"))
            try:
                for i in range(9):
                    if sorted_list[i+1].set == sorted_list[i].set:
                        return self.power
            except IndexError:
                pass
            return self.power + 50

    class RunaOchrony:
        name = "Runa ochrony"
        canceled_card = False
        power = 1
        set = "Artefakt"
        description = "PREMIA: USUWA kary z wszystkich kart."

        def card_points(self, list_of_cards):
            return self.power

    class WladcaBestii:
        name = "Władca bestii"
        canceled_card = False
        power = 9
        set = "Czarodziej"
        description = "PREMIA: +9 za każdą kartę Bestii. USUWA kary z wszystkich kart Bestii."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == "Bestia" and not card.canceled_card:
                    bonus += 9
            return self.power + bonus

    class Kolekcjoner:
        name = "Kolekcjoner"
        canceled_card = False
        power = 7
        set = "Czarodziej"
        description = "PREMIA: +9 za każdą kartę Bestii. USUWA kary z wszystkich kart Bestii."

        def card_points(self, list_of_cards):
            score = []
            count = 1
            sorted_list = []
            for card in list_of_cards:
                if not card.canceled_card:
                    sorted_list.append(card)
            sorted_list = sorted(sorted_list, key=attrgetter("set"))
            try:
                for i in range(9):
                    if sorted_list[i + 1].set == sorted_list[i].set:
                        count += 1
                    else:
                        score.append(count)
                        count = 1
            except IndexError:
                pass
            if max(score) == 3:
                return self.power + 10
            elif max(score) == 4:
                return self.power + 40
            elif max(score) == 5:
                return self.power + 100
            else:
                return self.power

    class Zaklinaczka:
        name = "Zaklinaczka"
        canceled_card = False
        power = 5
        set = "Czarodziej"
        description = "PREMIA: +5 za każdą kartę Krainy, Pogody, Powodzi i Płomienia"

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set in ("Kraina", "Pogoda", "Powódź", "Płomień") and not card.canceled_card:
                    bonus += 5
            return self.power + bonus

    class Nekromanta:
        name = "Nekromanta"
        canceled_card = False
        power = 3
        set = "Czarodziej"
        description = "PREMIA: Na koniec gry możesz wziąć z obszaru kart odrzuconych 1 kartę Armii, Przywódcy, " \
                      "Czarodzieja albo Bestii i dołączyć ją do swoich kart na ręce jako ósmą kartę."

        def card_points(self, list_of_cards):
            return self.power

    class Czarnoksieznik:
        name = "Czarnoksiężnik"
        canceled_card = False
        power = 25
        set = "Czarodziej"
        description = "KARA: -10 za każdą kartę Przywódcy i każdą inną kartę Czarodzieja."

        def card_points(self, list_of_cards):
            penalty = 0
            if not any(card.name == "Runa ochrony" for card in list_of_cards):
                for card in list_of_cards:
                    if card.set in ("Przywódca", "Czarodziej") and not card.canceled_card and card.name != self.name:
                        penalty += 10
            return self.power - penalty

    class Blazen:
        name = "Błazen"
        canceled_card = False
        power = 3
        set = "Czarodziej"
        description = "PREMIA: +3 za każdą inną kartę posiadającą nieparzystą podstawową siłę " \
                      "ALBO +50, jeśli każda karta na Twojej ręce posiada nieparzystą podstawową siłę."

        def card_points(self, list_of_cards):
            bonus = 0
            if all(card.power % 2 == 1 for card in list_of_cards):
                return self.power + 50
            sorted_list = []
            for card in list_of_cards:
                if not card.canceled_card:
                    sorted_list.append(card)
            sorted_list = sorted(sorted_list, key=attrgetter("name"))
            try:
                for i in range(9):
                    if sorted_list[i + 1].name != sorted_list[i].name and sorted_list[i].power % 2 == 1:
                        bonus += 3
            except IndexError:
                pass
            return self.power + bonus


class MyApp(App):
    def build(self):
        return SelectCardWindow()


if __name__ == "__main__":
    MyApp().run()
