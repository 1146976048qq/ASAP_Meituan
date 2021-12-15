import numpy as np
from xml.etree import ElementTree
import json

# restaurant
train_path = 'dataset/SubTask2/restaurant/train.xml'
test_path = 'dataset/SubTask2/restaurant/test.xml'
train_output = 'processed/res_train.npy'
test_output = 'processed/res_test.npy'
order_output = 'processed/order.json'

class parseRES():
    mapfixed = 0
    aspect_map = {}
    columns_num = 0

    def __init__(self,filepath):
        self.root = ElementTree.parse(filepath).getroot()
        self.rolls_num = 0
        self.columns_num = 0
        self.aspect_map = {}
        self.get_aspects_statics()
    def get_aspects_statics(self):
        dic = {}
        roll = 0
        for child in self.root:
            for child1 in child:
                for sentence in child1:
                    roll += 1
                    for sentenceleaf in sentence:
                        if sentenceleaf.tag == 'Opinions':
                            for opinion in sentenceleaf:
                                if opinion.attrib['category'] in dic:
                                    dic[opinion.attrib['category']]+=1
                                else:
                                    dic[opinion.attrib['category']]=1
        self.rolls_num = roll
        if not parseRES.mapfixed:
            parseRES.mapfixed = 1
            parseRES.columns_num = len(dic) + 1
            for i,key in enumerate(dic.keys()):
                parseRES.aspect_map[key] = i+1
        self.columns_num = parseRES.columns_num
        self.aspect_map = parseRES.aspect_map
        return dic
    def get_numpy(self):
        x = -1*np.ones((self.rolls_num,self.columns_num),dtype=object)
        roll = 0
        for child in self.root:
            for child1 in child:
                for sentence in child1:
                    for sentenceleaf in sentence:
                        if sentenceleaf.tag == 'text':
                            x[roll,0] = sentenceleaf.text
                        if sentenceleaf.tag == 'Opinions':
                            for opinion in sentenceleaf:
                                if opinion.attrib['polarity']=='negative':
                                    x[roll,self.aspect_map[opinion.attrib['category']]] = 0
                                elif opinion.attrib['polarity']=='positive':
                                    x[roll,self.aspect_map[opinion.attrib['category']]] = 2
                                elif opinion.attrib['polarity']=='neutral':
                                    x[roll,self.aspect_map[opinion.attrib['category']]] = 1
                    roll += 1
        return x
#print(parseRES(train_path).rolls_num)
np.save(test_output,parseRES(test_path).get_numpy())
np.save(train_output,parseRES(train_path).get_numpy())
with open(order_output,'w') as f:
    json.dump(parseRES.aspect_map,f)