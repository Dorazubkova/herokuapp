#!/usr/bin/env python
# coding: utf-8

# In[96]:


from bokeh.io import show, output_notebook
from bokeh.plotting import figure, show, output_notebook
from bokeh.tile_providers import CARTODBPOSITRON
import bokeh
import pandas as pd
import os
import sys
from bokeh.models import ColumnDataSource, HoverTool, LassoSelectTool, Label, Title
from bokeh.layouts import gridplot
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import PreText, Paragraph, Select, Dropdown
import bokeh.layouts as layout


# In[97]:


onoffmatrix = pd.read_csv('myapp/onoffmatrix_avg.csv', sep = ';', encoding='cp1251')
onoffmatrix = onoffmatrix[['stop_id_from','stop_id_to','movements_norm', 'hour_on']]

#остановки-суперсайты
stops_supers = pd.read_csv('myapp/stops_supers.csv', sep = ';', encoding='cp1251')

onoffmatrix = pd.merge(onoffmatrix, stops_supers, how='inner', left_on = ['stop_id_from'], right_on = ['stop_id'])
onoffmatrix = pd.merge(onoffmatrix, stops_supers, how='inner', left_on = ['stop_id_to'], right_on = ['stop_id'])
onoffmatrix = onoffmatrix[['super_site_x','super_site_y','movements_norm','hour_on']].rename(columns = {'super_site_x':'super_site_from',
                                                                                   'super_site_y':'super_site_to'})
onoffmatrix = onoffmatrix.groupby(['super_site_from','super_site_to','hour_on']).sum().reset_index()

supers_Moscow = pd.read_csv('myapp/supers_Mercator.csv', sep = ';')
supers_Moscow = supers_Moscow.drop_duplicates()

onoffmatrix = pd.merge(onoffmatrix, supers_Moscow, how = 'inner', 
              left_on = ['super_site_from'], right_on=['super_site']).rename(columns={'X':'X_from','Y':'Y_from'})
onoffmatrix = pd.merge(onoffmatrix,  supers_Moscow, how = 'inner', 
           left_on = ['super_site_to'], right_on=['super_site']).rename(columns={'X':'X_to','Y':'Y_to'})
onoffmatrix = onoffmatrix[['super_site_from','super_site_to','movements_norm','X_from','Y_from','X_to','Y_to','hour_on']]
onoffmatrix['movements_norm'] = round(onoffmatrix['movements_norm'],0)

#сайты Тушино из
supers_T = pd.read_csv('myapp/supersites_Tushino.csv', sep = ';')

onoffmatrix = pd.merge(onoffmatrix, supers_T, how='inner',left_on=['super_site_from'], right_on=['super_site'])
onoffmatrix = onoffmatrix[onoffmatrix['movements_norm']>10]


# In[ ]:


onoffmatrix_7 = onoffmatrix[onoffmatrix['hour_on'] == 7]
onoffmatrix_8 = onoffmatrix[onoffmatrix['hour_on'] == 8]


# In[ ]:


odmatrix = pd.read_csv('odmatrix_avg.csv', sep = ';', encoding='cp1251')
odmatrix = odmatrix[['site_id_from','site_id_to','movements_norm', 'hour_start']]

#сайты-суперсайты
sited_supers = pd.read_csv('sites_supers.csv', sep = ';', encoding='cp1251')

odmatrix = pd.merge(odmatrix, sited_supers, how='inner', left_on = ['site_id_from'], right_on = ['site_id'])
odmatrix = pd.merge(odmatrix, sited_supers, how='inner', left_on = ['site_id_to'], right_on = ['site_id'])
odmatrix = odmatrix[['super_site_x','super_site_y','movements_norm','hour_start']].rename(columns = {'super_site_x':'super_site_from',
                                                                              'super_site_y':'super_site_to', 'hour_start':'hour_on'})
odmatrix = odmatrix.groupby(['super_site_from','super_site_to','hour_on']).sum().reset_index()


odmatrix = pd.merge(odmatrix, supers_Moscow, how = 'inner', 
              left_on = ['super_site_from'], right_on=['super_site']).rename(columns={'X':'X_from','Y':'Y_from'})
odmatrix = pd.merge(odmatrix,  supers_Moscow, how = 'inner', 
           left_on = ['super_site_to'], right_on=['super_site']).rename(columns={'X':'X_to','Y':'Y_to'})
odmatrix = odmatrix[['super_site_from','super_site_to','movements_norm','X_from','Y_from','X_to','Y_to','hour_on']]
odmatrix['movements_norm'] = round(odmatrix['movements_norm'],0)

odmatrix = pd.merge(odmatrix, supers_T, how='inner',left_on=['super_site_from'], right_on=['super_site'])
odmatrix = odmatrix[odmatrix['movements_norm']>30]


# In[ ]:


odmatrix_7 = odmatrix[odmatrix['hour_on'] == 7]
odmatrix_8 = odmatrix[odmatrix['hour_on'] == 8]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


source_from = ColumnDataSource(data = dict(
                        X_from=[], 
                        Y_from=[],
                        size=[],
                        X_to=[], 
                        Y_to=[],
                        sitesfrom=[],
                        sitesto=[],
))


source_to = ColumnDataSource(data = dict(
                        X_from=[], 
                        Y_from=[],
                        size=[],
                        X_to=[], 
                        Y_to=[],
                        sitesfrom=[],
                        sitesto=[],
))


# source_from2 = ColumnDataSource(data = dict(
#                         X_from=list(links['X_from'].values), 
#                         Y_from=list(links['Y_from'].values),
#                         size=list(links['movements_norm'].values),
#                         X_to=list(links['X_to'].values), 
#                         Y_to=list(links['Y_to'].values)
# ))


# source_to2 = ColumnDataSource(data = dict(
#                         X_from=list(links['X_from'].values), 
#                         Y_from=list(links['Y_from'].values),
#                         size=list(links['movements_norm'].values),
#                         X_to=list(links['X_to'].values), 
#                         Y_to=list(links['Y_to'].values)
# ))


# source_from_labels = ColumnDataSource(data = dict(
#                         X_from=list(links[['X_from', 'Y_from','super_site_from']].drop_duplicates()['X_from'].values), 
#                         Y_from=list(links[['X_from', 'Y_from','super_site_from']].drop_duplicates()['Y_from'].values),
#                         label=list(links[['X_from', 'Y_from','super_site_from']].drop_duplicates()['super_site_from'].values)
# ))


# In[ ]:





# In[ ]:


lasso_from = LassoSelectTool(select_every_mousemove=True)
lasso_to = LassoSelectTool(select_every_mousemove=False)


toolList_from = [lasso_from, 'tap', 'reset', 'save', 'pan','wheel_zoom']
toolList_to = [lasso_to, 'tap', 'reset', 'save', 'pan','wheel_zoom']


p = figure(x_range=(4157975.01546188769862056 , 4173827.06850233720615506), y_range=(7521739.63348639197647572,  7533621.55124872922897339),
          x_axis_type="mercator", y_axis_type="mercator", tools=toolList_from)
p.add_tile(CARTODBPOSITRON)

p.add_layout(Title(text='Фильтр корреспонденций "ИЗ"', text_font_size='10pt', text_color = 'blue'), 'above')

# p.circle(x = 'X_from',
#          y = 'Y_from',
#          source=source_from_labels,
#         fill_color='black',
#         size=5)

r = p.circle(x = 'X_from',
         y = 'Y_from',
         source=source_from,
        fill_color='navy',
        size=10,
        fill_alpha = 1,
        nonselection_fill_alpha=0.4)



p_to = figure(x_range=(4157975.01546188769862056 , 4173827.06850233720615506), y_range=(7521739.63348639197647572,  7533621.55124872922897339),
          x_axis_type="mercator", y_axis_type="mercator", tools=toolList_to)
p_to.add_tile(CARTODBPOSITRON)


Time_Title = Title(text='Матрица: ', text_font_size='8pt', text_color = 'grey')
p.add_layout(Time_Title, 'above')

t = p_to.circle(x = 'X_to', y = 'Y_to', fill_color='red', fill_alpha = 0.6, 
                            line_color='red', line_alpha = 0.8, size=6 , source = source_to)



ds = r.data_source
tds = t.data_source


# In[ ]:


#widgets
stats = Paragraph(text='', width=500)
menu = [('onoffmatrix_7', 'onoffmatrix_7'), ('onoffmatrix_8', 'onoffmatrix_8'), ('odmatrix_7', 'odmatrix_7'),
       ('odmatrix_8', 'odmatrix_8')]
select = Dropdown(label="Выберите матрицу: ", menu = menu)


# In[ ]:





# In[ ]:


def update(attrname, old, new):
    sl = select.value
    print(sl)
    df = pd.DataFrame(data = eval(sl))
    print(df.columns.values)
    source_from_sl = ColumnDataSource(data = dict(
                        X_from=list(df['X_from'].values), 
                        Y_from=list(df['Y_from'].values),
                        size=list(df['movements_norm'].values),
                        X_to=list(df['X_to'].values), 
                        Y_to=list(df['Y_to'].values),
                        sitesfrom=list(df['super_site_from'].values),
                        sitesto=list(df['super_site_to'].values),
))
    source_from.data = source_from_sl.data
    
    
    source_to_sl = ColumnDataSource(data = dict(
                        X_from=list(df['X_from'].values), 
                        Y_from=list(df['Y_from'].values),
                        size=list(df['movements_norm'].values),
                        X_to=list(df['X_to'].values), 
                        Y_to=list(df['Y_to'].values),
                        sitesfrom=list(df['super_site_from'].values),
                        sitesto=list(df['super_site_to'].values),
))
    source_to.data = source_to_sl.data
    
    
    Time_Title.text = "Матрица: " + sl
    
    
select.on_change('value', update)


# In[ ]:





# In[ ]:





# In[ ]:


def callback(attrname, old, new):

    idx = source_from.selected.indices

    print("Indices of selected circles from: ", idx)
    print("Lenght of selected circles from: ", len(idx))

    #таблица с выбранными индексами 
    df = pd.DataFrame(data=ds.data).iloc[idx]
    #сумма movements по выделенным индексам
    aa = df.groupby(['X_to','Y_to'])['size'].transform(sum)


    p_to = figure(x_range=(4157975.01546188769862056 , 4173827.06850233720615506), 
                  y_range=(7521739.63348639197647572,  7533621.55124872922897339),
                  x_axis_type="mercator", y_axis_type="mercator", tools=toolList_to)
    p_to.add_tile(CARTODBPOSITRON)
    t = p_to.circle(x = 'X_to', y = 'Y_to', fill_color='red', fill_alpha = 0.6, 
                            line_color='red', line_alpha = 0.8, size=6 , source = source_to)


    if not idx: #если пустое выделение

        layout1.children[1] = p_to #обновить график справа

    else: #если не пустое выделение

        for x in idx: #для каждого выделенного индекса рисуем site_to и его параметры

            new_data = dict()
            new_data['x'] = [ds.data['X_to'][x]]
            new_data['y'] = [ds.data['Y_to'][x]]
            new_data['size'] = [aa[x]]
            new_data['index'] = [x]


            t_to = p_to.circle(x = [], y = [], fill_color='orange', fill_alpha = 0.6, 
                            line_color='red', line_alpha = 0.8, size=[] )
            tds_to=t_to.data_source
            tds_to.data = new_data

            #текст

            new_data_text = dict()
            new_data_text['x'] = [ds.data['X_to'][x]]
            new_data_text['y'] = [ds.data['Y_to'][x]]
            new_data_text['text'] = [aa[x]]


            l = p_to.text(x = [], y = [], text_color='black', text =[], text_font_size='8pt',
                         text_font_style = 'bold')
            lds=l.data_source
            lds.data = new_data_text


            layout1.children[1] = p_to #обновить график справа
            
source_from.selected.on_change('indices', callback)
    
            
def callback_to(attrname, old, new):

    idx2 = source_from.selected.indices
    idx_to = source_to.selected.indices

    inters_idx = list(set(idx2) & set(idx_to))
    
    print("Length of selected circles to: ", idx2)
    print("Length of selected circles to: ", inters_idx)


    #таблица с выбранными индексами 
    dff = pd.DataFrame(data=tds.data).loc[inters_idx]
    print("Length of selected circles to: ", dff)

    #сумма movements по выделенным индексам
    aaa = dff['size'].sum()
    print("size to: ", aaa)
    
    #сайты из
    sitesfrom = dff['sitesfrom'].drop_duplicates()
    sitesto = dff['sitesto'].drop_duplicates()

    stats.text = "Из сайтов " + str(list(sitesfrom)) + " в сайты " + str(list(sitesto)) + " едет " + str(aaa) + " человек(а) в час"

    
source_to.selected.on_change('indices', callback_to)




layout1 = layout.row(p,p_to)
layout2 = layout.column(select, stats)

# Create Tabs
box = layout.row(layout1, layout2)


curdoc().add_root(box)


# In[ ]:





# In[ ]:




