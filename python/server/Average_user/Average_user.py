#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import json


# In[2]:


def get_compressedData(listContent_One : list, listContent_Two : list, listHead : list):
    listVar = []
    for i in range(min(len(listContent_One), len(listContent_Two))):
        listVar.append( {listHead[0]:listContent_One[i], listHead[1]:listContent_Two[i]} )
    return listVar


# In[3]:


def save_fileInJSON(content ,strRoot : str, mode = 'w'):
    with open(strRoot,mode) as file:
        file.write(json.dumps(content))


# In[4]:


def get_SystSampl( TotalCount, flRate = 0.45):
    if type(TotalCount) == int:
         return round(TotalCount*flRate)
    else:
        intVar = TotalCount.shape[0]
        return round(intVar*flRate)


# In[5]:


data = pd.read_csv('RTG_CSV.csv').drop(['Unnamed: 0', 'Unnamed: 0.1'],axis=1)


# In[6]:


data.loc[data.gender == 'М', "gender"] = 'M'
data.loc[data.gender == 'Ж', "gender"] = 'F'


# In[7]:


data


# Суммарный остаток на карте

# In[8]:


avrBalance = data
avrBalance = avrBalance.query("current_balance_avg_sum > 0")
avrBalance = avrBalance.current_balance_avg_sum
avrBalance = avrBalance.sample(n=get_SystSampl(avrBalance))


# In[9]:


avrBalance = avrBalance.median()
avrBalance = avrBalance.tolist()


# In[10]:


save_fileInJSON([{'avrBalance': avrBalance}], 'avrBalance.json')


# Мужчины / Женщины

# In[11]:


ManToWoman = data
ManToWoman = ManToWoman.drop_duplicates(subset=['client_id'])
ManToWoman = ManToWoman.sample(n=get_SystSampl(ManToWoman))
ManToWoman = ManToWoman['gender'].value_counts()


# In[12]:


listGender   = [(ManToWoman.index)[0],(ManToWoman.index)[1]]
listPercent  = [[ManToWoman.values][0][0].tolist(), [ManToWoman.values][0][1].tolist()]
listHead = ['Gender','Percent']
save_fileInJSON(  get_compressedData( listGender, listPercent, listHead), 'Gender.json')


# Количество приобретённых карт за год

# In[13]:


now = datetime.datetime.now()


# In[14]:


cardTypeDF = data.query(f"start_date >= {now.year}-1")
cardTypeDF = cardTypeDF.sample(n=get_SystSampl(cardTypeDF))


# In[15]:


listCardType = cardTypeDF['card_type_name'].unique()


# In[16]:


cardTypeDF = cardTypeDF['card_type_name'].value_counts()


# In[17]:


sum = cardTypeDF.values.sum()


# In[18]:


listCreditSys = ['МИР', 'MIR', 'Visa', 'MasterCard','Maestro','Other']
listCreditSysCount = [0]*len(listCreditSys)


# In[19]:


for i in range(len(cardTypeDF.index)):
    for j in range(len(listCreditSys)):
        if (listCreditSys[j] in cardTypeDF.index[i]) or (listCreditSys[j] in cardTypeDF.index[i].capitalize()) : listCreditSysCount[j] += cardTypeDF.values[i]


# In[20]:


var = 0
for i in range(len(listCreditSysCount)): var += listCreditSysCount[i]


# In[21]:


listCreditSysCount[len(listCreditSysCount[:-1])] = sum - var


# In[22]:


listCreditSys = listCreditSys[1:]
listCreditSysCount[1] = listCreditSysCount[0] + listCreditSysCount[1]
listCreditSysCount = listCreditSysCount[1:]


# In[23]:


for i in range(len(listCreditSysCount)): listCreditSysCount[i] = round(listCreditSysCount[i]*100/sum, 1)


# In[24]:


save_fileInJSON(get_compressedData(listCreditSys, listCreditSysCount,['SystemName','Percent']), 'NewBankCard.json')


# Кол-во действующих банковских карт у человека в среднем

# In[25]:


ValueCardData = data
ValueCardData = ValueCardData.query("start_date != -1 & fact_close_date == -1")
ValueCardData = ValueCardData.drop(['purchase_sum','create_date', "create_date",'purchase_count','current_balance_avg_sum','current_balance_sum','current_debit_turn_sum','current_credit_turn_sum','contract_sum','gender','birth_date'], axis=1)
ValueCardData = ValueCardData.drop(['card_type_name', 'start_date', 'fact_close_date', 'card_type', 'product_category_name', 'city', 'nonresident_flag'], axis=1)


# In[26]:


ValueCardData = ValueCardData.value_counts('client_id')


# In[27]:


ValueCardData = ValueCardData.drop_duplicates()
ValueCardData = ValueCardData.sample(n=get_SystSampl(ValueCardData))


# In[28]:


listCreditCard = [1,2,3,"4+"]
listCreditCardCount = [0]*len(listCreditCard)


# In[29]:


for i in range(len(ValueCardData.index)):
        if ValueCardData[i] == 1:
            listCreditCardCount[0] +=1
        elif ValueCardData[i] == 2:
            listCreditCardCount[1] +=1
        elif ValueCardData[i] == 3:
            listCreditCardCount[2] +=1
        else:
            listCreditCardCount[3] +=1


# In[30]:


intSum = 0
for i in range(len(listCreditCardCount)) : intSum += listCreditCardCount[i]


# In[31]:


for i in range(len(listCreditCardCount)):
    listCreditCardCount[i] = round(listCreditCardCount[i] * 100 / intSum,2)


# In[32]:


save_fileInJSON(get_compressedData(listCreditCard, listCreditCardCount,['CardType','CardCount']), 'CreditCardCount.json')


# Возраст пользователей 

# In[33]:


ValueAgeData = data.query("start_date != -1 & fact_close_date == -1")
ValueAgeData = ValueAgeData.drop(['purchase_sum','create_date', "create_date",'purchase_count','current_balance_avg_sum','current_balance_sum','current_debit_turn_sum','current_credit_turn_sum','contract_sum','gender'], axis=1)
ValueAgeData = ValueAgeData.drop(['card_type_name', 'start_date', 'fact_close_date', 'card_type', 'product_category_name', 'city', 'nonresident_flag','card_id'], axis=1)
ValueAgeData = ValueAgeData.sample(n=get_SystSampl(ValueAgeData))


# In[34]:


def getlistEqualPartsOfNumberParts(intNub, intParts):
  d, r = divmod(intNub, intParts)
  return [d + (1 if i < r else 0) for i in range(intParts)]


# In[35]:


intMaxAge = 66


# In[36]:


listAgeZone = getlistEqualPartsOfNumberParts(100,14)


# In[37]:


listCountAgeZone = [0] * len(listAgeZone)
listSrtAgeZone = []
if listAgeZone[0] < 14: intLeft = 14-listAgeZone[0]
intRigth = listAgeZone[0]
intSum = 0


# In[38]:


for i in range(len(listAgeZone)-1):
    intLeft += listAgeZone[i]
    intRigth += listAgeZone[i+1]
    listCountAgeZone[i] += ValueAgeData.query(f"{now.year-intLeft} >= birth_date > {now.year-intRigth}").shape[0]
    intSum += listCountAgeZone[i]
    listSrtAgeZone.append( str(str(intLeft) + '-' + str(intRigth)) )
    if i == 0 : intLeft -= 14-listAgeZone[0]


# In[39]:


for i in range(len(listCountAgeZone)): listCountAgeZone[i] = round(listCountAgeZone[i]   * 100 / intSum,2)


# In[40]:


save_fileInJSON(get_compressedData(listSrtAgeZone[:-1], listCountAgeZone, ['Age','Percent'] ), 'Age.json')


# Сколько средний остаток за месяц по кредитным картам

# In[41]:


turnBalanceData = data
turnBalanceData = turnBalanceData.drop([ 'gender', 'birth_date', 'create_date', 'nonresident_flag', 'city', 'contract_sum', 'card_type_name', 'start_date', 'fact_close_date'], axis=1)
balanceData = turnBalanceData.drop_duplicates(subset='card_id')
creditTurnBalanceData = turnBalanceData.query("current_credit_turn_sum > 0 & product_category_name == 'Договор на текущий счет для дебетовой карты'")
creditTurnBalanceData = creditTurnBalanceData.sample(n=get_SystSampl(creditTurnBalanceData))
debetTurnBalanceData  = turnBalanceData.query("current_debit_turn_sum > 0  & product_category_name == 'Кредитная карта'")
debetTurnBalanceData = debetTurnBalanceData.sample(n=get_SystSampl(debetTurnBalanceData))
#ValueAgeData = ValueAgeData.sample(n=get_SystSampl(ValueAgeData))


# In[42]:


[debetTurnBalanceData.shape[0], creditTurnBalanceData.shape[0]]


# In[43]:


medianDebetTurnBalanceData = debetTurnBalanceData['current_debit_turn_sum'].median()
medianCreditTurnBalanceData = creditTurnBalanceData['current_credit_turn_sum'].median()


# In[44]:


save_fileInJSON([ { 'MedianDebetTurnSum':int(medianDebetTurnBalanceData),'MedianCreditTurnSum':int(medianCreditTurnBalanceData) } ], 'MedianBalance.json')


# Среднее время пользование банком

# In[45]:


AvrTimeUse = data
AvrTimeUse = AvrTimeUse[ ['client_id', 'card_id','start_date', 'fact_close_date'] ]
AvrTimeUse = AvrTimeUse.query("start_date > 0").sample(n=get_SystSampl(AvrTimeUse))
AvrTimeUse['Sum'] = 0
AvrTimeUse.loc[((AvrTimeUse.fact_close_date == -1)  ), "fact_close_date"] = now.year
AvrTimeUse.Sum = AvrTimeUse.fact_close_date - AvrTimeUse.start_date


# In[46]:


medianAvrTimeUse = AvrTimeUse.Sum.median()


# In[47]:


medianAvrTimeUse


# In[48]:


save_fileInJSON([{"MidAvrBankUseTime":medianAvrTimeUse}],'MidAvrBankUseTime.json')

