import time
import streamlit as st

st.set_page_config(page_title="เกมทายวรรคดีไทย", page_icon="📜")

st.title("👑 เกมทายวรรคดีไทยรอบรู้ 📜")

# รายการคำถามและเฉลย
questions = [
    ("1. ยักษ์กายสีเขียว ผู้ครองเมืองลงกา ในเรื่องรามเกียรติ์ คือใคร?", "ทศกัณฐ์"),
    ("2. สัตว์พาหนะของสุดสาครที่มีหัวเป็นมังกร ตัวเป็นม้า ชื่อว่าอะไร?", "ม้านิลมังกร"),
    ("3. วรรคดีเรื่องใดมีตัวละครเอกชื่อ ขุนแผน และ ขุนช้าง?", "ขุนช้างขุนแผน"),
    ("4. นางเอกในเรื่องรามเกียรติ์ที่เป็นมเหสีของพระราม ชื่ออะไร?", "นางสีดา"),
    ("5. กวีเอกสี่แผ่นดินผู้แต่งวรรคดีเรื่อง พระอภัยมณี คือใคร?", "สุนทรภู่")
]

TIME_LIMIT = 90  # 1.5 นาที = 90 วินาที

# จัดการ State ระบบ
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# หน้าแรกก่อนเริ่มเล่น
if not st.session_state.game_started:
    st.write("กดปุ่มด้านล่างเพื่อเริ่มเกม (มีเวลาทำทั้งหมด **1 นาที 30 วินาที**)")
    if st.button("🎮 เริ่มเล่นเกม", type="primary"):
        st.session_state.game_started = True
        st.session_state.start_time = time.time()
        st.session_state.submitted = False
        st.rerun()

# เข้าสู่หน้าเล่นเกม
else:
    # คำนวณเวลาคงเหลือ
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

    # แสดงตัวจับเวลาถอยหลัง (Visual Countdown)
    st.components.v1.html(f"""
        <div style="font-family: sans-serif; text-align: center; background-color: #ffebee; padding: 10px; border-radius: 8px; border: 1px solid #ef5350;">
            <h3 style="color: #c62828; margin: 0;">⏱️ เวลาคงเหลือ: <span id="timer">{remaining_time}</span> วินาที</h3>
        </div>
        <script>
            var timeLeft = {remaining_time};
            var timerElement = document.getElementById('timer');
            var countdown = setInterval(function() {{
                if (timeLeft <= 0) {{
                    clearInterval(countdown);
                    timerElement.innerHTML = "0 (หมดเวลา!)";
                }} else {{
                    timeLeft--;
                    timerElement.innerHTML = timeLeft;
                }}
            }}, 1000);
        </script>
    """, height=70)

    # แบบฟอร์มคำถาม 5 ข้อ
    with st.form("quiz_form"):
        user_inputs = []
        for idx, (q_text, _) in enumerate(questions):
            ans = st.text_input(q_text, key=f"q_{idx}")
            user_inputs.append(ans)
        
        submitted = st.form_submit_button("🏆 ส่งคำตอบทั้งหมด", type="primary")

    # ตรวจผลเมื่อกดส่งคำตอบ หรือ เมื่อหมดเวลา
    if submitted or (remaining_time <= 0 and not st.session_state.submitted):
        st.session_state.submitted = True
        used_time = int(time.time() - st.session_state.start_time)
        
        st.divider()
        if remaining_time <= 0 and not submitted:
            st.error("⏰ หมดเวลา 1 นาที 30 วินาทีแล้ว!")
            
        score = 0
        st.subheader("📊 ผลการทดสอบ")
        
        for idx, (q_text, correct_ans) in enumerate(questions):
            user_ans = user_inputs[idx].strip()
            clean_user = user_ans.replace("นาง", "")
            clean_correct = correct_ans.replace("นาง", "")

            if (clean_user != "" and clean_user == clean_correct) or user_ans == correct_ans:
                score += 1
                st.success(f"ข้อ {idx+1}: ถูกต้อง! 🎉 (ตอบ: {user_ans})")
            else:
                display_user = user_ans if user_ans else "ไม่ได้ระบุคำตอบ"
                st.error(f"ข้อ {idx+1}: ผิด ❌ (ตอบ: {display_user} | เฉลย: {correct_ans})")
        
        st.divider()
        st.metric(label="คะแนนรวมของคุณ", value=f"{score} / {len(questions)}")
        st.caption(f"⏱️ ใช้เวลาไปทั้งหมด: {min(used_time, TIME_LIMIT)} วินาที")
        
        # เกณฑ์ประเมิน
        if score == 5:
            st.balloons()
            st.success("ผ่านระดับเทพ! (เซียนวรรคดีไทยตัวจริง) 🏆✨")
        elif 1 <= score <= 4:
            st.info("พยายามอีกนิด! (แฟนพันธุ์แท้ระดับเริ่มต้น) 💪")
        else:
            st.error("แพ้! (ลองกลับไปอ่านวรรคดีเพิ่มแล้วมาสู้ใหม่นะ) ❌")
            
        if st.button("🔄 เล่นใหม่อีกครั้ง"):
            st.session_state.game_started = False
            st.session_state.submitted = False
            st.rerun()
