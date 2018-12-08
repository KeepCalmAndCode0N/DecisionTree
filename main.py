import pandas as pd
import numpy as np


isContinuous={'Pclass':False,'Sex':False,'Age':True,'SibSp':True,'Parch':True,'Ticket':True,'Cabin':True,'Fare':True,'Embarked':False}
attributeList=[]

class treeNode:
    attribute=None
    sonNum=0
    sons=None
    splitValue=None
    isLeaf=False
    type=None
    data=None

    def __init__(self,data=None,isLeaf=False,attribute=None,type=None):
        self.isLeaf=isLeaf
        self.attribute=attribute
        self.type=type
        self.sonNum = 0
        self.data=data

    def __init


    def calEntropy(self,d):
        valueList=d.ix[:,'Survived'].unique().tolist()
        ent=0.0
        for value in valueList:
            p=float(d[d['Survived']==value].shape[0])/d.shape[0]
            logp=np.log2(p)
            ent-=p*logp
        return ent

    def testAttribute(self):
        partitionDataList={}
        attributeMiniEnt={}
        splitValueList={}
        for attribute in attributeList:
            valueList=sorted(self.data.ix[:,attribute].unique().tolist())
            if(isContinuous[attribute]):
                miniEnt=10.0
                splitValue=None
                for value in valueList:
                    part1=self.data[self.data[attribute]<=value]
                    part2=self.data[self.data[attribute]>value]
                    part1Ent=self.calEntropy(part1)
                    part2Ent=self.calEntropy(part2)
                    ent=(float(part1.shape[0])/self.data.shape[0]*part1Ent)+(float(part2.shape[0])/self.data.shape[0]*part2Ent)
                    if(ent<miniEnt):
                        miniEnt=ent
                        splitValue=value
                splitValueList[attribute]=splitValue
                partitionDataList[attribute]=[self.data[self.data[attribute]<=splitValue],self.data[self.data[attribute]>splitValue]]
                attributeMiniEnt[attribute]=miniEnt
            else:
                attributeMiniEnt[attribute]=0.0
                dataList=[]
                for value in valueList:
                    part=self.data[self.data[attribute]==value]
                    dataList.append(part)
                    partEnt=self.calEntropy(part)
                    attributeMiniEnt[attribute]+=float(part.shape[0])/self.data.shape[0]*partEnt
                partitionDataList[attribute]=dataList

        bestAttribute=min(attributeMiniEnt,key=attributeMiniEnt.get)
        return bestAttribute,partitionDataList[bestAttribute],splitValueList[bestAttribute]


def GenerateDecisionTree(data,attributeList):
    node=treeNode(data=data)
    #数据中只有一类值
    if len(data.ix[:,'Survived'].unique().tolist()) == 1:
        node.isLeaf=True
        node.type=data.at([0],['Survived'])
        return node
    #没有待选属性
    if len(attributeList) == 0:
        node.isLeaf=True
        node.type=data.ix[:,'Survived'].value_counts().index[0]
        return node

    attribute,partitionDataList,splitValue=node.testAttribute()
    node.attribute=attribute
    if(~isContinuous[attribute]):
        attributeList.remove(attribute)
    for num in range(0,len(partitionDataList)):
        partData=partitionDataList[num]
        if partData.empty:
            if(isContinuous[attribute]):
                node.sons=[1,2]
                node.splitValue=splitValue
                leafnode=treeNode(isLeaf=True,type=partData.ix[:,'Survived'].value_counts().index[0])
                node.sons[num]=leafnode
            else:
                valueList = sorted(data.ix[:, attribute].unique().tolist())
                node.sons={}
                leafnode=treeNode(isLeaf=True,type=partData.ix[:,'Survived'].value_counts().index[0])
                node.sons[valueList[num]]=leafnode
        else:











if __name__ == "__main__":
    train=pd.read_csv('./data/train.csv')
    print(train.columns.tolist())
    print(train[train['Ticket']=='111427'])
    print(train.ix[:,'Cabin'].value_counts().index[0])
    #print(train.ix[:, 'Cabin'].value_counts())
    survived, unsurvived = train.ix[:, 'Survived'].value_counts()
    print(train.shape[1])
    node=treeNode(train)
    print(node.calEntropy(train))
    attributeList=train.columns.tolist()[2:]
    attributeList.remove('Name')
    print(attributeList)

