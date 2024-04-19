import pandas as pd

list1 = pd.read_csv('fsclist.csv')

list2 = pd.read_csv('fsclist2.csv')

list3 = list1.append(list2, ignore_index=True)

list3.to_csv('fsclistmegred.csv', index=False)