import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Violência Política no Brasil", layout="wide"
)


st.title("📊 Dashboard de Análise sobre Violência Política no Brasil")
st.markdown("""
### Contexto e Objetivo do Projeto
A violência política e os conflitos armados no Brasil impactam diretamente a segurança pública, a democracia e a rotina da população. 

Este minidashboard foi desenvolvido para transformar dados brutos sobre episódios de violência política em informações visuais simples e compreensíveis. A proposta é responder a duas perguntas centrais:
1. **Quais estados brasileiros apresentam a maior concentração de ocorrências de violência política?**
2. **Qual é o perfil desses eventos e quais categorias provocam o maior número de fatalidades?**
""")

st.markdown("---")


st.subheader("📂 Carregamento dos Dados")
arquivo = st.file_uploader(
    "Selecione o arquivo de dados (`dadosagressaopoli.csv`)", type=["csv"]
)

if arquivo is not None:
  
  df = pd.read_csv(arquivo)

  
  if "population_exposure" in df.columns:
    df["population_exposure"] = (
        df["population_exposure"].astype(str).str.replace(",", "").astype(float)
    )

 
  with st.expander("Clique para ver uma amostra dos dados brutos"):
    st.dataframe(df.head(10))

  
  st.subheader("Panorama Geral dos Dados")
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Total de Registros na Base", f"{df.shape[0]:,}")
  col2.metric("Total de Eventos Mapeados", f"{df['events'].sum():,}")
  col3.metric("Total de Fatalidades Registradas", f"{int(df['fatalities'].sum()):,}")
  col4.metric("Estados Atingidos (UFs)", df["admin1"].nunique())

  st.markdown("---")
  st.subheader("📈 Análises Gráficas e Respostas às Perguntas")


  st.markdown("### Pergunta 1: Quais estados apresentam maior volume de ocorrências?")

  df_estados = df.groupby("admin1")["events"].sum().reset_index()
  df_estados = df_estados.sort_values(by="events", ascending=False).head(10)

  fig_estados = px.bar(
      df_estados,
      x="admin1",
      y="events",
      title="Top 10 Estados com Maior Quantidade de Eventos de Violência Política",
      labels={"admin1": "Estado (UF)", "events": "Total de Eventos"},
      color="events",
      color_continuous_scale="Reds",
      text="events",
  )
  fig_estados.update_traces(textposition="outside")
  st.plotly_chart(fig_estados, use_container_width=True)

  
  st.info("""
    **💡 O que os dados mostram:**
    * **Distribuição Geográfica:** O gráfico deixa claro que o estado do **Rio de Janeiro** lidera o número de ocorrências, seguido de perto por **Bahia** e **Pernambuco**.
    * **Análise Prática:** A alta concentração de eventos nestes estados aponta para cenários de forte tensão territorial, onde incidentes violentos ocorrem com maior frequência. Isso indica onde a atenção das políticas de segurança e monitoramento precisa ser priorizada.
    """)

  st.markdown("---")

 
  st.markdown("### Pergunta 2: Como as fatalidades se distribuem entre os tipos de eventos?")

  df_eventos = df.groupby("event_type")["fatalities"].sum().reset_index()

  fig_eventos = px.pie(
      df_eventos,
      names="event_type",
      values="fatalities",
      title="Distribuição de Fatalidades por Categoria de Evento de Violência Política",
      hole=0.4,
      color_discrete_sequence=px.colors.qualitative.Set2,
  )
  st.plotly_chart(fig_eventos, use_container_width=True)

 
  st.info("""
    **💡 O que os dados mostram:**
    * **Proporção de Impacto e Letalidade:** A imensa maioria das mortes registradas está concentrada em episódios de **Violência contra civis (*Violence against civilians*)** e **Confrontos armados (*Battles*)**.
    * **Análise Prática:** Enquanto outros tipos de eventos (como protestos e tumultos) acontecem, a perda de vidas humanas está fortemente associada a ataques diretos à população civil e confrontos armados entre grupos ou com forças de segurança, evidenciando o alto grau de risco desses conflitos.
    """)


  st.markdown("---")
  st.caption("""
    📌 **Fonte dos dados:** Base pública de monitoramento de episódios de violência política e conflitos no Brasil da ACLED.
    
    """)
else:
  st.info(
      "👆 Por favor, faça o upload do arquivo `dadosagressaopoli.csv` acima para visualizar as análises completas."
  )