#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import kaleido



class missing_metrics_calculator():
    def __init__(self,path):
        data=pd.read_excel(path, index_col=0)
        self.data=data.sort_values(by = ['Фамилия, Имя, Отчество', 'Дата обследования'], ascending = [True, True])
        
    def get_persons_list(self,data):
        persons=data["Фамилия, Имя, Отчество"].unique()
        return sorted(persons)
    
    def prepare_individual_data(data,persons_list):
        individual_data_list=[]
        for person in persons_list:       
            individual_data_list.append(data[data.values  == person])
        return individual_data_list
        
    def calc_tension_degree(self,HR,SI,pNN50,HF):
        tension_degree=-0.697+0.015*HR-0.001*SI-0.132*pNN50+0.043*HF
        return tension_degree

    def calc_functional_reserves(self,HR,SI,pNN50,HF):
        functional_reserves=4.087-0.012*HR-0.009*SI-0.005*pNN50-0.006*HF
        return functional_reserves

    def calc_functional_status(self,pNN50,LF,HF):
        functional_status=81.79175-0.03406*pNN50-0.00165*LF+0.00067*HF
        return functional_status

    def calc_adaptation_potential(self,HR,SD,DD,B,m,P):
        adaptation_potential=0.011*HR+0.014*SD+0.008*DD+0.014*B+0.009*m-0.009*P-0.27
        return adaptation_potential
        
    def make_data_list(self,data):
        return np.array(data.values)

    def calc_all_metrics_for_person(self):
        data=self.data[["Примечания","Фамилия, Имя, Отчество","Дата обследования","1. HR, уд./мин.","Систол. давление","Диастол. давление","Вес,кг","Рост,см","Возраст, лет","19. SI","8. pNN50 (Нормир.)","21. HF (Нормир.)","22. LF (Нормир.)"]]
        data_list=self.make_data_list(data)
        #result=[]
        #functional_reserves_data=[]
        #tension_degree_data=[]
        dataframe_list=[]
        observation_no=0
        for row in data_list:
            row={k:v for k,v in zip(list(data.columns),row)}
            tension_degree=self.calc_tension_degree(row["1. HR, уд./мин."],row["19. SI"],row["8. pNN50 (Нормир.)"],row["21. HF (Нормир.)"])  
            #tension_degree=calc_tension_degree(row[0],row[6],row[7],row[8])
            func_status=self.calc_functional_status(row["8. pNN50 (Нормир.)"],row["22. LF (Нормир.)"],row["21. HF (Нормир.)"])
            adaptation_potential=self.calc_adaptation_potential(row["1. HR, уд./мин."],row["Систол. давление"],row["Диастол. давление"],row["Возраст, лет"],row["Вес,кг"],row["Рост,см"])
            functional_reserves=self.calc_functional_reserves(row["1. HR, уд./мин."],row["19. SI"],row["8. pNN50 (Нормир.)"],row["21. HF (Нормир.)"])
            if len(dataframe_list)!=0:
                if row["Фамилия, Имя, Отчество"]==dataframe_list[-1][1]:
                    observation_no+=1
                else:
                    observation_no=0
            dataframe_list.append([observation_no,row["Фамилия, Имя, Отчество"],row["Дата обследования"],row["Примечания"],tension_degree,func_status,adaptation_potential,functional_reserves])
            #functional_reserves_data.append(functional_reserves)
            #tension_degree_data.append(tension_degree)
        df = pd.DataFrame(dataframe_list, 
        columns=['no','Фамилия, Имя, Отчество', 'Дата обследования',"Примечания","Cтепень напряжения","функциональное состояние","Aдаптационный потенциал","Функциональные резервы"])
        self.df=df
        return df
    def draw_and_save_plot(self,data):
        persons_list=self.get_persons_list(data)
        fig = px.line(data, x="Cтепень напряжения", y="Функциональные резервы", color="Фамилия, Имя, Отчество", text="no")
        layout = go.Layout(
        
        )
        #fig.layout.height =800
        fig.update_traces(textposition="bottom right")
        fig.update_traces(hoverinfo="all", hovertemplate="Степень напряжения: %{x}<br>Функциональные резервы:%{y}")
        fig.update_yaxes( zeroline=True, zerolinewidth=2, zerolinecolor='black',constraintoward="center")
        fig.update_xaxes( zeroline=True, zerolinewidth=2, zerolinecolor='black',constraintoward="center")
        fig.update_layout(legend_orientation="h",
                      autosize=False,
                      width=1000,
                      height=1000,
                      legend=dict(x=.5, xanchor="left"),
                      title="График",
                      xaxis_title="Степень напряжения",
                      yaxis_title="Функциональные резервы",
                      margin=dict(l=0, r=0, t=30, b=0))
        fig.show()
        fig.write_html("fig1.html")
    def main(self):
        new_data=self.calc_all_metrics_for_person()
        self.draw_and_save_plot(new_data)
        new_data.to_excel("result.xlsx")  
        





#calc=missing_metrics_calculator('turisty_dlya_Sevy.xlsx')
#calc.main()




#pd.read_excel("result.xlsx", index_col=0)





