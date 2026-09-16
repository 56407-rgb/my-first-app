import streamlit as st

st.set_page_config(page_title="เกมทายวรรคดีไทย", page_icon="📜")

st.title("👑 เกมทายวรรคดีไทยรอบรู้ 📜")

# รายการคำถามและเฉลย
questions = [
    ("ยักษ์กายสีเขียว ผู้ครองเมืองลงกา ในเรื่องรามเกียรติ์ คือใคร?", "ทศกัณฐ์"),
    ("สัตว์พาหนะของสุดสาครที่มีหัวเป็นมังกร ตัวเป็นม้า ชื่อว่าอะไร?", "ม้านิลมังกร"),
    ("วรรคดีเรื่องใดมีตัวละครเอกชื่อ ขุนแผน และ ขุนช้าง?", "ขุนช้างขุนแผน"),
    ("นางเอกในเรื่องรามเกียรติ์ที่เป็นมเหสีของพระราม ชื่ออะไร?", "นางสีดา"),
    ("กวีเอกสี่แผ่นดินผู้แต่งวรรคดีเรื่อง พระอภัยมณี คือใคร?", "สุนทรภู่")
]

# จัดการ State ระบบ
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "answered" not in st.session_state:
    st.session_state.answered = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

def reset_game():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.answered = False
    st.session_state.last_result = None

# หน้าแรกก่อนเริ่มเกม
if not st.session_state.game_started:
    st.write("กดปุ่มด้านล่างเพื่อเริ่มทดสอบความรู้!")
    if st.button("🎮 เริ่มเล่นเกม", type="primary"):
        reset_game()
        st.rerun()

# หน้าสรุปผลลัพธ์
elif st.session_state.game_over:
    st.subheader("🎯 จบการทดสอบ!")
    score = st.session_state.score
    total = len(questions)
    
    st.metric(label="คะแนนรวมของคุณ", value=f"{score} / {total}")
    
    if score == 5:
        st.balloons()
        st.success("ผ่านระดับเทพ! (เซียนวรรคดีไทยตัวจริง) 🏆✨")
    elif 1 <= score <= 4:
        st.info("พยายามอีกนิด! (แฟนพันธุ์แท้ระดับเริ่มต้น) 💪")
    else:
        st.error("แพ้! (ลองกลับไปอ่านวรรคดีเพิ่มแล้วมาสู้ใหม่นะ) ❌")
        
    if st.button("🔄 เล่นใหม่อีกครั้ง", type="primary"):
        reset_game()
        st.rerun()

# หน้าแสดงคำถาม
else:
    idx = st.session_state.current_index
    q_text, correct_ans = questions[idx]

    st.progress((idx) / len(questions))
    st.caption(f"ข้อที่ {idx + 1} จาก {len(questions)} | คะแนนสะสม: {st.session_state.score}")
    st.markdown(f"**{q_text}**")

    if not st.session_state.answered:
        with st.form(key=f"form_{idx}"):
            user_ans = st.text_input("พิมพ์คำตอบของคุณ:")
            submit_button = st.form_submit_button("ส่งคำตอบ", type="primary")

            if submit_button:
                clean_user = user_ans.strip().replace("นาง", "")
                clean_correct = correct_ans.replace("นาง", "")

                if clean_user == clean_correct or user_ans.strip() == correct_ans:
                    st.session_state.score += 1
                    st.session_state.last_result = ("correct", "ถูกต้อง! 🎉 ได้รับ +1 คะแนน")
                else:
                    st.session_state.last_result = ("incorrect", f"ยังไม่ถูกต้องนะครับ คำตอบคือ: **{correct_ans}**")
                
                st.session_state.answered = True
                st.rerun()
    else:
        res_type, res_msg = st.session_state.last_result
        if res_type == "correct":
            st.success(res_msg)
        else:
            st.error(res_msg)

        if st.button("ข้อถัดไป ➡️", type="primary"):
            st.session_state.current_index += 1
            st.session_state.answered = False
            if st.session_state.current_index >= len(questions):
                st.session_state.game_over = True
            st.rerun()
