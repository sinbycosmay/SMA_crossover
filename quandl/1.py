import quandl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

us = quandl.get("EIA/PET_RWTC_D",authtoken="GpyMDziakbz1uv-2SJAD",paginate=True)
short_window = 25
long_window=120
signals = pd.DataFrame(index=us.index)
signals['signal']=0.0
signals['sm']=us['Value'].rolling(window=short_window,min_periods=1,center=False).mean()
signals['lm']=us['Value'].rolling(window=long_window,min_periods=1,center=False).mean()
signals['signal'][short_window:]=np.where(signals['sm'][short_window:]>signals['lm'][short_window:],1.0,0.0)
signals['positions']=signals['signal'].diff()
fig=plt.figure(figsize=(20,10))
ax1=fig.add_subplot(111,ylabel="y axis")
us['Value'].plot(ax=ax1,lw=1.)
signals[['sm','lm']].plot(ax=ax1,linewidth=1.0)
ax1.plot(signals.loc[signals.positions==1.0].index,signals.sm[signals.positions==1.0],'^',markersize=10,color='g')
ax1.plot(signals.loc[signals.positions==-1.0].index,signals.sm[signals.positions==-1.0],'v',markersize=10,color='r')
plt.show()