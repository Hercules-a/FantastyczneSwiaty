from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty


class SelectCardWindow(Widget):
    list_of_cards = ListProperty()
    count_cards = StringProperty()
    sum_to_display = StringProperty()

    def add_card(self, state, card):
        if state == 'down':
            self.list_of_cards.append(card)
        else:
            for element in self.list_of_cards:
                if card.name == element.name:
                    self.list_of_cards.remove(element)
                    break

        self.count_cards = str(len(self.list_of_cards))
        self.points_sum()
        self.sum_to_display = str(self.points_sum())
        for card in self.list_of_cards:
            print(card.name, card.canceled_card)
        print('')

    def points_sum(self):
        points_sum = 0
        for card in self.list_of_cards:
            if not card.canceled_card:
                points_sum += card.card_points(card, self.list_of_cards)
        return points_sum

    class KrasnoludzkaPiechota:
        name = "Krasnoludzka Piechota"
        canceled_card = False
        canceled_penalty = False
        power = 15
        set = "Armia"
        description = "KARA: -2 za każdą inną kartę Armii."

        def __init__(self):
            print('abc')
            SelectCardWindow.points_sum()

        def card_points(self, list_of_cards):

            if any(card.name == "Zwiadowcy" for card in list_of_cards):
                return self.power

            else:
                penalty = -2
                for card in list_of_cards:
                    if card.set == "Armia" and not card.canceled_card:
                        penalty += 2
                return self.power - penalty


    class ElfiLucznicy:
        def __init__(self):
            SelectCardWindow.points_sum()

        name = "Elfi łucznicy"
        canceled_card = False
        canceled_penalty = False
        power = 10
        set = "Armia"
        description = "PREMIA: +5, jeśli nie masz żadnej karty Pogody."

        def card_points(self, list_of_cards):
            for card in list_of_cards:
                if card.set == "Pogoda" and not card.canceled_card:
                    return self.power
            return self.power + 5

    class Rycerze:
        def __init__(self):
            SelectCardWindow.points_sum()

        name = "Rycerze"
        canceled_card = False
        canceled_penalty = False
        power = 20
        set = "Armia"
        description = "KARA: -8, chyba że masz przynajmniej 1 kartę Przywódcy"

        def card_points(self, list_of_cards):
            if any(card.set == "Przywódca" for card in list_of_cards):
                return self.power
            return self.power - 8


    class LekkaKonnica:
        def __init__(self):
            SelectCardWindow.points_sum()

        name = "Lekka konnica"
        canceled_card = False
        canceled_penalty = False
        power = 17
        set = "Armia"
        description = "KARA: -2 za każdą kartę Krainy."

        def card_points(self, list_of_cards):
            penalty = 0
            for card in list_of_cards:
                if card.set == "Kraina":
                    penalty += 2
            return self.power - penalty


    class Zwiadowcy:
        def __init__(self):
            SelectCardWindow.points_sum()

        name = "Zwiadowcy"
        canceled_card = False
        canceled_penalty = False
        power = 5
        set = "Armia"
        description = "PREMIA: +10 za każdą kartę Krainy. USUWA słowo Armia z kar wszystkich kart."

        def card_points(self, list_of_cards):
            bonus = 0
            for card in list_of_cards:
                if card.set == "Kraina":
                    bonus += 10
            return self.power + bonus

    class Bazyliszek:
        def __init__(self):
            SelectCardWindow.points_sum()

        name = "Bazyliszek"
        canceled_card = False
        canceled_penalty = False
        power = 35
        set = "Bestia"
        description = "KARA: ANULUJE wszystkie karty Armii, Przywódcy i innych Bestii."

        def card_points(self, list_of_cards):
            for card in list_of_cards:
                if card.set == "Armia" or card.set == "Przywódca" or (card.set == "Przywódca" and card.name != "Bazyliszek"):
                    card.canceled_card = True
            return self.power


class MyApp(App):
    def build(self):
        return SelectCardWindow()


if __name__ == "__main__":
    MyApp().run()
