import math

from bulbs.rexster import Graph
from bulbs.config import Config
from models import Word,Bigram,Trigram

def clear(g):
    if g.E is not None:
        e = [x.eid for x in g.E]
        for i in e:
            g.edges.delete(i)
    if g.V is not None:
        v = [x.eid for x in g.V]
        for i in v:
            g.vertices.delete(i)


def in_bigram_context_entropy(wordOne,wordTwo,g):
    ws = g.words.index.lookup(word=wordOne)
    if ws is None:
        return 'Error! Word one not found!'
    w_one = next(ws)
    ws = g.words.index.lookup(word=wordTwo)
    if ws is None:
        return 'Error! Word two not found!'
    w_two = next(ws)

    w_one_contexts = w_one.get_bigram_contexts()
    w_two_contexts = w_two.get_bigram_contexts()
    w_one_contexts.update({x:0 for x in w_two_contexts if x not in w_one_contexts})
    w_two_contexts.update({x:0 for x in w_one_contexts if x not in w_two_contexts})

    c_w_one = w_one.get_bigram_count()
    c_w_two = w_two.get_bigram_count()
    #print(c_w_one)
    #print(c_w_two)
    context_ent = [entropy_calc(c_w_one,c_w_two,
                                w_one_contexts[x],w_two_contexts[x]) for x in w_one_contexts]

    #print(context_ent)
    context_sum = sum(context_ent)
    #print(context_sum)
    return context_sum

def in_trigram_context_entropy(wordOne,wordTwo,g):
    ws = g.words.index.lookup(word=wordOne)
    if ws is None:
        return 'Error! Word one not found!'
    w_one = next(ws)
    ws = g.words.index.lookup(word=wordTwo)
    if ws is None:
        return 'Error! Word two not found!'
    w_two = next(ws)

    w_one_contexts = w_one.get_trigram_contexts()
    w_two_contexts = w_two.get_trigram_contexts()
    #print(w_one_contexts)
    #print(w_two_contexts)
    w_one_contexts.update({x:0 for x in w_two_contexts if x not in w_one_contexts})
    w_two_contexts.update({x:0 for x in w_one_contexts if x not in w_two_contexts})
    #print(w_one_contexts)
    #print(w_two_contexts)

    c_w_one = w_one.get_trigram_count()
    c_w_two = w_two.get_trigram_count()
    #print(c_w_one)
    #print(c_w_two)
    context_ent = [entropy_calc(c_w_one,c_w_two,
                                w_one_contexts[x],w_two_contexts[x]) for x in w_one_contexts]

    #print(context_ent)
    context_sum = sum(context_ent)
    #print(context_sum)
    return context_sum


def entropy_calc(cntOne,cntTwo,cntCOne,cntCTwo):
    pCGivenWords = (cntCOne + cntCTwo)/(cntOne + cntTwo)
    Entp = cntCOne / (cntCOne + cntCTwo)
    if Entp == 0.0:
        Entp = 0.0000001
    elif Entp == 1.0:
        Entp = 0.9999999
    HWordsGivenC = - (Entp * math.log(Entp)) - ((1-Entp) * math.log(1-Entp))
    return pCGivenWords * HWordsGivenC

def create_bigrams(g):
    bigrams = [('a','boy',130),
                ('every','boy',130),
                ('in','the',100),
                ('in','a',20),
                ('see','in',100),
                ('a','girl',150),
                ('some','girl',150),
                ('some','boy',10),
                ('one','girl',200),
                ('one','boy',10),
                ('the','girl',30)]
    for line in bigrams:
        ws =g.words.index.lookup(word=line[0])
        if ws is None:
            w_one = g.words.create(word=line[0])
        else:
            w_one = next(ws)
        ws = g.words.index.lookup(word=line[1])
        if ws is None:
            w_two = g.words.create(word=line[1])
        else:
            w_two = next(ws)
        bgs = w_one.outV("bigram")
        if bgs is None or w_two not in bgs:
            bg = g.bigram.create(w_one,w_two,count=line[2])

def create_trigrams(g):
    trigrams = [('a','red','boy',130),
                ('a','red','girl',150),
                ('some','blue','girl',150),
                ('some','red','boy',10),
                ('one','red','girl',200),
                ('one','blue','boy',10),
                ('the','red','girl',30)]
    for line in trigrams:
        ws =g.words.index.lookup(word=line[0])
        if ws is None:
            w_one = g.words.create(word=line[0])
        else:
            w_one = next(ws)
        ws = g.words.index.lookup(word=line[1])
        if ws is None:
            w_two = g.words.create(word=line[1])
        else:
            w_two = next(ws)
        ws = g.words.index.lookup(word=line[2])
        if ws is None:
            w_three = g.words.create(word=line[2])
        else:
            w_three = next(ws)
        trgs = w_one.outV("trigram")
        if trgs is None or w_three not in trgs:
            bg = g.trigram.create(w_one,w_three,middle_word=line[1],count=line[3])

def main():
    config = Config('http://localhost:8182/graphs/conlexgraph')
    g = Graph(config)
    #clear(g)
    g.add_proxy("words",Word)
    g.add_proxy("bigram",Bigram)
    g.add_proxy("trigram",Trigram)
    #create_bigrams(g)
    #create_trigrams(g)
    in_bigram_context_entropy('boy','girl',g)
    in_trigram_context_entropy('boy','girl',g)

if __name__ == '__main__':
    main()
