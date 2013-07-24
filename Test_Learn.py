from learn import *
import string
if __name__ == '__main__':
    word_list = [    
    word(r'c{\ae}ts',{'ROOT':'CAT','OTHER':['PL']}),
    word(r'b{\ae}t',{'ROOT':'BAT','OTHER':['SG']}),
    word(r'b{\ae}ts',{'ROOT':'BAT','OTHER':['PL']}),
    word(r'r{\ae}t',{'ROOT':'RAT','OTHER':['SG']}),
    word(r'r{\ae}ts',{'ROOT':'RAT','OTHER':['PL']}),
    word(r'fIS',{'ROOT':'FISH','OTHER':['SG']}),
    word(r'fIS9z',{'ROOT':'FISH','OTHER':['PL']}),
    word(r'toU',{'ROOT':'TOE','OTHER':['SG']}),
    word(r'toUz',{'ROOT':'TOE','OTHER':['PL']}),
    word(r'dAg',{'ROOT':'DOG','OTHER':['SG']}),
    word(r'dAgz',{'ROOT':'DOG','OTHER':['PL']}),
    word(r'fIS',{'ROOT':'FISH','OTHER':['PRESENT']}),
    word(r'fISIN',{'ROOT':'FISH','OTHER':['PRESENT PARTICIPLE']}),
    word(r'fISt',{'ROOT':'FISH','OTHER':['PAST']}),
    word(r'plej',{'ROOT':'PLAY','OTHER':['PRESENT']}),
    word(r'plejIN',{'ROOT':'PLAY','OTHER':['PRESENT PARTICIPLE']}),
    word(r'plejd',{'ROOT':'PLAY','OTHER':['PAST']}),
    word(r'wOk',{'ROOT':'WALK','OTHER':['PRESENT']}),
    word(r'wOkt',{'ROOT':'WALK','OTHER':['PAST']}),
    word(r'wOkIN',{'ROOT':'WALK','OTHER':['PRESENT PARTICIPLE']}),
    ]
    #setting = settings(1,1,3,2,5000,10000,2)
    #model = learn_vocab(word_list,debug=True)
    model = learn_vocab(word_list,iterate=True)
    #model = learn_vocab(word_list)