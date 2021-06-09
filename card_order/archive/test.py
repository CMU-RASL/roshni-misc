from models import Card, Rule
from utils import compute_alpha
import numpy as np

#Create all the cards
cards = []
for color in ['red', 'green', 'purple']:
    for shading in ['open', 'striped', 'solid']:
        for shape in ['diamond', 'oval', 'squiggle']:
            for number in ['one', 'two', 'three']:
                cards.append(Card(color=color, shading=shading, shape=shape, number=number))

#Create actual rule
rule = Rule(bin_num=2)
for card in cards:
    if card.color == 'red' and (card.number == 'two' or card.number == 'three'):
        rule.add_card(card, 1)
    else:
        rule.add_card(card, 0)
# for card in cards:
#     if card.shape == 'oval':
#         rule.add_card(card, 0)
#     else:
#         rule.add_card(card, 1)

card_order = []
num_cards = 10
cur_rule = Rule(bin_num=2)

for ii in range(num_cards):

    #Compute alphas
    alphas = []
    for card in cards:
        if card in card_order:
            alphas.append(0.0)
        else:
            alphas.append(compute_alpha(rule, cur_rule, card, cards))
            # break
    #Choose card with max alpha
    max_alpha = np.max(alphas)
    max_inds = np.where(alphas == np.max(alphas))[0]
    idx = np.random.choice(max_inds)
    # idx = max_inds[0]
    # print(max_inds)
    # print(np.round(alphas, decimals=2))

    #Add card
    bin = np.argmax(rule.bin_acc(cards[idx]))
    print(ii, idx, cards[idx], 'added to bin', bin, ', alpha', np.round(alphas[idx], decimals=3))

    cur_rule.add_card(cards[idx], bin)
    card_order.append(cards[idx])