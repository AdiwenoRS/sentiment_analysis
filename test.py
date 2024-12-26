import pandas as pd

datas = pd.read_csv('datasets/training.1600000.processed.noemoticon.csv')
sentiments = datas.iloc[:, 5].to_numpy()
subset = sentiments[:10]

print(subset)
# sentences = []
# for sentence in sentiments:
#     sentences.append(sentence)
# print(sentences)
