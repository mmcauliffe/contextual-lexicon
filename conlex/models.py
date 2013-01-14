from bulbs.model import Node, Relationship
from bulbs.property import String,Integer

#Basic test classes
#~ class Word(Node):
    #~ element_type= "word"
    #~
    #~ name = String(nullable=False)
    #~ count = Integer(nullable=True)
    #~
    #~ def get_count(self):
        #~ return sum([x.count for x in self.inE("precedes")])
        #~
    #~ def get_contexts(self):
        #~ return {x.outV().name:x.count for x in self.inE("precedes")}
    #~
#~ class Precedes(Relationship):
    #~ label = "precedes"
    #~
    #~ count = Integer()

class Word(Node):
    element_type= "word"

    #~ word = Integer(nullable=False)
    word = String(nullable=False)
    count = Integer(nullable=True)

    def get_bigram_count(self):
        return sum([x.count for x in self.inE("bigram")])

    def get_bigram_contexts(self):
        return {x.outV().word:x.count for x in self.inE("bigram")}

    def get_trigram_count(self):
        return sum([x.count for x in self.inE("trigram")])

    def get_trigram_contexts(self):
        return {(x.outV().word,x.middle_word):x.count for x in self.inE("trigram")}

class Bigram(Relationship):
    label = "bigram"

    count = Integer()

class Trigram(Relationship):
    label = "trigram"

    count = Integer()
    #middle_word = Integer()
    middle_word = String(nullable=False)
