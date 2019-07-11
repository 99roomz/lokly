def parser(address):
    from nltk.tag.stanford import StanfordNERTagger
    stanford_ner_tagger = StanfordNERTagger(
        'model/model.ser.gz',
        'model/stanford-ner-3.9.2.jar'
    )

    def remove_punctuation(string):   
        sym = ['?', '!', '.','-','_','/',"\\",',',':','(',')','[',']',';','@','#','&','|','+']              
        out = ""
        for c in string:
            # check if this is the symbol we need to process
            if c in sym:
                tmp = ' '
                out = out + tmp
            else:
                out = out + c
        out1=out[0]
        for i in range(1,len(out)):
            if(out[i].isalpha() and not out[i-1].isalpha() ) or ( not out[i].isalpha() and out[i-1].isalpha()):
                out1+=" "
            out1+=out[i]
     
        return out1

    total = {}
    correct = {}
    incorrect = {}
    pred_data={}
    act_data={}
    import math      
    count=0
    variables=['HOUSE_NO','STREET','SUBLOCALITY_LEVEL_3' ,'SUBLOCALITY_LEVEL_2',  'SUBLOCALITY_LEVEL_1','NEIGHBORHOOD','CITY','STATE','COUNTRY','POSTAL']
    dict={}
    for x in variables:
      dict['{}'.format(x)]=""
      total[x] = 0
      correct[x] = 0
      incorrect[x] = 0 
      act_data[x]=[]
      pred_data[x]=[]
    d=[address]

    for i in range(len(d)):
      count+=1
      row = d[count-1]
      ad = str(row)
      l=remove_punctuation(ad).split()
      words = []
      for part in l:
        words.append(str(part).lower())
      li_tags = stanford_ner_tagger.tag(words)
      ad=str(ad)
      for x in variables:
        dict['{}'.format(x)]=""

        for temp in li_tags:
          if(str(temp[1]) == str(x)):
            dict['{}'.format(x)] = dict['{}'.format(x)] +temp[0]+" "
        dict['{}'.format(x)]=str(dict['{}'.format(x)].lstrip().rstrip())
        ad=str(ad)
    dict2={}
    variables1=['HOUSE_NO','STREET','SUBLOCALITY_LEVEL_3' ,'SUBLOCALITY_LEVEL_2',  'SUBLOCALITY_LEVEL_1','NEIGHBORHOOD','CITY','STATE','COUNTRY','POSTAL']
    variables2=['House No','Street','Micro Locality' ,'Sublocality','Locality','Neighbourhood','City','State','Country','Postal']
    for id in range(len(variables1)):
        dict2[variables2[id]] = dict[variables1[id]]
    return dict2