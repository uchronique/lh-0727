import streamlit as st

st.set_page_config(layout="wide")

st.title("두 숫자 더하기 앱")
st.write("두 개의 숫자를 입력하면 그 합을 계산해 드립니다.")

# 숫자 입력 받기
number1 = st.number_input("첫 번째 숫자를 입력하세요:", value=0)
number2 = st.number_input("두 번째 숫자를 입력하세요:", value=0)

# 합 계산
sum_numbers = number1 + number2

# 결과 출력
st.subheader("계산 결과")
st.success(f"두 숫자의 합은: {sum_numbers}")

st.write("--- ")
