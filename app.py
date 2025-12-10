import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="나만의 AI 비서", page_icon="🤖")
st.title("🤖 Gemini 2.5 챗봇")
st.caption("Streamlit으로 만든 빠르고 똑똑한 AI")

# 2. API 키 설정 (Secrets에서 가져옴)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("API 키가 없습니다. Streamlit 설정에서 Secrets를 추가해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 3. 모델 설정 (최신 gemini-2.5-flash 사용)
model = genai.GenerativeModel("gemini-2.5-flash")

# 4. 세션 상태 초기화 (대화 기록 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. 이전 대화 내용 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 처리
if prompt := st.chat_input("궁금한 것을 물어보세요..."):
    # 사용자 메시지 표시
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Gemini에게 메시지 전송
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")