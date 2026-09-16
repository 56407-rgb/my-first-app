import streamlit as st

st.set_page_config(page_title="เกมทายวรรคดีไทย", page_icon="📜")

st.title("👑 เกมทายวรรคดีไทยรอบรู้ 📜")
st.caption("ตอบคำถามด้านล่างให้ครบทุกข้อ แล้วกดส่งคำตอบเพื่อดูผลคะแนนได้ทันที")

# รายการคำถามและเฉลย
questions = [
    ("1. ยักษ์กายสีเขียว ผู้ครองเมืองลงกา ในเรื่องรามเกียรติ์ คือใคร?", "ทศกัณฐ์"),
    ("2. สัตว์พาหนะของสุดสาครที่มีหัวเป็นมังกร ตัวเป็นม้า ชื่อว่าอะไร?", "ม้านิลมังกร"),
    ("3. วรรคดีเรื่องใดมีตัวละครเอกชื่อ ขุนแผน และ ขุนช้าง?", "ขุนช้างขุนแผน"),
    ("4. นางเอกในเรื่องรามเกียรติ์ที่เป็นมเหสีของพระราม ชื่ออะไร?", "นางสีดา"),
    ("5. กวีเอกสี่แผ่นดินผู้แต่งวรรคดีเรื่อง พระอภัยมณี คือใคร?", "สุนทรภู่")
]

# แบบฟอร์มคำถามรวมในหน้าเดียว
with st.form("quiz_form"):
    user_inputs = []
    for idx, (q_text, _) in enumerate(questions):
        ans = st.text_input(q_text, key=f"q_{idx}")
        user_inputs.append(ans)
    
    submitted = st.form_submit_button("🏆 ส่งคำตอบทั้งหมด", type="primary")

# แสดงเฉลยและสรุปผลหลังกดส่งคำตอบ
if submitted:
    score = 0
    st.divider()
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
    
    # เกณฑ์ประเมินผู้เล่น
    if score == 5:
        st.balloons()
        st.success("ผ่านระดับเทพ! (เซียนวรรคดีไทยตัวจริง) 🏆✨")
    elif 1 <= score <= 4:
        st.info("พยายามอีกนิด! (แฟนพันธุ์แท้ระดับเริ่มต้น) 💪")
    else:
        st.error("แพ้! (ลองกลับไปอ่านวรรคดีเพิ่มแล้วมาสู้ใหม่นะ) ❌")
