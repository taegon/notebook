#%%
# 위처럼 쓰면, VS Code + ipython 환경에서 셀로 지정됨.
# 현재 코드는 2개 셀로 구성하였는데, 파일을 읽는 부분과 지도 그리는 부분으로 나눔.
# 지도 그리는 코드를 수정해서 다시 돌릴 때, nc 파일을 다시 읽지 않아도 되도록 하기 위함.

#%matplotlib

import matplotlib.pyplot as plt
from scipy.io import netcdf
from mpl_toolkits.basemap import Basemap
import numpy as np

# 파일 읽기. 파일은 용량 관계로 업로드 하지 않았음. 경로를 맞춰서 수정하길 바람.
fh =  netcdf.netcdf_file('data/SPEI24.rcp85.nc', mode='r')

# t = 1900 부터 24 (2년) 간격으로 2000까지 뽑기. 1860년 1월이 0
grids = fh.variables["SPEI24"][1900:2000:24, :, :].copy()

# null 값은 지도에 표시되지 않도록 지우기
grids = np.ma.masked_array(grids, grids == -999)

# 지도에서 cell 위치를 맞추기 위해서 조정. 0.5도 간격이므로 반칸 이동.
lat = fh.variables['lat'][:].copy() - .25
lon = fh.variables['lon'][:].copy() - .25
lon, lat = np.meshgrid(lon, lat)

fh.close()

#%%
i = 1
for grid in grids:
    fig = plt.figure(figsize=(5, 7))
    # 지도의 영역을 지정함. 여기서는 한반도가 중심에 잡히는 위치로 임의설정함.
    m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=30, urcrnrlat=45,
            llcrnrlon=123, urcrnrlon=132, )
    # 맵에 색칠되는 셀의 색 팔레트.
    m.pcolormesh(lon, lat, grid,
                latlon=True, cmap='RdBu')
    plt.clim(-5, 5)
    m.drawcoastlines(color='gray')
    m.drawcountries(linewidth=1, color='gray')

    plt.title('SPEI24')
    plt.colorbar(label='spei 24')

    fig.savefig('output/test{:03d}.png'.format(i))
    i += 1
