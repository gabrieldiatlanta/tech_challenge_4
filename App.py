import streamlit as st
import json
from prophet.serialize import model_from_json
import pandas as pd
from prophet.plot import plot_plotly
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    layout='wide'
)

# Adicionando textos ao layout do Streamlit
st.title('Análise de Tendências e Impactos do Preço do Petróleo Brent')
st.caption('Por GV Consultoria')
st.caption('Integrantes: Antônio Gabriel Di Atlanta Valente e Vanessa Larize Alves de Carvalho')

st.write('''
O petróleo Brent é um dos principais indicadores do mercado global de energia, desempenhando um papel crucial na determinação dos custos e margens de produtos refinados, como combustíveis e petroquímicos. 

Para a indústria petroquímica, que opera em mercados dinâmicos e enfrenta desafios como volatilidade de preços, mudanças regulatórias e transições para fontes de energia mais limpas, compreender as tendências do Brent é essencial para manter a competitividade.

Este dashboard foi projetado para fornecer insights profundos sobre o comportamento histórico e atual dos preços do petróleo Brent, além de permitir identificar padrões, correlacionar eventos geopolíticos e econômicos com as flutuações do mercado, fornecendo assim suporte na tomada de decisões estratégicas.
'''
)

st.write('''**Como usar este dashboard:**''')

st.write('''
- Explorar tendências históricas: Analise flutuações de preço ao longo de períodos específicos;

- Antecipar riscos e oportunidades: Identifique momentos críticos que podem impactar custos e margens operacionais;

- Guiar decisões estratégicas: Utilize insights para otimizar compras de petróleo, estratégias de refino e negociações no mercado;

- Prever valores futuros do petróleo Brent com machine learning: Com a aplicação de um modelo preditivo baseado em algoritmos de machine learning, oferecemos projeções dos preços futuros do barril de petróleo. Isso ajuda a tomar decisões proativas, reduzindo a exposição a riscos e maximizando as oportunidades em cenários de alta volatilidade. 

Prepare-se para descobrir como dados bem analisados podem transformar desafios em oportunidades e fortalecer a liderança no setor energético global.

''')

st.subheader("Análise das Flutuações dos Preços ao Longo do Tempo")

st.write(
    '''
Como mostrado no gráfico abaixo, é possível identificar alguns picos e vales no preço do barril que merecem destaque.

Vamos focar em quatro deles e, para tornar o dashboard mais interativo e direcionado à análise desejada, será possível aplicar filtros de datas e selecionar os eventos mais relevantes.
'''
)

dados = pd.read_csv('historico_preco_barril_petroleo.csv')
dados['data'] = pd.to_datetime(dados['data'])
dados = dados.set_index('data')

# Lista de opções para o combobox
opcoes = ["Selecione um evento relevante", "2008-2009: Crise Financeira Global", "2014-2016: Colapso do Petróleo", "2020: Pandemia de COVID-19", "2022: Conflito Rússia-Ucrânia"]

# Intervalos associados aos eventos
eventos = {
    "2008-2009: Crise Financeira Global": ("2008-06-01", "2009-01-31"),
    "2014-2016: Colapso do Petróleo": ("2014-06-01", "2016-02-28"),
    "2020: Pandemia de COVID-19": ("2020-02-01", "2020-08-31"),
    "2022: Conflito Rússia-Ucrânia": ("2022-02-01", "2022-06-30"),
}

# Criando o combobox
escolha = st.selectbox(
    " ",  # Texto de instrução
    opcoes,                  # Lista de opções
    index=0                  # Índice padrão (opcional, padrão é 0)
)

start_date, end_date = st.slider(
    "Selecione o intervalo de datas para análise:",
    min_value=dados.index.min().date(),
    max_value=dados.index.max().date(),
    value=(dados.index.min().date(), dados.index.max().date()),  # Valores padrão: intervalo completo
    format="YYYY-MM-DD"
)

# Filtrar dados com base no intervalo
filtered_data = dados.loc[start_date:end_date]

# Criar o gráfico com Plotly
fig = go.Figure()

# Adicionar a linha do preço
fig.add_trace(go.Scatter(
    x=filtered_data.index,
    y=filtered_data['preco'],
    mode='lines',
    name='Preço do barril'
))

# Verificar se um evento foi selecionado
if escolha != "Selecione um evento relevante":

    # Obter o intervalo de datas do evento selecionado
    highlight_start, highlight_end = eventos[escolha]

    # Adicionar área destacada
    fig.add_trace(go.Scatter(
        x=[datetime.strptime(highlight_start, '%Y-%m-%d'), datetime.strptime(highlight_start, '%Y-%m-%d'), 
        datetime.strptime(highlight_end, '%Y-%m-%d'), datetime.strptime(highlight_end, '%Y-%m-%d')],
        y=[dados['preco'].min(), dados['preco'].max(), dados['preco'].max(), dados['preco'].min()],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Período Selecionado'
    ))

# Configurações do layout
fig.update_layout(
    title=f"Análise de Preço do Petróleo Brent ({start_date} a {end_date})",
    xaxis_title="Data",
    yaxis_title="Preço (US$)",
    legend_title="Legenda",
    template="plotly_white"
)

# Exibir gráfico
st.plotly_chart(fig, use_container_width=True)

if escolha == "2008-2009: Crise Financeira Global":
    st.subheader('2008-2009: Crise Financeira Global')
    st.write('''
    A crise financeira global, desencadeada pela falência do Lehman Brothers em setembro de 2008, resultou em uma drástica desaceleração econômica global. 
    
    A menor atividade econômica gerada pela crise reduziu a demanda por petróleo em setores como transporte e manufatura, contribuindo para a forte desvalorização do preço do barril.

    O preço do petróleo Brent sofreu uma queda abrupta entre meados de 2008 e o início de 2009, saindo de cerca de US\$ 140 por barril em julho de 2008 para menos de US\$ 40 em janeiro de 2009.
    '''
    )

if escolha == "2014-2016: Colapso do Petróleo":
    st.subheader("2014-2016: Colapso do Petróleo")
    st.write('''
    No início de 2014, o preço de petróleo começou a cair drasticamente, impulsionado por uma combinação de fatores, destacando-se o aumento significativo da produção global. 
    
    Entre os principais elementos, está o boom do shale oil (petróleo de xisto) nos Estados Unidos, que transformou o país em um dos maiores produtores globais, reduzindo sua dependência de importações. 
    
    Paralelamente, a Organização dos Países Exportadores de Petróleo (OPEP) decidiu não cortar sua produção, optando por manter a oferta elevada como estratégia para proteger sua participação de mercado diante da concorrência crescente do petróleo não convencional.

    Esse excesso de oferta no mercado global foi agravado por uma desaceleração na demanda, especialmente em economias emergentes como a China, que enfrentou desafios econômicos e redução no ritmo de crescimento industrial. 
    
    Essa combinação de alta oferta e demanda enfraquecida resultou em um desequilíbrio significativo no mercado.

    Como consequência, o preço do petróleo Brent, despencou de aproximadamente US\$ 110 por barril em meados de 2014 para menos de US\$ 30 no início de 2016, marcando um dos períodos mais críticos para a indústria petrolífera nas últimas décadas. 
    O
    Essa crise impactou severamente as economias dependentes de exportação de petróleo, como Rússia e Venezuela, além de forçar grandes cortes de custos e reestruturações em empresas do setor.
    '''
    )

if escolha == "2020: Pandemia de COVID-19":
    st.subheader("2020: Pandemia de COVID-19")
    st.write('''
    A pandemia de COVID-19 trouxe impactos severos para o mercado de petróleo, desencadeando uma queda histórica na demanda global. 
    
    As medidas de bloqueio e as restrições de circulação implementadas em todo o mundo reduziram drasticamente a atividade econômica. 
    
    O setor de transporte foi especialmente afetado: as viagens aéreas praticamente cessaram, enquanto o transporte rodoviário sofreu uma queda acentuada, levando a um declínio sem precedentes no consumo de petróleo.
    
    Como resultado, o preço do petróleo Brent despencou rapidamente, caindo para menos de US\$ 10 por barril em abril de 2020. 
    
    Este foi um dos níveis mais baixos registrados na história recente, gerando uma crise profunda para a indústria petrolífera e impactando severamente países e empresas dependentes da produção de petróleo.
    '''
    )

if escolha == "2022: Conflito Rússia-Ucrânia":
    st.subheader("2022: Conflito Rússia-Ucrânia")
    st.write('''
    A invasão da Ucrânia pela Rússia em fevereiro de 2022 gerou grandes incertezas no mercado energético global, dado o papel crucial da Rússia como um dos maiores exportadores de petróleo e gás natural. 
    
    A crise escalou rapidamente com a imposição de sanções econômicas e embargos pelos países ocidentais, que limitaram significativamente a exportação de petróleo russo, reduzindo a oferta global em um momento de alta demanda.

    Além disso, a possibilidade de interrupções no fornecimento de gás natural da Rússia para a Europa, essencial para aquecimento e geração de energia, aumentou ainda mais a pressão nos mercados. 
    
    A dependência europeia dos recursos energéticos russos colocou governos e empresas em alerta, forçando a busca por alternativas de fornecimento.

    Como reflexo dessas tensões, o preço do petróleo Brent disparou, alcançando cerca de US\$ 130 por barril em meados do primeiro semestre de 2022, marcando uma das maiores altas em anos. 
    
    Este aumento significativo exerceu forte impacto sobre a inflação global e intensificou os debates sobre segurança energética e transição para fontes renováveis.
    '''
    )

st.subheader('Impacto dos eventos globais nos preços do Petróleo')

st.write('''
Após analisar cada um desses eventos separadamente, podemos destacar a importância de acompanhar atentamente os acontecimentos globais para identificar oportunidades e mitigar riscos que podem impactar diretamente os negócios e o planejamento estratégico.

A Crise Financeira Global (2008-2009) mostrou a importância de prever e responder à volatilidade do mercado, demonstrando como uma desaceleração econômica global pode desvalorizar abruptamente ativos. Empresas que anteciparam a crise ou ajustaram suas operações para lidar com a queda na demanda por petróleo foram mais capazes de sobreviver e até prosperar em um ambiente desfavorável.

Durante o Colapso do Petróleo (2014-2016), companhias que reconheceram a superprodução de petróleo e sua relação com a política da OPEP poderiam ter planejado melhor suas finanças e estoques, evitando prejuízos desnecessários.

A pandemia de COVID-19 (2020) mostrou que as empresas que souberam interpretar a queda acentuada dos preços e armazenar petróleo barato obtiveram vantagens econômicas significativas, aproveitando oportunidades em tempos de crise.

O conflito Rússia-Ucrânia (2022) evidenciou como fatores geopolíticos podem alterar drasticamente o mercado, provando que empresas que monitoram o contexto geopolítico e entendem os impactos de sanções, conseguem antecipar custos mais altos e reavaliar contratos e cadeias de fornecimento.

O monitoramento contínuo de eventos globais e a elaboração de cenários futuros são fundamentais para mitigar a exposição a riscos. Com esse objetivo, foi desenvolvido um modelo preditivo que utiliza o histórico completo de preços para identificar tendências e antecipar movimentos de mercado.
'''
)

# Previsão Prophet

st.subheader('Análise Preditiva')

st.write('''

Para fazer a análise preditiva foi utilizado o algoritmo de machine learning Prophet, com parâmetros cuidadosamente ajustados e testados. O modelo também incorporou os períodos de eventos relevantes mencionados anteriormente, garantindo maior precisão nas previsões.

Para avaliar a eficácia do modelo, foram aplicadas as métricas MSE (Erro Quadrático Médio) e RMSE (Raiz do Erro Quadrático Médio), que alcançaram valores excelentes de 23,73 e 4,87, respectivamente.

O modelo foi treinado com o histórico de preços até o dia 18 de novembro de 2024. Logo, a previsão será gerada a partir do dia 19 de novembro de 2024.

A previsão pode ser realizada selecionando, abaixo, a quantidade de dias desejados para projeção.

''')

def load_model():
    with open('modelo_prophet.json', 'r') as file_in:
        modelo = model_from_json(json.load(file_in))
        return modelo
                
modelo = load_model()

dias = st.number_input('Insira o número de dias para previsão:', min_value=1, value=1, step=1)

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
    fig.update_layout(xaxis=dict(range=[st.session_state['dados_previsao']['ds'].tail(dias*3).min(), st.session_state['dados_previsao']['ds'].max()]))
    st.plotly_chart(fig, use_container_width=True)

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