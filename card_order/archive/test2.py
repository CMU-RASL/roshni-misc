from models import Card, Rule, Hypothesis
from utils import compute_alpha, compute_hyp_removed
import numpy as np
import pickle as pkl
import os.path

#Create all the cards
cards = []
for color in ['red', 'green', 'purple']:
    for shading in ['open', 'striped', 'solid']:
        for shape in ['diamond', 'oval', 'squiggle']:
            for number in ['one', 'two', 'three']:
                cards.append(Card(color=color, shading=shading, shape=shape, number=number))

props = {'color': ['red', 'green', 'purple'], 'shading': ['open', 'striped', 'solid'], 'shape': ['diamond', 'oval', 'squiggle'], 'number': ['one', 'two', 'three']}

#Ovals on left, everything else on right
true_hyp = Hypothesis(bin_num = 2, bins = [ [ [['color', ['red']], ['number', ['two', 'three']] ], [['color', ['green', 'purple']]] ] ,
                                             [ [['color', ['red']], ['number', ['one']] ]  ]   
                                             ] )
prop_vals = {'color': [[],[]], 'shading': [[],[]], 'shape': [[],[]], 'number': [[],[]]}
for prop, prop_val in props.items():
    #All possible combos

    #All and all
    prop_vals[prop][0].append(prop_val)
    prop_vals[prop][1].append(prop_val)

    #All and none
    prop_vals[prop][0].append(prop_val)
    prop_vals[prop][1].append([])
    prop_vals[prop][1].append(prop_val)
    prop_vals[prop][0].append([])

    #One and two
    for val1 in prop_val:
        one = [val1]
        two = []
        for val2 in prop_val:
            if not val2 == val1:
                two.append(val2)
        
        prop_vals[prop][0].append(one)
        prop_vals[prop][1].append(two)
        prop_vals[prop][0].append(two)
        prop_vals[prop][1].append(one)



file_count = 0
for color0, color1 in zip(prop_vals['color'][0], prop_vals['color'][1]):
    for shading0, shading1 in zip(prop_vals['shading'][0], prop_vals['shading'][1]):
        file_count += 1
        count = 0
        if not os.path.exists(str(file_count)+'.pkl'):
            all_hyp = []
            for shape0, shape1 in zip(prop_vals['shape'][0], prop_vals['shape'][1]):
                for number0, number1 in zip(prop_vals['number'][0], prop_vals['number'][1]):
                    for color0_1, color1_1 in zip(prop_vals['color'][0], prop_vals['color'][1]):
                        for shading0_1, shading1_1 in zip(prop_vals['shading'][0], prop_vals['shading'][1]):
                            for shape0_1, shape1_1 in zip(prop_vals['shape'][0], prop_vals['shape'][1]):
                                for number0_1, number1_1 in zip(prop_vals['number'][0], prop_vals['number'][1]):
                                    
                                    all_hyp.append(Hypothesis(bin_num=2, bins = [ [ [['color', color0 ], ['shading', shading0], ['shape', shape0], ['number', number0] ],
                                                                                [['color', color0_1 ], ['shading', shading0_1], ['shape', shape0_1], ['number', number0_1] ]],
                                                                                [ [['color', color1 ], ['shading', shading1], ['shape', shape1], ['number', number1] ],
                                                                                [['color', color1_1 ], ['shading', shading1_1], ['shape', shape1_1], ['number', number1_1] ]] ]))

                                    count += 1
                                    print(np.round(count / 9**6, decimals=6))

            with open(str(file_count)+'.pkl','wb') as f:
                pkl.dump(all_hyp, f)

#Load all files
all_hyp = []
for f_num in range(1, 82):
    with open(str(f_num)+'.pkl', 'rb') as f:
        hyp = pkl.load(f)
    all_hyp.extend(hyp)
    print(f_num)

with open('hypotheses.pkl', 'wb') as f:
    pkl.dump(all_hyp, f)

# with open('hypotheses.pkl', 'rb') as f:
#     all_hyp = pkl.load(f)

# #One exception possible
# all_hyp = []

# #Pick two properties
# for prop1, prop_vals1 in props.items():
#     for prop2, prop_vals2 in props.items():
#         if not prop1 == prop2:
        
#             for prop_val1 in prop_vals1:
#                 p1_1 = [prop_val1]
#                 p1_2 = []
#                 for prop_val1_1 in prop_vals1:
#                     if not prop_val1_1 == prop_val1:
#                         p1_2.append(prop_val1_1)
                
#                 for prop_val2 in prop_vals2:
#                     p2_1 = [prop_val2]
#                     p2_2 = []
#                     for prop_val2_1 in prop_vals2:
#                         if not prop_val2_1 == prop_val2:
#                             p2_2.append(prop_val2_1)
                    
#                     for place1 in zip(p2_1, p2_2):
#                         bin0 = [p1_1, place1]
#                     [p1_1, p2_1], [p1_1, p2_2]
                    
#                     hyp = Hypothesis(bin_num = 2, bins = [0, 1, 1], props=[ [ [prop1, prop2], [p1_1, p2_1] ],
#                                                             [ [prop1, prop2], [p1_1, p2_2] ],
#                                                             [ [prop1], [p1_2] ] ])
#                     print(hyp)
#                     hyp = Hypothesis(bin_num = 2, bins = [0, 1, 1], props=[ [ [prop1, prop2], [p1_1, p2_2] ],
#                                                             [ [prop1, prop2], [p1_1, p2_1] ],
#                                                             [ [prop1], [p1_2] ] ])
#                     print(hyp)
#                     hyp = Hypothesis(bin_num = 2, bins = [0, 1, 1], props=[ [ [prop1, prop2], [p1_1, p2_1] ],
#                                                             [ [prop1, prop2], [p1_1, p2_2] ],
#                                                             [ [prop1], [p1_2] ] ])
#                     print(hyp)
#                     hyp = Hypothesis(bin_num = 2, bins = [0, 1, 1], props=[ [ [prop1, prop2], [p1_1, p2_2] ],
#                                                             [ [prop1, prop2], [p1_1, p2_1] ],
#                                                             [ [prop1], [p1_2] ] ])
#                     print(hyp)
#                     print('')
#                     break
#     break
                
    

# card_order = []
# num_cards = 5
# for card in range(num_cards):
#     print('Number of Hypotheses', len(all_hyp))
#     #Pick the card that eliminates the most hypotheses
#     hyp_removed_arr = []
#     hyp_removed_ind_arr = []
#     for card in cards:
#         if card in card_order:
#             hyp_removed_arr.append(0)
#             hyp_removed_ind_arr.append([])
#         else:
#             hyp_removed, hyp_removed_ind = compute_hyp_removed(all_hyp, cards, true_hyp, card)
#             hyp_removed_arr.append(hyp_removed)
#             hyp_removed_ind_arr.append(hyp_removed_ind)
    
#     max_val = np.max(hyp_removed_arr)
#     max_inds = np.where(hyp_removed_arr == max_val)[0]
#     card_ind = np.random.choice(max_inds)

#     #Add card and remove hypotheses
#     card_order.append(cards[card_ind])
#     new_all_hyp = []
#     for hyp_ind, hyp in enumerate(all_hyp):
#         if not hyp_ind in hyp_removed_ind_arr[card_ind]:
#             new_all_hyp.append(hyp)
#     all_hyp = new_all_hyp

#     print('Card:', card_order[-1], 'in bin', true_hyp.sort_card(card_order[-1]))


