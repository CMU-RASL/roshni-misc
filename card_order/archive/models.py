import numpy as np

class Card():
    def __init__(self, color, number, shape, shading):
        self.color = color
        self.number = number
        self.shape = shape
        self.shading = shading
        self.attr = {'color': color, 'number': number, 'shape': shape, 'shading': shading}
    def __str__(self):
        return '{}-{}-{}-{}'.format(self.color, self.number, self.shape, self.shading)

class Rule():
    def __init__(self, bin_num):
        self.bin_num = bin_num
        self.bins = []
        for bin in range(bin_num):
            self.bins.append(set([]))
    def add_card(self, card, bin):
        self.bins[bin].add(card)
    def bin_acc(self, card, test_card=None, test_bin=None):
        dist = []
        
        for bin in range(self.bin_num):
            #If already added, distance is 0
            if card in self.bins[bin] or card == test_card:
                dist.append(0.0)
            else:
                cur_dists = []
                incr = [1, 1, 1, 1]
                for bin_card in self.bins[bin]:
                    card_dist = 0.0
                    if not card.color == bin_card.color:
                        card_dist += incr[0]
                    if not card.number == bin_card.number:
                        card_dist += incr[1]
                    if not card.shape == bin_card.shape:
                        card_dist += incr[2]
                    if not card.shading == bin_card.shading:
                        card_dist += incr[3]
                    cur_dists.append(card_dist)
                if test_bin == bin:
                    card_dist = 0
                    if not card.color == test_card.color:
                        card_dist += incr[0]
                    if not card.number == test_card.number:
                        card_dist += incr[1]
                    if not card.shape == test_card.shape:
                        card_dist += incr[2]
                    if not card.shading == test_card.shading:
                        card_dist += incr[3]
                    cur_dists.append(card_dist)
                if len(cur_dists) > 0:
                    dist.append(np.mean(cur_dists))
                else:
                    dist.append(np.sum(incr))

        # already_added = False
        # for bin in range(self.bin_num):
        #     if test_card in self.bins[bin]:
        #         already_added = True

        # for bin in range(self.bin_num):
        #     if already_added:
        #         if card in self.bins[bin]:
        #             dist.append(0)
        #         else:
        #             cur_dists = []
        #             for bin_card in self.bins[bin]:
        #                 card_dist = 0
        #                 if not card.color == bin_card.color:
        #                     card_dist += 1
        #                 if not card.number == bin_card.number:
        #                     card_dist += 1
        #                 if not card.shape == bin_card.shape:
        #                     card_dist += 1
        #                 if not card.shading == bin_card.shading:
        #                     card_dist += 1
        #                 cur_dists.append(card_dist)
        #             if len(cur_dists) > 0:
        #                 dist.append(np.mean(cur_dists))
        #             else:
        #                 dist.append(0)
        #     else:
        #         if card in self.bins[bin] or test_card in self.bins[bin]:
        #             dist.append(0)
        #         else:
        #             cur_dists = []
        #             for bin_card in self.bins[bin]:
        #                 card_dist = 0
        #                 if not card.color == bin_card.color:
        #                     card_dist += 1
        #                 if not card.number == bin_card.number:
        #                     card_dist += 1
        #                 if not card.shape == bin_card.shape:
        #                     card_dist += 1
        #                 if not card.shading == bin_card.shading:
        #                     card_dist += 1
        #                 cur_dists.append(card_dist)
        #             if test_bin==bin:
        #                 card_dist = 0
        #                 if not card.color == test_card.color:
        #                     card_dist += 1
        #                 if not card.number == test_card.number:
        #                     card_dist += 1
        #                 if not card.shape == test_card.shape:
        #                     card_dist += 1
        #                 if not card.shading == test_card.shading:
        #                     card_dist += 1
        #                 cur_dists.append(card_dist)
        #             if len(cur_dists) > 0:
        #                 dist.append(np.mean(cur_dists))
        #             else:
        #                 dist.append(0)
        # min_val = np.min(dist)
        # min_idx = np.where(dist == min_val)[0]

        # return min_idx[0]
        if np.sum(dist) == 0:
            dist = np.array([0.5, 0.5])
        else:
            dist = dist/np.sum(dist)
        acc = 1 - dist
        return acc

class Hypothesis():
    def __init__(self, bin_num, bins):
        self.bin_num = bin_num       
        self.bin_rule = bins
        

    def sort_card(self, card):
        #For each bin
        bin_res = []
        for bin_ind, bin in enumerate(self.bin_rule):
            for row in bin: #one of these rows needs to be true
                flag = True
                for prop, val in row: #all of these need to be true
                    if not card.attr[prop] in val:
                        flag = False
                
                if flag:
                    bin_res.append(True)
                    break
            if len(bin_res) == bin_ind:
                bin_res.append(False)
        return bin_res

    def __str__(self):
        return str(self.bin_rule)

        
    