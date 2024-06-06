import streamlit as st
import openai

def request_chat_completion(
    prompt, 
    system_role="Your role is to be a competent interview assistant.", 
    model="gpt-4", 
    # gpt-3.5-turbo
    stream=False
):
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    stream=stream
    )
    return response

def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "✒️")
        else:
            break
    placeholder.markdown(message)
    return message

def print_streaming_response_console(response):
    message = ""
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            print(delta["content"], end="")
        else:
            break
    return message

st.set_page_config(
    page_title="특성화고 면접 도우미✍️",
    page_icon="✍️"
)

st.title("특성화고 면접 도우미🏫")
st.subheader("합격을 위해! 가현쌤이 응원합니다!👊")
auto_complete = st.toggle("👈누르면 예시가 나옵니다.")

example = {
    "school": "서서울생활과학고등학교",
    "department": "국제조리학과",
    "max_length": 700,
    "question": "지원한 동기가 무엇인지 말해보세요.",
    "answer": "어린 시절부터 요리 좋아했고 음식을 나누는 것에 기쁨을 느낌."
    # "answer": "저는 음식을 통해 사람들에게 기쁨과 만족을 주는 것에 열정을 느끼고 있습니다. 어린 시절부터 가정에서 요리를 통해 사람들을 행복하게 해본 경험이 있고, 음식을 창조하는 과정과 예술적 표현에 흥미를 느끼고 있습니다. 조리학 공부를 통해 음식을 예술로써 표현하고 사회적으로 소통과 이해를 촉진하는 방법을 배우고 싶습니다. 최종적으로, 레스토랑 쉐프로서 사람들에게 즐거움을 주는 직업을 향해 나아가고 싶습니다."
}

prompt_template="""
고등학교 면접 질문에 대한 답을 작성해야합니다.
답변해야하는 예상 질문과 이에 관련된 유저의 답안을 참고해서 예시 답변을 작성해주세요.
반드시 {max_length} 단어 이내로 작성해야 합니다.


---
지원 학교:{school}
지원 과:{department}
면접 문제: {question}
면접 답안:{answer}
---
""".strip()

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        school = st.text_input(
            "지원 학교",
            value=example["school"] if auto_complete else "",
            placeholder=example["school"])
    with col2:
        department = st.text_input(
            "지원 과",
            value=example["department"] if auto_complete else "",
            placeholder=example["department"])
    with col3:
        max_length= st.number_input(
            "최대 길이",
            min_value=100,
            max_value=2000,
            step=100,
            value=700
    )
    question = st.text_area(
        "면접 문제",
        value=example["question"] if auto_complete else "",
            placeholder=example["question"])
    answer = st.text_area(
        "면접 답안",
        value=example["answer"] if auto_complete else "",
            placeholder=example["answer"])
    submit = st.form_submit_button("제출하기")
if submit:
    if not school:
        st.error("지원하는 학교를 입력해주세요.")
    elif not department:
        st.error("지원하는 과를 입력해주세요")
    elif not question:
        st.error("예상 면접 문항을 입력해주세요.")
    elif not answer:
        st.error("면접 답안을 작성해주세요.")
    else:
        prompt = prompt_template.format(
            school = school,
            department = department,
            max_length = max_length // 6,
            question = question,
            answer = answer
        )
        system_role = "Your role is to be a competent interview assistant."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)
        st.markdown(f"**공백 포함 글자 수: {len(message)}**")
