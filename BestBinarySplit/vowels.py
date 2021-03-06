from copy import deepcopy

class Feature:
        Plus = 1
        Minus = 2
        NotSpecified = 5

def FeatureOpposite(featval):
        if featval == 1: return 2
        elif featval == 2: return 1
        else: return featval

GlobalFeats = ['high', 'low', 'front', 'back', 'round', 'ATR', 'long']

class Vowel:
        def __init__(self, char, high = Feature.NotSpecified, 
                        low = Feature.NotSpecified,
                        front = Feature.NotSpecified, 
                        back = Feature.NotSpecified,
                        round = Feature.NotSpecified, 
                        ATR = Feature.NotSpecified,
                        long = Feature.Minus):
                self._features = {}
                self._features['high'] = high
                self._features['front'] = front
                self._features['back'] = back
                self._features['low'] = low
                self._features['round'] = round
                self._features['ATR'] = ATR
                self._features['long'] = long
                self.symbol = char

        def __repr__(self):
                toReturn = '<Vowel-\'%s\': ' % self.symbol.encode('UTF-8')
                keys = self._features.keys()
                keys.sort()
                for f in keys:
                        if(self._features[f] == Feature.Plus):
                                toReturn += "+%s, "%f
                        elif(self._features[f] == Feature.Minus):
                                toReturn += "-%s, "%f
                        else: #Feature.NotSpecified
                           pass
                return toReturn[:-2] + ">" #remove last comma and space
                
        def __getitem__(self, key):
                '''Vowel[key]'''
                return self._features[key]
        def __setitem__(self, key, value):
                '''Vowel[key] = value'''
                self._features[key] = value
        def __eq__(self, other):
                '''Vowel == other'''
                if not isinstance(other, self.__class__):
                        return False
                for feat in self._features.keys():
                        if self._features[feat] != other._features[feat]:
                                return False
                return True
        def __ne__(self, other):
                '''Vowel != other'''
                return not self.__eq__(other)
        
def FindContrasts(vowels, feat, featset, trace = 0):
        '''Given the vowels, a featureset, and a feature, finds all the
        pairs of vowels that are contrastive for that feature'''
        pairs = []
        visited = []
        for vowel in [vow for vow in vowels if vow not in visited]:
                partner = deepcopy(vowel)
                partner[feat] = FeatureOpposite(vowel[feat])
                for v in [vow for vow in vowels if vow not in visited]:
                        match = reduce(lambda x,y: x and y,
                                       map(lambda feat:
                                           v[feat] == partner[feat],
                                           featset))
                        if trace > 0:
                                print vowel.symbol, "?=", v.symbol, match
                        if match:
                                pairs.append((vowel, v))
                                visited.append(vowel)
                                visited.append(v)
        return pairs

def rankFeatures(tiedFeatures, usedFeatures):
        ranks = {'low' : 0, 'high' : 1, 'back' : 2,
                  'front':3, 'round':4, 'ATR': 5, 'long': 6}

        #Deprecate height and front/backness if another feature exists
##        if 'low' in usedFeatures: ranks['high'] = ranks['high'] + 6
##        if 'high' in usedFeatures: ranks['low'] = ranks['low'] + 6
##        if 'front' in usedFeatures: ranks['back'] = ranks['back'] + 6
##        if 'back' in usedFeatures: ranks['front'] = ranks['front'] + 6

        #print ranks
        
        ranked = [(ranks[f],f) for f in tiedFeatures]
        ranked.sort()
        return [p[1] for p in ranked]

def FindBestSingle(matrix, relevantFeats):
        splits = {}
        for f in matrix:
                if not splits.has_key(matrix[f]): splits[matrix[f]] = []
                splits[matrix[f]].append(f)
        for k in splits: 
                if len(splits[k]) > 1: splits[k] = rankFeatures(splits[k],
                                                                relevantFeats)
        #print splits
        splits = [(k, splits[k]) for k in splits]
        splits.sort()
        return splits[0][1][0]

                        
def findBestSplit(sets, features, relevantFeats):
        if len(sets) == 1:
                return FindBestSingle(sets[0], relevantFeats)
        else:
                scores = {}
                for feature in features:
                        scoreList = []
                        for set in sets:
                                if set.has_key(feature):
                                         scoreList.append(set[feature])
                                else:
                                        scoreList = []
                                        break
                        if scoreList != []: scores[feature] = scoreList
                for key in scores:
                        scores[key] = sum(scores[key])/len(scores[key])
                return FindBestSingle(scores, relevantFeats)
                                

def splitSet(vowelsets, feature):
        newVowelSet = []
        for vowels in vowelsets:
                if isinstance(vowels, list):
                        plus = []
                        minus = []
                        for vowel in vowels:
                                if vowel[feature] == Feature.Plus:
                                        plus.append(vowel)
                                if vowel[feature] == Feature.Minus:
                                        minus.append(vowel) 
                        for sign in [plus, minus]:
                                if len(sign) > 1: newVowelSet.append(sign)
        return newVowelSet      
        

def distinguish(vowelsets, features = GlobalFeats, relevantFeats = []):
        results = []    
        for vowels in vowelsets:
                if isinstance(vowels, list):
                        print [v.symbol for v in vowels]
                        matrix = {}
                        for f in features:
                                matrix[f] = [v[f] for v in vowels]
                        for f in matrix:
                                matrix[f] = \
                                 max(float(matrix[f].count(Feature.Plus))/\
                                             len(matrix[f]),
                                     float(matrix[f].count(Feature.Minus))/\
                                             len(matrix[f]))
                        results.append((vowels, matrix))
        if results == []: return relevantFeats
        bestSplitFeat = findBestSplit([pairs[1] for pairs in results],
                                      features,
                                      relevantFeats)
        features.remove(bestSplitFeat)
        relevantFeats.append(bestSplitFeat)
        print bestSplitFeat, "\n###################\n"
        return distinguish(splitSet(vowelsets, bestSplitFeat),
                           features,
                           relevantFeats)


if __name__ == "__main__":
        i = Vowel("i", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        y = Vowel("y", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Plus)
        
        e = Vowel("e", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        slash_o = Vowel('slsh-o', high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Plus)
        
        epsilon = Vowel("epsil", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Minus)
        oe = Vowel("oe", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Plus, ATR = Feature.Minus)

        ash = Vowel("ae", high = Feature.Minus, front = Feature.Plus,
                        low = Feature.Plus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)

        u = Vowel("u", high = Feature.Plus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Plus)
        unround_u = Vowel("unrd-u", high = Feature.Plus, front = Feature.Minus,
                          low = Feature.Minus, back = Feature.Plus,
                          round = Feature.Minus, ATR = Feature.Plus)

        o = Vowel("o", high = Feature.Minus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Plus)
        baby_gamma= Vowel("b-gam", high = Feature.Minus, front = Feature.Minus,
                          low = Feature.Minus, back = Feature.Plus,
                          round = Feature.Minus, ATR = Feature.Plus)

        open_o = Vowel('opn-o', high = Feature.Minus, front = Feature.Minus,
                       low = Feature.Minus, back = Feature.Plus,
                       round = Feature.Plus, ATR = Feature.Minus)
        
        wedge = Vowel("wedge", high = Feature.Minus, front = Feature.Minus,
                             low = Feature.Minus, back = Feature.Plus,
                             round = Feature.Minus, ATR = Feature.Minus)


        schwa = Vowel("schwa", high = Feature.Minus, front = Feature.Minus,
                      low = Feature.Minus,back = Feature.Minus,
                      round = Feature.Minus, ATR = Feature.Plus)
        
        lax_i = Vowel("lax-i", high = Feature.Plus, front = Feature.Plus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Minus)
        lax_u = Vowel("lax-u", high = Feature.Plus, front = Feature.Minus,
                        low = Feature.Minus, back = Feature.Plus,
                        round = Feature.Plus, ATR = Feature.Minus)

        a = Vowel("a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Plus,
                  round = Feature.Minus, ATR = Feature.Minus)

        type_a = Vowel("typ-a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Minus,
                  round = Feature.Minus, ATR = Feature.Minus)

        round_a = Vowel("rnd-a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Plus,
                  round = Feature.Plus, ATR = Feature.Minus)
        
        atr_a = Vowel("atr-a", high = Feature.Minus, front = Feature.Minus,
                  low = Feature.Plus, back = Feature.Plus,
                  round = Feature.Minus, ATR = Feature.Plus)

        barred_i = Vowel("bar-i", high =Feature.Plus, front=Feature.Minus,
                        low = Feature.Minus, back = Feature.Minus,
                        round = Feature.Minus, ATR = Feature.Plus)
        
        
        shortVowels = [i, u, open_o, a]
        longVowels = []

        vowels = shortVowels

        for vowel in longVowels:
                curr = deepcopy(vowel)
                curr.symbol = curr.symbol + ":"
                curr._features["long"] = Feature.Plus
                vowels.append(curr)

        distinctiveFeats = distinguish([vowels])
        print "       ",
        for f in distinctiveFeats:
                print f, "\t",
        print ""
        for vowel in vowels:
                print "%(sym)6s " % {'sym': vowel.symbol.encode('UTF-8')},
                for f in distinctiveFeats:
                        if vowel[f] == Feature.Plus: print "+",
                        elif vowel[f] == Feature.Minus: print "-",
                        print "\t",
                print ""
        
        print "\nContrasts:"
        for feat in distinctiveFeats:
                print feat,":",
                pairs = FindContrasts(deepcopy(vowels), feat, distinctiveFeats)
                print [(x.symbol, y.symbol) for (x,y) in pairs]        
