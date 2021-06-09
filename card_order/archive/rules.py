from itertools import combinations, product

color = ['red', 'green', 'purple']
shape = ['oval', 'diamond', 'squiggle']
number = ['one', 'two', 'three']
pattern = ['solid', 'blank', 'stripe']
all_properties = [color, shape, number, pattern]

def one_prop_rule(property):
    return [(p,) for p in property] + list(combinations(property, 2))

def two_prop_rule(property1, property2):
    return [p1 + p2 for p1, p2 in product(one_prop_rule(property1), one_prop_rule(property2))]

def card_position(c, s, n, p):
    return color.index(c) + 3*shape.index(s) + 9*number.index(n) + 27*pattern.index(p)

def generate_one_prop_hypotheses():
    hypotheses = []
    for property in all_properties:
        for rule in one_prop_rule(property):
            hypothesis = [0]*81
            hypotheses.append(hypothesis)
            for c in color:
                for s in shape:
                    for p in pattern:
                        for n in number:
                            if ((c in rule) or (s in rule) or (p in rule) or (n in rule)):
                                hypothesis[card_position(c, s, n, p)] = 1
            print(rule, sum(hypothesis))
            #print(hypothesis)
    return hypotheses

def generate_two_prop_hypotheses():
    hypotheses = []
    for property1, property2 in combinations(all_properties, 2):
        for rule in two_prop_rule(property1, property2):
            #print(property1, property2, rule)
            hypothesis = [0]*81
            hypotheses.append(hypothesis)
            for c in color:
                for s in shape:
                    for p in pattern:
                        for n in number:
                            if ((c in rule and s in rule) or (c in rule and p in rule) or (c in rule and n in rule) or
                                (s in rule and p in rule) or (s in rule and n in rule) or (p in rule and n in rule)):
                                hypothesis[card_position(c, s, n, p)] = 1
            print(rule, sum(hypothesis))
            #print(hypothesis)
    return hypotheses

#print(one_prop_rule(color))
#print(two_prop_rule(color, shape))
# print(len(generate_one_prop_hypotheses()))
print(len(generate_two_prop_hypotheses()))
