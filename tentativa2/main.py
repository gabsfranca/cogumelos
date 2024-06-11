import pandas as pd
import sqlite3
import dash 
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output 

# Ensure the path is correct and accessible
arquivoCsv = r'tentativa2/csv_result-COGU (1).csv'
try:
    le = pd.read_csv(arquivoCsv)
except Exception as e:
    print(f"falha ao ler csv: {e}")
    exit(1)

print(le.head())

conn = sqlite3.connect('cogus.db')  
le.to_sql('tabelaDados', conn, if_exists='replace', index=False)

selectAll = pd.read_sql_query('SELECT * FROM tabelaDados', conn)
conn.close()

app = dash.Dash(__name__)

index_page = html.Div([
    html.H1("Escolha:"), 
    dcc.Link('venenenoso ou nao?', href = '/ven'), 
    html.Br(),
    dcc.Link('habitat', href='/hab'),
    html.Br(),
    dcc.Link('Classe X Habitat', href='/cxh'),  
    html.Br(),
    dcc.Link('Classe X Odor', href='/cxo'),
    html.Br(),
    dcc.Link('Classe X mancha', href='/cxa'),
    html.Br(),
    dcc.Link('Classe X Cor Esporos', href='/cxce'),
    html.Br(),
    dcc.Link('habitat x Raiz Estipe', href='/hxr'),
    html.Br(),
])

classe_counts = le['classe'].value_counts().reset_index()
classe_counts.columns = ['classe', 'count']

# Criando o gráfico de pizza
venenoso = html.Div([
    html.H1('Venenoso?'),
    dcc.Graph(
        id='ven',
        figure=px.pie(classe_counts, values='count', names='classe', title="Distribuição de Classes")
    )
])

habitat = html.Div([
    html.H1('Habitat'),
    dcc.Graph(
        id = 'hab',
        figure = px.bar(le, x='habitat', color='habitat', opacity=1)
    )
])

classexhabitat = html.Div([
    html.H1('Classe x Habitat'),
    dcc.Graph(
        id='cxh',  # Renamed ID for claristy
        figure=px.violin(le, x='classe', y='habitat').update_traces(box_visible=False)  # Moved plot creation inside callback
    )
])

classexodor = html.Div([
    html.H1('Classe X Odor'),
    dcc.Graph(
        id ='cxo',
        figure = px.violin(le, x= 'classe', y='odor').update_traces(box_visible=False)
    )
])

classexaneis = html.Div([
    html.H1('Classe X Mancha'),
    dcc.Graph(
        id='cxa',
        figure = px.violin(le, x='classe', y='MANCHA').update_traces(box_visible=False)                    
    )
])

classexesporos = html.Div([
    html.H1('Classe X Cor da Impressão dos Esporos'),
    dcc.Graph(
        id='cxce',
        figure = px.violin(le, x= 'classe', y='cor_impressao_esporos').update_traces(box_visible=False)
    )
])

habitatxraiz = html.Div([
    html.H1('Habitat x Raiz do Estipe'),
    dcc.Graph(
        id='hxr',
        figure = px.violin(le, x = 'habitat', y = 'raiz_estipe').update_traces(box_visible=False)
    )
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))  # Corrected parameter name to 'pathname'
def mostraPagina(pathname):  # Updated function parameter to match Input property
    if pathname == '/':
        return index_page
    elif pathname == '/cxh':
        return classexhabitat
    elif pathname == '/cxo':
        return classexodor
    elif pathname == '/cxa':
        return classexaneis
    elif pathname == '/cxce':
        return classexesporos
    elif pathname == '/hxr':
        return habitatxraiz
    elif pathname == '/ven':
        return venenoso
    elif pathname == '/hab':
        return habitat
    else:
        return "404 Page Not Found"


if __name__ == '__main__':
    app.run_server(debug=False)
