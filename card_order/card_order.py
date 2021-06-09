import numpy as np
from utils import card_str, calc_hyp_removed, sort_card, hyp_str, all_props, create_all_cards, create_all_hypotheses, create_card_order
import matplotlib.pyplot as plt

def one_order():
    #Initialize cards and hypotheses
    cards = create_all_cards()
    all_hyp = create_all_hypotheses()

    #True hypothesis
    blank_hyp = np.zeros((2, 10, 4, 3))

    #True hypothesis - diamonds on left, all others on right
    true_hyp = np.copy(blank_hyp)
    true_hyp[0, 0, 2, 0] = 1
    true_hyp[1, 0, 2, 1] = 1
    true_hyp[1, 1, 2, 2] = 1

    #True hypothesis - green-one, red/purple on left, green two/three on right
    # true_hyp = np.copy(blank_hyp)
    # true_hyp[0, 0, 0, 1] = 1 #green
    # true_hyp[0, 0, 3, 0] = 1 #one
    # true_hyp[0, 1, 0, 0] = 1 #red
    # true_hyp[0, 1, 0, 2] = 1 #purple

    # true_hyp[1, 0, 0, 1] = 1 #green
    # true_hyp[1, 0, 3, 1] = 1 #two
    # true_hyp[1, 0, 3, 2] = 1 #three

    card_num = 10
    res = create_card_order(card_num, true_hyp, all_hyp, cards)
    print(res[0])
    print(res[-1])


def create_plots():

    #Initialize cards and hypotheses
    cards = create_all_cards()
    all_hyp = create_all_hypotheses()

    #True hypothesis
    blank_hyp = np.zeros((2, 10, 4, 3))

    #True hypothesis - diamonds on left, all others on right
    # true_hyp = np.copy(blank_hyp)
    # true_hyp[0, 0, 2, 0] = 1
    # true_hyp[1, 0, 2, 1] = 1
    # true_hyp[1, 1, 2, 2] = 1

    #True hypothesis - green-one, red/purple on left, green two/three on right
    true_hyp = np.copy(blank_hyp)
    true_hyp[0, 0, 0, 1] = 1 #green
    true_hyp[0, 0, 3, 0] = 1 #one
    true_hyp[0, 1, 0, 0] = 1 #red
    true_hyp[0, 1, 0, 2] = 1 #purple

    true_hyp[1, 0, 0, 1] = 1 #green
    true_hyp[1, 0, 3, 1] = 1 #two
    true_hyp[1, 0, 3, 2] = 1 #three

    card_num = 10

    tot_iters = 100
    all_card_orders = []
    all_num_hypotheses = []
    all_equiv_cards = []
    all_prob = []
    for iter in range(tot_iters):
        print('Starting iter', iter+1, 'out of', tot_iters)
        res = create_card_order(card_num, true_hyp, all_hyp, cards)
        all_card_orders.append(res[0])
        all_num_hypotheses.append(res[1])
        all_equiv_cards.append(res[2])
        all_prob.append(res[3])

    all_prob = np.vstack(all_prob)
    all_num_hypotheses = np.vstack(all_num_hypotheses)
    all_equiv_cards = np.vstack(all_equiv_cards)

    prob_mean = np.mean(all_prob, axis=0)
    hypotheses_mean = np.mean(all_num_hypotheses, axis=0)
    equiv_cards_mean = np.mean(all_equiv_cards, axis=0)

    prob_std = np.std(all_prob, axis=0)
    hypotheses_std = np.std(all_num_hypotheses, axis=0)
    equiv_cards_std = np.std(all_equiv_cards, axis=0)


    fig, ax = plt.subplots(3, 1)

    ax[0].errorbar(np.arange(card_num), prob_mean, yerr=prob_std)
    ax[0].set_title('Number of Iterations ' + str(tot_iters) + ' with 1-std around mean shown')
    ax[0].set_ylabel('Probability of Choosing Correct Bin')

    ax[1].errorbar(np.arange(card_num), hypotheses_mean, yerr=hypotheses_std)
    ax[1].set_ylabel('Number of Remaining Hypotheses before card')

    ax[2].errorbar(np.arange(card_num), equiv_cards_mean, yerr=equiv_cards_std)
    ax[2].set_ylabel('Number of Equivalent Cards')

    plt.show()


one_order()
