import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

MEDICAL_PROMPT = """
Siz tibbiyot talabalari va shifokorlar uchun professional klinik yordamchisiz. 
Siz faqat tasdiqlangan tibbiy ko'rsatmalar, JSST (WHO) standartlari va farmakologik qo'llanmalar asosida javob berasiz.

Javob berish qoidalari:
1. Tashxislar, dori dozalari va davolash sxemalarini aniq va bandma-band ko'rsating.
2. Har doim dorilarning xalqaro patentlanmagan nomini (XPN) birinchi yozib, qavsda savdo nomlarini keltiring.
3. Javob yakunida har doim klinik vaziyatni individual baholashni eslatib o'ting.
"""

st.set_page_config(page_title="MedAssistant AI", page_icon="🩺", layout="wide")
st.title("🩺 MedAssistant AI — Klinik yordamchi")

mode = st.sidebar.selectbox(
    "Yo'nalishni tanlang:",
    ["Dori dozalari va o'zaro ta'siri", "Klinik keys (Case Study) tahlili", "Tezkor tibbiy ma'lumotnoma"]
)

user_input = st.text_area("Klinik vaziyat yoki dori nomini kiriting:", height=150)

if st.button("Tahlil qilish ✨"):
    if not user_input.strip():
        st.warning("Iltimos, matn kiriting!")
    else:
        with st.spinner("Tahlil qilinmoqda..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                full_prompt = f"{MEDICAL_PROMPT}\n\nFoydalanuvchi so'rovi ({mode}):\n{user_input}"
                response = model.generate_content(full_prompt)
                st.success("Tahlil tayyor:")
                st.markdown(response.text)
            except Exception as e:
                st.error("Xatolik yuz berdi. API kalitni tekshiring.")
