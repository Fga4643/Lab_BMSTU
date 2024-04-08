from sklearn.datasets import fetch_20newsgroups
# from sklearn.datasets import fetch_20newsgroups_vectorized
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
# %matplotlib inline
sns.set(style="ticks")

MOST_POPULAR_WORDS_NUM = 10

cats = ['alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space']
dataset_bunch = fetch_20newsgroups(data_home='./dataset', categories=cats, remove=('headers', 'footers', 'quotes'))
# target_names - названия 20 категорий
# 
# dataset_bunch = fetch_20newsgroups(data_home='./dataset', categories=cats)

for x in dataset_bunch:
  print(x)
# print(dataset_bunch.DESCR)
# print(dataset_bunch.target)
# print(dataset_bunch.filenames)
# pprint(list(dataset_bunch.target_names))
# print(type(dataset_bunch.data))
# print(dataset_bunch.data)

print('target', dataset_bunch.target)
# print('frame', dataset_bunch.frame)
print('target_names', dataset_bunch.target_names)
# pprint('feature_names', list(dataset_bunch.feature_names))
# pprint(list(dataset_bunch.feature_names))
print('SAMPLE\n', dataset_bunch.data[0][:50], ' ... END SAMPLE\n')
# print(dataset_bunch.DESCR)

def show_top10(classifier, vectorizer, categories):
  feature_names = vectorizer.get_feature_names_out()
  for i, category in enumerate(categories):
    top = np.argsort(classifier.coef_[i])[-MOST_POPULAR_WORDS_NUM:]

    print("%s: %s" % (category, " ".join(feature_names[top])))

# dataset = pd.DataFrame(data= np.c_[dataset_bunch['data'], dataset_bunch['target']], columns= dataset_bunch['feature_names'] + ['target'])
# temp_df = make_dataframe(dataset_bunch)
# temp_df.head()
# print(dataset)

# составляет разреженную матрицу
#        \   № слова 
# №статьи    частота, %       
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(dataset_bunch.data)
print(vectors.shape)
print(type(vectors))
print(vectors[0])

print('после преобразования:')

# sorted_matrix = vectors[np.argsort(result)]
# sorted_matrix = np.argsort(vectors.coef_)
# print(sorted_matrix.shape)
# print(type(sorted_matrix))
# print(sorted_matrix)


clf = MultinomialNB(alpha=0.01, class_prior=None, fit_prior=True)
clf.fit(vectors, dataset_bunch.target)
print(type(clf))


sorted_koefs = np.sort(clf.coef_)   # это значения (уловные) - чем больше - тем чаще
sorted_idxs = np.argsort(clf.coef_) # это слова
# sorted_koefs = np.sort(clf.coef_)[0][-MOST_POPULAR_WORDS_NUM:]   # это значения (уловные) - чем больше - тем чаще
# sorted_idxs = np.argsort(clf.coef_)[0][-MOST_POPULAR_WORDS_NUM:] # это слова


print(sorted_idxs)
print(sorted_koefs)

# print(clf.coef_[0][17380])
# data = {'word' : ???[sorted_idxs][-MOST_POPULAR_WORDS_NUM:],
#         'group' : ['ball', 'pen', 'pencil', 'paper', 'mug'],
#         'value' : sorted_koefs[-MOST_POPULAR_WORDS_NUM:]}
# df = pd.DataFrame()
# print(df)

# top = np.argsort(clf.coef_[0])[-MOST_POPULAR_WORDS_NUM:]
# print(type(top))
# print(top)

# show_top10(clf, vectorizer, dataset_bunch.target_names)

# df = pd.DataFrame(data= np.c_[ds['data'], ds['target']],
#                      columns= list(ds['feature_names']) + ['target'])


coo = clf.coef_.tocoo(copy=False)

print(coo.row)
print(coo.col)
print(coo.data)

# Access `row`, `col` and `data` properties of coo matrix.
# df = pd.DataFrame({'index': coo.row, 'col': coo.col, 'data': coo.data})[['index', 'col', 'data']]
# df.head()