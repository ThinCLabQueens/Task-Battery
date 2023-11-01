import pandas as pd
import numpy as np

maindf = pd.read_csv('output.csv')
demodf = pd.read_csv('demo.csv')
maindf['Id_number'] = pd.Series([x.split('_')[0] + x.split('_')[1].zfill(3) for x in maindf['Id_number'].values])
outdf = pd.merge(maindf,demodf,on="Id_number")
outdf.to_csv('mergedfs.csv',index=False)