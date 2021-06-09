import numpy as np
from utils import card_str, calc_hyp_removed, sort_card, hyp_str

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
blank_hyp1 = np.zeros((2, 1, 4, 3))
blank_hyp2 = np.zeros((2, 2, 4, 3))

#True hypothesis - ovals on left, all others on right
# true_hyp = np.copy(blank_hyp1)
# true_hyp[0, 0, 2, 1] = 1
# true_hyp[1, 0, 2, 0] = 1
# true_hyp[1, 0, 2, 2] = 1

#True hypothesis - red-one, green/purple on left, red two/three on right
true_hyp = np.copy(blank_hyp2)
# true_hyp[0, 0, 0, 1] = 1
# true_hyp[0, 1, 0, 2] = 1
# true_hyp[0, 2, 0, 0] = 1
# true_hyp[0, 2, 3, 0] = 1

# true_hyp[]



# true_hyp[0, 0, 0, 0] = 1
# true_hyp[0, 0, 3, 0] = 1
# true_hyp[0, 1, 0, 1] = 1
# true_hyp[0, 1, 0, 2] = 1

# true_hyp[1, 0, 0, 0] = 1
# true_hyp[1, 0, 3, 1] = 1
# true_hyp[1, 0, 3, 2] = 1

all_hyp = []

#Separated by one prop
for prop in range(4):
    for bin0, bin1 in zip([0, 1], [1, 0]):

        #0 value on the left, 1 and 2 value on the right
        hyp = np.copy(blank_hyp1)
        hyp[bin0,0,prop,0] = 1
        hyp[bin1,0,prop,[1,2]] = 1
        all_hyp.append(hyp)

        #1 value on the left, 0 and 2 value on the right
        hyp = np.copy(blank_hyp1)
        hyp[bin0,0,prop,1] = 1
        hyp[bin1,0,prop,[0,2]] = 1
        all_hyp.append(hyp)

        #2 value on the left, 0 and 1 value on the right
        hyp = np.copy(blank_hyp1)
        hyp[bin0,0,prop,2] = 1
        hyp[bin1,0,prop,0] = 1
        hyp[bin1,0,prop,1] = 1
        all_hyp.append(hyp)

#Separated by two props

for prop1 in range(4):
    for prop2 in range(4):
        if not prop1 == prop2:
            for bin0, bin1 in zip([0, 1], [1, 0]):
                for prop1val in range(3):
                    for bin_1 in range(2):
                        ##
                        hyp = np.copy(blank_hyp2)
                        hyp[bin0,0,prop1,prop1val] = 1
                        hyp[bin0,0,prop2,0] = 1
                        hyp[bin1,0,prop1,prop1val] = 1
                        hyp[bin1,0,prop2,[1,2]] = 1

                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin_1,1,prop1,prop1val_2] = 1
                        all_hyp.append(hyp)

                        hyp = np.copy(blank_hyp2)
                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin0,0,prop1,prop1val_2] = 1
                                hyp[bin0,0,prop2,0] = 1
                                hyp[bin1,0,prop1,prop1val_2] = 1
                                hyp[bin1,0,prop2,[1,2]] = 1

                        hyp[bin_1,1,prop1,prop1val] = 1

                        all_hyp.append(hyp)
                        ##
                        hyp = np.copy(blank_hyp2)
                        hyp[bin0,0,prop1,prop1val] = 1
                        hyp[bin0,0,prop2,1] = 1
                        hyp[bin1,0,prop1,prop1val] = 1
                        hyp[bin1,0,prop2,0] = 1
                        hyp[bin1,0,prop2,2] = 1

                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin_1,1,prop1,prop1val_2] = 1
                        all_hyp.append(hyp)
                        
                        hyp = np.copy(blank_hyp2)
                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin0,0,prop1,prop1val_2] = 1
                                hyp[bin0,0,prop2,1] = 1
                                hyp[bin1,0,prop1,prop1val_2] = 1
                                hyp[bin1,0,prop2,0] = 1
                                hyp[bin1,0,prop2,2] = 1

                        hyp[bin_1,1,prop1,prop1val] = 1

                        all_hyp.append(hyp)
                        
                        ##
                        hyp = np.copy(blank_hyp2)
                        hyp[bin0,0,prop1,prop1val] = 1
                        hyp[bin0,0,prop2,2] = 1
                        hyp[bin1,0,prop1,prop1val] = 1
                        hyp[bin1,0,prop2,0] = 1
                        hyp[bin1,0,prop2,1] = 1

                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin_1,1,prop1,prop1val_2] = 1
                        all_hyp.append(hyp)
                        
                        hyp = np.copy(blank_hyp2)
                        for prop1val_2 in range(3):
                            if not prop1val == prop1val_2:
                                hyp[bin0,0,prop1,prop1val_2] = 1
                                hyp[bin0,0,prop2,2] = 1
                                hyp[bin1,0,prop1,prop1val_2] = 1
                                hyp[bin1,0,prop2,0] = 1
                                hyp[bin1,0,prop2,1] = 1

                        hyp[bin_1,1,prop1,prop1val] = 1

                        all_hyp.append(hyp)
                        

#Card order
card_num = 10
card_order = -1*np.ones((card_num)).astype('int')
for ind in range(card_num):
    print('Num Hypotheses:', len(all_hyp))
    #Find number of hypotheses eliminated by each card
    num_hyp_removed = -1*np.ones((81))
    hyp_removed_ind = []
    for test_card in range(81):
        if test_card in card_order:
            num_hyp_removed[test_card] = -10
            hyp_removed_ind.append([])
        else:
            tmp1, tmp2 = calc_hyp_removed(all_hyp, true_hyp, cards[test_card,:,:])
            num_hyp_removed[test_card] = tmp1
            hyp_removed_ind.append(tmp2)
    
    max_val = np.max(num_hyp_removed)
    max_inds = np.where(num_hyp_removed == max_val)[0]
    print(len(max_inds))
    card_ind = np.random.choice(max_inds)

    #Add card and remove hypotheses
    card_order[ind] = card_ind
    new_all_hyp = []
    for hyp_ind, hyp in enumerate(all_hyp):
        if not hyp_ind in hyp_removed_ind[card_ind]:
            new_all_hyp.append(hyp)
    all_hyp = new_all_hyp
    print(card_order[ind], card_str(cards[card_order[ind],:,:], props))
    # print(hyp_str(all_hyp[0], props))
    # print(' ')
