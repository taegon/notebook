#%%
import urllib.request
import json
import pandas as pd
import bs4

#%%
response = urllib.request.urlopen('http://www.burgerking.co.kr/api/store/searchmap/empty/?areacd=')
bgk_data = json.loads(response.read().decode('utf-8'))
bgk_tbl_web = pd.DataFrame(bgk_data)
bgk_tbl_web.head()
bgk_tbl_web.to_csv("input/bgk.csv")

#%%
bgk_tbl = pd.read_csv("input/bgk.csv", index_col=0)
bgk_tbl.head()

bgk_locs = pd.DataFrame(bgk_tbl['NewAddr'].apply(lambda v: v.split()[:2]).tolist(),
                        columns=('d1', 'd2'))
bgk_locs.head()

#%%
bgk_locs['d1'].unique()

#%%
d1_aliases = """서울시:서울특별시 충남:충청남도 강원:강원도 경기:경기도 충북:충청북도 경남:경상남도 경북:경상북도
전남:전라남도 전북:전라북도 제주도:제주특별자치도 제주:제주특별자치도 대전시:대전광역시 대구시:대구광역시 인천시:인천광역시
광주시:광주광역시 울산시:울산광역시"""
d1_aliases = dict(aliasset.split(':') for aliasset in d1_aliases.split())
bgk_locs['d1'] = bgk_locs['d1'].apply(lambda v: d1_aliases.get(v, v))

#%%
bgk_locs['d1'].unique()

#%%
#bgk_locs[bgk_locs['d1'] == '수원시']

#%%
#bgk_locs.iloc[101] = ['경기도', '수원시']

#%%
bgk_locs['d2'].unique()
#%%
bgk_locs['d2'] = bgk_locs['d2'].apply(lambda v: "" if v is None else v)

#%%
B = bgk_locs.apply(lambda r: r['d1'] + ' ' + r['d2'], axis=1).value_counts()
B.head()

