import streamlit as st
import os, json
import requests
from PIL import Image


from streamlit_agent.clear_results import with_clear_container
import libs as libs


# App title
st.set_page_config(page_title="KT AI Agent PoC", layout="wide")

first_message = """
:두_손을_들고_있는_사람: 안녕하세요! 장사의 고수, 여러분의 AI 파트너! 저는 K intelligence AI Agent입니다.
창업 준비 중이신가요? 가게 운영이 막막하신가요? 걱정은 이제 그만! 당신의 아이디어에 장사의 날개를 달아드릴게요.
메뉴 선정부터, 손님 응대, 매출 관리, 홍보 전략까지! 실패는 줄이고, 성공 확률은 확 끌어올리는 진짜 장사 노하우를 전수해드립니다.
:말풍선: 예를 들어, 이런 질문도 할 수 있어요:
·      커피집 어떻게 매출을 올리나요?
·      요식업 주방 설계는 어떻게 해야 해요?
·      유튜브 광고는 어떻게 해야 효과가 좋을까요?
지금 바로 질문해보세요! K intelligence AI Agent는 항상 여러분의 옆에 있습니다. 당신의 성공, 제가 함께 만들어 드릴게요! :로켓:
K intelligence AI Agent
"""

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": first_message}]

# Replicate Credentials
with st.sidebar:
    st.title('소상공인 지원 Agent')

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요. KT AI Agent입니다. 무엇을 도와드릴까요?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

submit_clicked = False
user_input = ""

# message send form
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        user_input = prompt
        submit_clicked = True


if st.session_state.messages[-1]["role"] != "assistant":
    user_input = st.session_state.messages[-1]["content"]
    output_container = st.empty()
    if with_clear_container(submit_clicked):
        status_message = st.empty()
        status_message.info("에이전트에게 요청 중...")

        output_container = output_container.container()
        # answer_container = output_container.chat_message("assistant", avatar=Image.open('./ktlogo.png'))

        placeholder = st.empty()

        # curl -i \
        # -H 'Content-Type: application/json' \
        # -d '{"question": "오늘 서울 날씨는?", "chatHistory": [], "agentVer": "0.1", "curDate": "20250204 09:30", "userId": "user-id-20250204", "sessionId": "sessionid-20250204-0930"}' \
        # -X POST https://aca-poc-smeagent.greenmoss-898b3e43.koreacentral.azurecontainerapps.io/chat/stream

        response = requests.post(
            "https://aca-poc-smeagent.greenmoss-898b3e43.koreacentral.azurecontainerapps.io/chat/stream",
            json={"question": user_input, "chatHistory": [], "agentVer": "0.1", "curDate": "20250204 09:30", "userId": "user-id-20250204", "sessionId": "sessionid-20250204-0930"},
            stream=True
        )

        response_text = ""

        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                data_str = line[len("data: "):]  # 'data: ' 제거

                try:
                    data = json.loads(data_str)

                    if data.get("type") == "token":
                        content = data.get("content", "")
                        response_text += content
                        response_text = response_text.replace("\\n", "\n")
                        placeholder.markdown(f"{response_text}")
                
                except json.JSONDecodeError as e:
                    st.warning(f"JSON 파싱 에러: {e}")
                    continue
        
        message = {"role": "assistant", "content": response_text}
        st.session_state.messages.append(message)
        status_message.empty()

        submit_clicked = False
