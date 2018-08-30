from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import pandas as pd
# tsne=TSNE()
# tsne.fit_transform(data_zs)  #进行数据降维,降成两维
# #a=tsne.fit_transform(data_zs) #a是一个array,a相当于下面的tsne_embedding
#
# tsne=pd.DataFrame(tsne.embedding_,index=data_zs.index) #转换数据格式
#
#
# d=tsne[r[u'聚类类别']==0]
# plt.plot(d[0],d[1],'r.')
#
# d=tsne[r[u'聚类类别']==1]
# plt.plot(d[0],d[1],'go')
#
# d=tsne[r[u'聚类类别']==2]
# plt.plot(d[0],d[1],'b*')
#
# plt.show()