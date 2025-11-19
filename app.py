import streamlit as st
from openai import OpenAI

# --- API KEY ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit 앱 제목
st.title("회사 이름 생성기")

# 사용자 입력 받기
what = st.text_input("무엇을 하는 회사인가요?(빈칸일시 친환경사업을 주업으로 하는 회사이름을 추천해드려요)", "")
want = st.text_input("회사 이름에 반드시 들어가야 하는 단어가 있나요?", "")
wordnumber = st.number_input("몇 글자로 제한할까요?", min_value=1, step=1)
many = st.number_input("몇 개의 후보 생성을 원하시나요?", min_value=1, step=1)

# 버튼 클릭 시 이름 생성 로직 실행
if st.button("회사 이름 생성"):
    # want가 빈 문자열이면 조건 문장에서 제외
    if want:
        want_phrase = f"{want}를 포함하여"
    else:
        want_phrase = ""

    # what이 빈 문자열이면 조건 문장 변경
    if what:
        what_phrase = f"{what}관련 일을 주업으로 하는"
    else:
        what_phrase = "친환경사업을 주업으로 하는"

    # 프롬프트 만들기
    prompt = f"""{what_phrase} 회사의 이름을 {want_phrase} 반드시 {wordnumber}+1글자로 출력.
이름은 독창적이며 한눈에 봤을때 무슨 회사인지 알기 쉽고 기억하기 쉬워야 함.
{many}개의 후보를 번호를 붙여서 리스트 형태로 출력."""

    # OpenAI GPT-4 응답 받기
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "번호를 붙여 목록 형태로만 답변, 다른 설명 금지."},
            {"role": "user", "content": prompt}
        ]
    )

    # 응답에서 회사 이름 후보 리스트 출력
    company_names = response.choices[0].message.content
    
    st.write("생성된 회사 이름 후보 목록:")
    st.text_area("회사 이름 후보", company_names, height=300)
