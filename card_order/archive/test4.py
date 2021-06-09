import numpy as np
from utils import card_str, calc_hyp_removed, sort_card, hyp_str
from itertools import product

#Initialize cards
props = [['red', 'green', 'purple'],['open', 'striped', 'solid'],['diamond', 'oval', 'squiggle'],['one', 'two', 'three']]
cards = np.zeros((81, 4, 3))
card_ind = 0
for color in range(3):
    for shading in range(3):
        for shape in range(3):
            for number in range(3):
                cards[card_ind, 0, color] = 1
                cards[card_ind, 1, shading] = 1
                cards[card_ind, 2, shape] = 1
                cards[card_ind, 3, number] = 1
                card_ind += 1


#Initialize hypotheses - bin, row, prop, val
blank_hyp = np.zeros((2, 10, 4, 3))

#True hypothesis - diamonds on left, all others on right
true_hyp = np.copy(blank_hyp)
true_hyp[0, 0, 2, 0] = 1
true_hyp[1, 0, 2, 1] = 1
true_hyp[1, 1, 2, 2] = 1

#True hypothesis - green-one, red/purple on left, green two/three on right
# true_hyp = np.copy(blank_hyp)
# true_hyp[0, 0, 0, 0] = 1 #red
# true_hyp[0, 1, 0, 2] = 1 #purple
# true_hyp[0, 2, 0, 1] = 1 #green
# true_hyp[0, 2, 3, 0] = 1 #one

# true_hyp[1, 0, 0, 1] = 1 #green
# true_hyp[1, 0, 3, 1] = 1 #two
# true_hyp[1, 1, 0, 1] = 1 #green
# true_hyp[1, 1, 3, 2] = 1 #three

# true_hyp[]
all_hyp = []


options = list(product(range(2), repeat=9))
#Separated by two prop
for prop1 in range(4):
    for prop2 in range(4):
        if prop1 > prop2:
            #All possible combos
            for option in options:
                bin0_count = 0
                bin1_count = 0
                hyp = np.copy(blank_hyp)
                for prop1val, prop2val, bin in zip([0, 0, 0, 1, 1, 1, 2, 2, 2], [0, 1, 2, 0, 1, 2, 0, 1, 2], option):
                    if bin == 0:
                        hyp[bin, bin0_count, prop1, prop1val] = 1
                        hyp[bin, bin0_count, prop2, prop2val] = 1
                        bin0_count += 1
                    else:
                        hyp[bin, bin1_count, prop1, prop1val] = 1
                        hyp[bin, bin1_count, prop2, prop2val] = 1
                        bin1_count += 1
                all_hyp.append(hyp)

#Card order
card_num = 10
card_order = np.zeros((card_num)).astype('int')
num_bins = np.array([0, 0])
for ind in range(card_num):
    
    print('Num Hypotheses:', len(all_hyp))

    #Find number of hypotheses eliminated by each card
    num_hyp_removed = np.zeros((81))
    hyp_removed_ind = []
    for test_card in range(81):
        if test_card in card_order:
            num_hyp_removed[test_card] = -10
            hyp_removed_ind.append([])
        else:
            tmp1, tmp2 = calc_hyp_removed(all_hyp, true_hyp, cards[test_card,:,:])
            num_hyp_removed[test_card] = tmp1
            hyp_removed_ind.append(tmp2)
        if test_card%10 == 0:
            print('Processed Card', test_card, 'out of 81')
    
    max_val = np.max(num_hyp_removed)
    max_inds = np.where(num_hyp_removed == max_val)[0]
    print('Equivalent Cards:', len(max_inds))

    #Find bins these cards belong in
    # if np.sum(num_bins) == 0:
    #     probs = 0.5*np.ones((2))
    # else:
    #     probs = num_bins/np.sum(num_bins)
    # probs = 1 - probs
    # p = []
    # for equiv_ind in max_inds:
    #     bin = sort_card(true_hyp, cards[equiv_ind, :, :])
    #     p.append(probs[bin])
    # p = np.array(p)/np.sum(p)

    card_ind = np.random.choice(max_inds)

    #Add card and remove hypotheses
    card_order[ind] = card_ind
    new_all_hyp = []
    for hyp_ind, hyp in enumerate(all_hyp):
        if not hyp_ind in hyp_removed_ind[card_ind]:
            new_all_hyp.append(hyp)
    all_hyp = new_all_hyp

    if len(all_hyp) < 10:
        for hyp in all_hyp:
            print(hyp_str(hyp, props))

    current_bin = sort_card(true_hyp, cards[card_order[ind],:,:])
    num_bins[current_bin] += 1
    print('Chosen card:', card_order[ind], card_str(cards[card_order[ind],:,:], props), 'Bin', current_bin)
    print(' ')
