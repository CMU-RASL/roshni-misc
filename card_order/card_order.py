import numpy as np
from utils import card_str, calc_hyp_removed, sort_card, hyp_str, all_props, create_all_cards, create_all_hypotheses, create_card_order
import matplotlib.pyplot as plt
import os.path
from os import path

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
    return res

def create_plots(rule, tot_iters):
    name = 'card_order/' + rule + '_' + str(tot_iters)
    card_num = 10
    
    if path.exists(name+'.npz'):
        with np.load(name+'.npz') as data:
            all_prob=data['all_prob']
            all_num_hypotheses=data['all_num_hypotheses']
            all_equiv_cards=data['all_equiv_cards']
            all_prob_best=data['all_prob_best']
            all_num_hypotheses_best=data['all_num_hypotheses_best']
            all_equiv_cards_best=data['all_equiv_cards_best']
    else:
        #Initialize cards and hypotheses
        cards = create_all_cards()
        all_hyp = create_all_hypotheses()

        #True hypothesis
        blank_hyp = np.zeros((2, 10, 4, 3))
        
        if rule == 'easy':
            #True hypothesis - diamonds on left, all others on right
            true_hyp = np.copy(blank_hyp)
            true_hyp[0, 0, 2, 0] = 1
            true_hyp[1, 0, 2, 1] = 1
            true_hyp[1, 1, 2, 2] = 1
        else:
            #True hypothesis - green-one, red/purple on left, green two/three on right
            true_hyp = np.copy(blank_hyp)
            true_hyp[0, 0, 0, 1] = 1 #green
            true_hyp[0, 0, 3, 0] = 1 #one
            true_hyp[0, 1, 0, 0] = 1 #red
            true_hyp[0, 1, 0, 2] = 1 #purple

            true_hyp[1, 0, 0, 1] = 1 #green
            true_hyp[1, 0, 3, 1] = 1 #two
            true_hyp[1, 0, 3, 2] = 1 #three

        all_card_orders_best = []
        all_num_hypotheses_best = []
        all_equiv_cards_best = []
        all_prob_best = []
        all_card_orders = []
        all_num_hypotheses = []
        all_equiv_cards = []
        all_prob = []
        for iter in range(tot_iters):
            print('Starting iter', iter+1, 'out of', tot_iters)
            res = create_card_order(card_num, true_hyp, all_hyp, cards)
            all_card_orders_best.append(res[0])
            all_num_hypotheses_best.append(res[1])
            all_equiv_cards_best.append(res[2])
            all_prob_best.append(res[3])
            res = create_card_order(card_num, true_hyp, all_hyp, cards, best_card=False)
            all_card_orders.append(res[0])
            all_num_hypotheses.append(res[1])
            all_equiv_cards.append(res[2])
            all_prob.append(res[3])

        all_prob_best = np.vstack(all_prob_best)
        all_num_hypotheses_best = np.vstack(all_num_hypotheses_best)
        all_equiv_cards_best = np.vstack(all_equiv_cards_best)
        all_prob = np.vstack(all_prob)
        all_num_hypotheses = np.vstack(all_num_hypotheses)
        all_equiv_cards = np.vstack(all_equiv_cards)

    prob_mean = np.mean(all_prob, axis=0)
    hypotheses_mean = np.mean(all_num_hypotheses, axis=0)
    equiv_cards_mean = np.mean(all_equiv_cards, axis=0)
    prob_mean_best = np.mean(all_prob_best, axis=0)
    hypotheses_mean_best = np.mean(all_num_hypotheses_best, axis=0)
    equiv_cards_mean_best = np.mean(all_equiv_cards_best, axis=0)

    prob_std = np.std(all_prob, axis=0)
    hypotheses_std = np.std(all_num_hypotheses, axis=0)
    equiv_cards_std = np.std(all_equiv_cards, axis=0)
    prob_std_best = np.std(all_prob_best, axis=0)
    hypotheses_std_best = np.std(all_num_hypotheses_best, axis=0)
    equiv_cards_std_best = np.std(all_equiv_cards_best, axis=0)

    fig, ax = plt.subplots(3, 1)

    ax[0].errorbar(np.arange(card_num), prob_mean, yerr=prob_std)
    ax[0].errorbar(np.arange(card_num), prob_mean_best, yerr=prob_std_best)
    ax[0].set_title('Iterations ' + str(tot_iters) + ' with 1-std around mean shown')
    ax[0].set_ylabel('Prob')

    ax[1].errorbar(np.arange(card_num), hypotheses_mean, yerr=hypotheses_std)
    ax[1].errorbar(np.arange(card_num), hypotheses_mean_best, yerr=hypotheses_std_best)
    ax[1].set_ylabel('Hyp Remaining')

    ax[2].errorbar(np.arange(card_num), equiv_cards_mean, yerr=equiv_cards_std)
    ax[2].errorbar(np.arange(card_num), equiv_cards_mean_best, yerr=equiv_cards_std_best)
    ax[2].legend(['Suboptimal Card', 'Optimal Card'])
    ax[2].set_ylabel('Equiv Cards')

    plt.savefig(name+'.png')
    np.savez(name+'.npz', all_prob=all_prob, all_num_hypotheses=all_num_hypotheses, all_equiv_cards=all_equiv_cards,
                        all_prob_best=all_prob_best, all_num_hypotheses_best=all_num_hypotheses_best, all_equiv_cards_best=all_equiv_cards_best)


# res = one_order()
# fig, ax = plt.subplots(3, 1)
# ax[0].plot(np.arange(len(res[0])), res[-2])
# # ax[0].set_title('Iterations ' + str(tot_iters) + ' with 1-std around mean shown')
# ax[0].set_ylabel('Probability of Choosing Correct Bin')

# ax[1].plot(np.arange(len(res[0])), res[1])
# ax[1].set_ylabel('Remaining Hypotheses before card')

# ax[2].plot(np.arange(len(res[0])), res[-3])
# ax[2].set_ylabel('Equivalent Cards')

# plt.show()
create_plots('easy', 50)
create_plots('difficult', 50)