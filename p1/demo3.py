import pandas as pdimport numpy as npimport cufflinks as cfdf=pd.DataFrame
(np.random.rand(12, 4), 
columns=['a', 'b', 'c', 'd'])
df.iplot(kind ='bar',title='示例', xTitle = 'X轴', yTitle ='Y轴')