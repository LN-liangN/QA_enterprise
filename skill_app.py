import time
import streamlit as st
from skill.skill import ReactSkill

# 标题
st.title("企业智能问答助手")
st.divider()

if "skill" not in st.session_state:
    st.session_state["skill"] = ReactSkill()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能问答助手思考中..."):
        res_stream = st.session_state["skill"].execute_stream(prompt)

        def capture(generator, cache_list):     # 捕获

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()
