import streamlit as st
import json
from prophet.serialize import model_from_json
import pandas as pd
from prophet.plot import plot_plotly

def load_model():
    with open('modelo_prophet.json', 'r') as file_in:
        modelo = model_from_json(json.load(file_in))
        return modelo
                
modelo = load_model()

# Adicionando textos ao layout do Streamlit
st.title('Previsão do Preço por barril do petróleo bruto Brent Utilizando a Biblioteca Prophet')

st.caption('''Projeto com a biblioteca Prophet para prever preços do petróleo Brent. 
Treinado até 18/11/2024, o modelo apresenta RMSE de 7.57. Insira o número de dias para previsão 
e visualize um gráfico interativo e uma tabela com os valores estimados.''')

st.subheader('Insira o número de dias para previsão:')

dias = st.number_input(' ', min_value=1, value=1, step=1)

if 'previsao_feita' not in st.session_state:
    st.session_state['previsao_feita'] = False
    st.session_state['dados_previsao'] = None

if st.button('Prever'):
    st.session_state.previsao_feita = True
    futuro = modelo.make_future_dataframe(periods=dias, freq='D')
    previsao = modelo.predict(futuro)
    st.session_state['dados_previsao'] = previsao

if st.session_state.previsao_feita:
    fig = plot_plotly(modelo, st.session_state['dados_previsao'])
    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 1)',  # Define o fundo da área do gráfico como branco
        'paper_bgcolor': 'rgba(255, 255, 255, 1)', # Define o fundo externo ao gráfico como branco
        'title': {'text': "Previsão do Preço por Barril do Petróleo", 'font': {'color': 'black'}},
        'xaxis': {'title': 'Data', 'title_font': {'color': 'black'}, 'tickfont': {'color': 'black'}},
        'yaxis': {'title': 'Preço por Barril (US$)', 'title_font': {'color': 'black'}, 'tickfont': {'color': 'black'}}
    })
    fig.update_layout(xaxis=dict(range=[st.session_state['dados_previsao']['ds'].tail(dias*2).min(), st.session_state['dados_previsao']['ds'].max()]))
    st.plotly_chart(fig)

    previsao = st.session_state['dados_previsao']
    tabela_previsao = previsao[['ds', 'yhat']].tail(dias)
    tabela_previsao.columns = ['Data (Dia/Mês/Ano)', 'Preço (US$)']
    tabela_previsao['Data (Dia/Mês/Ano)'] = tabela_previsao['Data (Dia/Mês/Ano)'].dt.strftime('%d-%m-%Y')
    tabela_previsao['Preço (US$)'] = tabela_previsao['Preço (US$)'].round(2)
    tabela_previsao.reset_index(drop=True, inplace=True)
    st.write('Tabela contendo as previsões do preço por barril do petróleo bruto tipo Brent para os próximos {} dias:'.format(dias))
    st.dataframe(tabela_previsao, height=300)

    csv = tabela_previsao.to_csv(index=False)
    st.download_button(label='Baixar tabela como csv', data=csv, file_name='previsao_preco_petroleo.csv', mime='text/csv')