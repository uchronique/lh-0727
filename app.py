
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import kagglehub # Add kagglehub for direct download

st.set_page_config(layout="wide", page_title="COVID-19 대시보드")

st.title("COVID-19 전 세계 및 국가별 트렌드")
st.write("이 대시보드는 COVID-19의 확진자, 사망자, 회복자, 활동 중인 사례의 시간 경과에 따른 변화를 시각화합니다.")

@st.cache_data
def load_data():
    # Download the dataset directly from Kaggle
    try:
        # Note: For Streamlit Cloud deployment, you might need to configure Kaggle API keys
        # as Streamlit secrets (KAGGLE_USERNAME, KAGGLE_KEY). Otherwise, this might fail.
        path = kagglehub.dataset_download("imdevskp/corona-virus-report")
    except Exception as e:
        st.error(f"Kaggle dataset 다운로드 중 오류 발생: {e}. Streamlit Cloud에 배포하는 경우 Kaggle API 키를 `st.secrets`에 설정했는지 확인하세요.")
        st.stop()

    file_name = 'full_grouped.csv' # Assuming this is the main data file in the dataset
    file_path = os.path.join(path, file_name)
    
    if not os.path.exists(file_path):
        st.error(f"다운로드된 Kaggle 데이터셋에서 파일을 찾을 수 없습니다: {file_path}. 데이터셋 구조를 확인하세요.")
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
st.info("데이터 출처: Kaggle 'corona-virus-report' (앱 실행 중 직접 다운로드)")
