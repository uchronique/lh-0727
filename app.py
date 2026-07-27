
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="COVID-19 대시보드")

st.title("COVID-19 전 세계 및 국가별 트렌드")
st.write("이 대시보드는 COVID-19의 확진자, 사망자, 회복자, 활동 중인 사례의 시간 경과에 따른 변화를 시각화합니다.")

@st.cache_data
def load_data():
    # KaggleHub 경로 사용 (이전에 다운로드된 데이터셋 경로)
    data_path = "/kaggle/input/corona-virus-report"
    file_name = 'full_grouped.csv'
    file_path = os.path.join(data_path, file_name)
    
    if not os.path.exists(file_path):
        st.error(f"데이터 파일을 찾을 수 없습니다: {file_path}")
        st.stop()

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_covid = load_data()

# 국가 선택 위젯
country_list = ['전 세계'] + sorted(df_covid['Country/Region'].unique().tolist())
selected_country = st.selectbox("국가를 선택하세요:", country_list)

if selected_country == '전 세계':
    # 전 세계 데이터 집계
    df_plot = df_covid.groupby('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
    title_text = '전 세계 COVID-19 트렌드'
else:
    # 선택된 국가 데이터 필터링
    df_plot = df_covid[df_covid['Country/Region'] == selected_country]
    title_text = f'{selected_country} COVID-19 트렌드'

# 시계열 그래프 생성
fig = px.line(df_plot, x='Date', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
              title=title_text,
              labels={'value': '확진자/사망자/회복자/활동 중인 사례 수', 'variable': '지표'},
              hover_data={'Date': '|%Y-%m-%d'})

fig.update_layout(hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

st.markdown("--- ")
st.info("데이터 출처: Kaggle 'corona-virus-report'")
