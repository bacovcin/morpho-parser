from Comb import *
from itertools import repeat

class word(object):
    def __init__(self,phon,morph):
        self.phonology = phon           #list of segments with features
        self.morphology = list(morph)   #ordered list of m-feature
                                        #sets  associated with word

class exponent(object):
        def __init__(self,phonology,side):
            self.phon = phonology       #phonology of exponent
            self.side = side            #adfix type [(p)refix,(s)uffix,(b)ase]
            

class vocab_item(object):
    def __init__(self,morph_feature,phonology,side,context):
        self.morph_feature = morph_feature       #m-feature to be spelled out
        self.exponent = exponent(phonology,side) #exponent and adfix status
        self.context = context                   #when to use this item
        
class settings(object):
    def __init__(self, length, phon):
        self.vlength = length         #weight of the list length penalty
        self.phon = phon             #weight of the phonology vs. allomorphy 
                                     #penalty, which can be negative

class model(object):
    def __init__(self, vocab, mprules):
        self.vocab = vocab
        self.mprules = mprules

def Dictionaryify(input):
    lexicon = {} 
    for word in input:
        for morph in word.morphology:
            try:
                lexicon[morph[0]][morph[1]].append(word)
            except:
                try:
                    lexicon[morph[0]][morph[1]] = [word]
                except:
                    lexicon[morph[0]] = {morph[1]:[word]}
    return lexicon

def find_common_substring(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    for j in range(len(long_string)):
        for i in range(len(long_string),-1,-1):
            if len(long_string[j:i]) > len(result):
                if is_common_substr(long_string[j:i],word_list):
                    result = long_string[j:i]
    return result

def find_common_prefix(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string

    result = ''
    i = len(long_string)
    for j in range(len(long_string)):
        if len(long_string[j:i]) > len(result):
            if is_common_substr(long_string[j:i],word_list):
                result = long_string[j:i]
    return result

def find_common_suffix(word_list):
    is_common_substr = lambda s, strings: all(s in x for x in strings)
    long_string = ""
    for string in word_list:
        if len(string) > len(long_string):
            long_string = string
    result = ''
    j = 0
    for i in range(len(long_string),-1,-1):
        if len(long_string[j:i]) > len(result):
            if is_common_substr(long_string[j:i],word_list):
                result = long_string[j:i]
    return result

def add_mprules(vocab):
    '''adds morpho-phonological rules to models that fail to generate the data with only contextual allomorphy'''
    pass

def create_model_space(lexicon, ordering):
    listOfTypeModels = []
    for i in range(len(ordering)):
        type = ordering[i]
        listOfMorphs = []
        if i == 0:
            side = 'b'
        else:
            side = ['s','p']
        for morph in lexicon[type]:
            setOfTriggers = set(frozenset(lexicon[y].keys())
                                for y in set(ordering) - set([type]))
            trueSet = set()
            for x in set(product(set_combs(x) for x in setOfTriggers)):
                trueSet.add(frozenset(frozenset(z for a in y for z in a) for y in list(product(x))))
            listOfMorphs.append(list(product([[morph],product([side,list(trueSet)])])))
        listOfTypeModels.append(list(product([[type],list(product(listOfMorphs))])))
        try:
            i = i + 1
            print i
        except:
            i = 1
            print i
    return list(product(listOfTypeModels))

def check_vocab(vocab,lexicon):
    for type in lexicon.keys():
        for key in lexicon[type].keys():
            for word in lexicon[type][key]:
                morphs = tuple(y[1] for y in word.morphology)
                phonology = ''
                for morph_list in vocab:
                    for item in morph_list:
                        if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                            if item.exponent.side == 'b':
                                phonology = item.exponent.phon
                            elif item.exponent.side == 'p':
                                phonology = item.exponent.phon + phonology
                            elif item.exponent.side == 's':
                                phonology = phonology + item.exponent.phon
                if phonology != word.phonology:
                    return False
    return True

def build_models(modelSpace, lexicon):
    models = []
    for i in range(len(modelSpace)):
        curModel = modelSpace[i]
        vocab = []
        for j in range(len(curModel)):
            curMorphType = curModel[j]
            type = curMorphType[0]
            for k in range(len(curMorphType[1])):
                curMorph = curMorphType[1][k]
                side = curMorph[1][0]
                morph = curMorph[0]
                if j == 0:
                    for subSet in list(x for x in curMorph[1][1]):
                        #raw_input(curMorph[1][1])
                        words = [x.phonology for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(subSet)]
                        #print subSet
                        #print str(list(set(set([y[1] for y in x.morphology])-set([morph])) for x in lexicon[type][morph]))
                        #raw_input(words)
                        try:
                            vocab[j].append(vocab_item(morph,find_common_substring(words),'b',list(subSet)))
                        except:
                            vocab.append([vocab_item(morph,find_common_substring(words),'b',list(subSet))])
                else:
                    vocab.append([])
                    for subSet in curMorph[1][1]:
                        fullWords = [x for x in lexicon[type][morph] if set(set([y[1] for y in x.morphology])-set([morph])).issubset(set(subSet))]
                        before = set([])
                        after = set([])
                        for word in fullWords:
                            morphs = tuple(y[1] for y in word.morphology)
                            phon = ''
                            for l in range(j):
                                for item in vocab[l]:
                                    if (item.morph_feature in morphs) and (False not in list(x in set(item.context) for x in set(morphs)-set([item.morph_feature]))):
                                        if item.exponent.side == 'b':
                                            phon = item.exponent.phon
                                        elif item.exponent.side == 'p':
                                            phon = item.exponent.phon + phon
                                        elif item.exponent.side == 's':
                                            phon = phon + item.exponent.phon
                            try:
                                splice = word.phonology.split(phon)
                            except:
                                splice = [word.phonology,word.phonology]
                            before.add(splice[0])
                            after.add(phon.join(splice[1:]))
                        if side == 's':
                            vocab[j].append(vocab_item(morph,find_common_suffix(after),'s',list(subSet)))
                        if side == 'p':
                            vocab[j].append(vocab_item(morph,find_common_prefix(before),'p',list(subSet)))
                    #for key in vocab[j][-1].__dict__.keys():
                    #    if key == 'exponent':
                    #        for key2 in vocab[j][-1].exponent.__dict__.keys():
                    #            print vocab[j][-1].exponent.__dict__[key2]
                    #    else:
                    #        print vocab[j][-1].__dict__[key]
                    #raw_input(1)
        if check_vocab(vocab,lexicon):
            try:
                sucess = sucess + 1
            except:
                sucess = 1
            models.append(model(list(y for x in vocab for y in x),[]))
        else:
            try:
                fail = fail + 1
            except:
                fail = 1
            mprules = add_mprules(vocab)
        print str("%.2f" % ((float(i)/float(len(modelSpace)))*float(100))) + '% complete'
    print 'Success: ' + str(sucess)
    print 'Fail: ' + str(fail)
    return models

def check_models(models,settings):
    "checks for the smallest model, and returns a list of the smallest models"
    for i in range(len(models)):
        model = models[i]
        try:
            if cur_len > (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon):
                cur_len = (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon)
        except:
            cur_len = (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon)
    smallest = []
    i = 0
    for i in range(len(models)):
        model = models[i]
        if (len(model.vocab)*settings.vlength + len(model.mprules)*settings.phon) == cur_len:
            i = i + 1
            smallest.append(model)
    print i
    return smallest
