import pandas as pd
import numpy as np
import json

with open('config.json') as config_file:
    config = json.load(config_file)

# Read in chart songs with SVR predictions and create time series measures for regression analyses 
df = pd.read_pickle(config['output'])
reg_data = pd.DataFrame(columns=['country','year'])
years = list(range(1973,2020))
for year in years:
    
    print(f'Year: {year}')
    year_df = df[df.year==year].sort_values('position').reset_index(drop=True)  
    
    scores = year_df.loc[:,['valence_th','arousal_th','valence_md','arousal_md']]
    
    if year_df.shape[0]:
    
        means = scores.mean()       
        means = means.rename({'valence_th':'valence_th_av',
                              'arousal_th':'arousal_th_av',
                              'valence_md':'valence_md_av',
                              'arousal_md':'arousal_md_av'})
        
        num1 = year_df.loc[year_df.position==1, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num1 = num1.rename({'valence_th':'valence_th_num1',
                              'arousal_th':'arousal_th_num1',
                              'valence_md':'valence_md_num1',
                              'arousal_md':'arousal_md_num1'})
        
        num2 = year_df.loc[year_df.position==2, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num2 = num2.rename({'valence_th':'valence_th_num2',
                              'arousal_th':'arousal_th_num2',
                              'valence_md':'valence_md_num2',
                              'arousal_md':'arousal_md_num2'})
        
        num3 = year_df.loc[year_df.position==3, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num3 = num3.rename({'valence_th':'valence_th_num3',
                              'arousal_th':'arousal_th_num3',
                              'valence_md':'valence_md_num3',
                              'arousal_md':'arousal_md_num3'})

        num4 = year_df.loc[year_df.position==4, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num4 = num4.rename({'valence_th':'valence_th_num4',
                              'arousal_th':'arousal_th_num4',
                              'valence_md':'valence_md_num4',
                              'arousal_md':'arousal_md_num4'})

        num5 = year_df.loc[year_df.position==5, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num5 = num5.rename({'valence_th':'valence_th_num5',
                              'arousal_th':'arousal_th_num5',
                              'valence_md':'valence_md_num5',
                              'arousal_md':'arousal_md_num5'})

        num6 = year_df.loc[year_df.position==6, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num6 = num6.rename({'valence_th':'valence_th_num6',
                              'arousal_th':'arousal_th_num6',
                              'valence_md':'valence_md_num6',
                              'arousal_md':'arousal_md_num6'})

        num7 = year_df.loc[year_df.position==7, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num7 = num7.rename({'valence_th':'valence_th_num7',
                              'arousal_th':'arousal_th_num7',
                              'valence_md':'valence_md_num7',
                              'arousal_md':'arousal_md_num7'})

        num8 = year_df.loc[year_df.position==8, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num8 = num8.rename({'valence_th':'valence_th_num8',
                              'arousal_th':'arousal_th_num8',
                              'valence_md':'valence_md_num8',
                              'arousal_md':'arousal_md_num8'})

        num9 = year_df.loc[year_df.position==9, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num9 = num9.rename({'valence_th':'valence_th_num9',
                              'arousal_th':'arousal_th_num9',
                              'valence_md':'valence_md_num9',
                              'arousal_md':'arousal_md_num9'})


        num10 = year_df.loc[year_df.position==10, ['valence_th','arousal_th','valence_md','arousal_md']].mean()
        num10 = num10.rename({'valence_th':'valence_th_num10',
                              'arousal_th':'arousal_th_num10',
                              'valence_md':'valence_md_num10',
                              'arousal_md':'arousal_md_num10'})     
    
        data = pd.concat([means,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10])
        
        data['country']='uk'      
        data['year']=year      
    
    reg_data = reg_data.append(data, ignore_index=True)


# Read in macro time series data from Hills et al. (2019) and merge with music time series measures
macro_df = pd.read_stata(config['happiness_data'])
macro_df = macro_df[(macro_df.isocntry=='GB-GBN') & (macro_df.year>=1973)]
macro_df.isocntry = macro_df.isocntry.replace('GB-GBN','uk')
macro_df = macro_df.rename(columns={'isocntry':'country'})
reg_data = pd.merge(reg_data,macro_df, on=['country','year'], how='outer')

# Create stata dta
obj_type_cols = list(reg_data.select_dtypes(include=['object']).columns)
reg_data[obj_type_cols] = reg_data[obj_type_cols].astype(str)
reg_data.to_stata(f'./data/model/reg_data.dta', write_index=False, version=117)