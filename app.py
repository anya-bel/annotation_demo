import streamlit as st
import pandas as pd
import numpy as np
import math

pos_dict = {'V': 'Verbe', 'D': 'Déterminant', 'N': 'Nom', 'A':'Adjectif', 'P': 'Préposition', 'PRO': 'Pronom', 'C':'Conjonction', 'PONCT':'Ponctuation'}

text = [('Afin', 'P'), ('de', 'P'), ('raconter', 'V'), ("l'", 'D'), ('histoire', 'N'), ("qu'", 'PRO'), ('ils', 'CL'), ('ont', 'V'), ('découverte', 'V'), (',', 'PONCT'), ('les', 'D'), ('petits', 'A'), ('et', 'C'), ('moyens', 'A'), ('de', 'P'), ('la', 'D'), ('classe', 'N'), ('de', 'P'), ('Chantal', 'N'), ('Hetzel', 'N'), (',', 'PONCT'), ('directrice', 'N'), (',', 'PONCT'), ('ont', 'V'), ('rédigé', 'V'), ('ce', 'D'), ('texte', 'N'), ('eux-mêmes', 'PRO'), ('.', 'PONCT')]

st.title("Texte")
st.write(" ".join([x[0] for x in text]))

nb_forms = [x*6 for x in range(math.ceil(len(text)/6))]

choice = [0 for _ in text]


st.title("Forme pour l'annotation")
st.write("N'oubliez pas de soumettre votre annotation")
with st.form(key='columns_in_form'):
    cols = st.columns(6)
    for i, col in enumerate(cols):
        for idx in nb_forms:
            if i+idx > len(text)-1:
                continue
            choice[i+idx] = col.selectbox(text[i+idx][0], ['-']+list(set([pos_dict.get(t[1], t[1])  for t in text])), key=i+idx)


    submitted = st.form_submit_button('Soumettre')   

if submitted:
    with open('answers.csv', 'a') as ans_file:
        answers = ",".join(choice)+'\n'
        ans_file.write(answers)

#st.text(submitted)
#st.text(choice)

df = pd.read_csv('answers.csv', header=None).T

df2 = pd.DataFrame(columns=pos_dict.values()+['-'])
for n in range(df.shape[0]):
    df2.loc[n] = 0
#print('???')

for idx, row in df.iterrows():
    #print(row)
    for n, col in enumerate(row):
        #print(idx, col)
        df2.at[idx, col] = df2.loc[idx, col]+1

st.title('Résultats')
        
st.bar_chart(data=df2)
print('done')
