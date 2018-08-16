
# coding: utf-8

# In[1]:


# Part 2: Python Skills (50%)
# Quiz 2-1: word counts (10%)
def ngram_probs(filename='raw_sentences.txt'):
    fo = open("raw_sentences.txt", "r")
    i=0
    BagofBigram={}
    BagofTrigram={}
    while True:
        i+=1
        line = fo.readline()
        if line=="":
            fo.close()
            break
        line = line.lower()
        line = line.split()
        for j in range(len(line)-2+1):
            #Add bigram in bag
            bigram=tuple(line[j:j+2])
            if bigram not in BagofBigram:
                BagofBigram[bigram]=1
            else: BagofBigram[bigram]+=1  
            
            #Add trigram in bag
            trigram=tuple(line[j:j+3])
            if trigram not in BagofTrigram:
                BagofTrigram[trigram]=1
            else: BagofTrigram[trigram]+=1
    
    #count probs 
    NofB=.0
    bigram_probs={}
    for key in BagofBigram:
        NofB+=BagofBigram[key]
    for key in BagofBigram:
        bigram_probs[key]=BagofBigram[key]/NofB
    NofT=.0
    trigram_probs={}
    for key in BagofTrigram:
        NofT+=BagofTrigram[key]
    for key in BagofTrigram:
        trigram_probs[key]=BagofTrigram[key]/NofT 

#########################debugblock#####################
#     prob=0
#     for key in bigram_probs:
#         prob+=bigram_probs[key]
#        
#     print(prob)  
#     print(i)
#     print(NofB)
#     print(NofT)
#     print(len(BagofBigram))
#     print(len(BagofTrigram))
#     print(BagofBigram[("is",'going')])
#     print(bigram_probs[("is",'going')])
#     print(BagofTrigram[("is","going","to")])
#     print(trigram_probs[("is","going","to")])
#########################debugblock#####################

    bigram_probs, trigram_probs=bigram_probs,trigram_probs
    return bigram_probs, trigram_probs


# In[2]:


cnt2, cnt3=ngram_probs()
print(cnt2[("we","are")])


# In[3]:


# Quiz 2-2: next word probabilities (10%)
import math
def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    logof2=math.log(cnt2[bigram])
    prob={}
    for key in cnt3:
        if key[0:2]==bigram:
            prob[key[2]]=math.log(cnt3[key])-logof2

    return prob


# In[9]:


p=prob3(("we","are"))
p["family"]


# In[5]:


# Quiz 2-3: predicting the next word (10%)
def predict_max(starting, cnt2=cnt2, cnt3=cnt3):
    list_of_words=[]
    list_of_words=[]+list(starting)
    while True:
#     for i in range(1):##
        p=prob3(starting)
        pmax=max(list(p.values()))
        nextword=""
        for key in p:
            #假設最大likelihood對應的word只有一個
            if p[key]==pmax:
                nextword=key
#                 print(type(nextword))##
                list_of_words+=[nextword]
#                 print(list_of_words)##
        if list_of_words[-1]=="." or len(list_of_words)>=15:break
        starting=tuple(list_of_words[-2:])
    return list_of_words


# In[7]:


sent = predict_max(('we', 'are'))
assert sent[-1] == '.' or len(sent) <= 15
print(' '.join(sent))


# In[ ]:


# Quiz 2-4: beam search (20%)
# 不考慮句子短比句子長機率來的大，故不做平均
def predict_beam(bigram, beam_size=4, sent_length=10, cnt2=cnt2, cnt3=cnt3):
    list_of_sentence=[]
    sentence={}
    p=prob3(bigram)
    firstfour_p=list(p.values()).sort()[:beamsize]
    for key in p:
        if p[key] in firstfour_p:sentence[p[key]]=key
            
            ##Unfinished 
            
    while True:
        if len(list_of_sentence)>=4:break
        for props in sentence:
            bigram=sentence[props][-2:]
            p=prob3
    
    return list_of_sentence
##未完成，故把想法寫出，每一次找nextword時，
##要把「前幾次的log probability與最新的logprob加總起來」且找出的前n(beam_size)個機率最大值
##重複上述步驟直到句子結尾為句點或長度達10為找到一個句子直到找到n個


# In[ ]:


for sent in predict_beam(('we', 'are')):
assert sent[-1] == '.' or len(sent) < 10
print(' '.join(sent))


