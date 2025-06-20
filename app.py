import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from audio_recorder_streamlit import audio_recorder

API_BASE = "https://ocr1-production-1237ead.up.railway.app"

st.set_page_config(page_title="名片 + 語音辨識 DEMO", layout="centered")
st.title("📇 名片與語音辨識系統（DEMO）")

st.markdown("---")
st.subheader("📤 上傳名片圖片")

image_file = st.file_uploader("請選擇一張名片圖片（JPG/PNG）", type=["jpg", "jpeg", "png"])

if image_file and st.button("🔍 執行 OCR 辨識"):
    with st.spinner("辨識中...請稍候"):
        try:
            files = {"file": (image_file.name, image_file, image_file.type)}
            res = requests.post(f"{API_BASE}/ocr?user_id=1", files=files, timeout=60)
            res.raise_for_status()
            result = res.json()
            st.success("✅ OCR 辨識完成！")

            st.subheader("📝 辨識文字內容")
            st.text_area("OCR 結果", result["text"], height=200)

            if result.get("fields"):
                st.subheader("🤖 LLaMA 欄位萃取結果")
                fields = result["fields"]
                st.markdown(f'''
                - 👤 **姓名**：{fields.get("name", "N/A")}
                - 📞 **電話**：{fields.get("phone", "N/A")}
                - ✉️ **信箱**：{fields.get("email", "N/A")}
                - 🧳 **職稱**：{fields.get("title", "N/A")}
                - 🏢 **公司**：{fields.get("company_name", "N/A")}
                ''')
        except Exception as e:
            st.error(f"❌ OCR 發生錯誤：{e}")

st.markdown("---")
st.subheader("🎙️ 語音備註錄音")

audio = audio_recorder(text="點擊開始錄音，再點擊結束", recording_color="#f63366", neutral_color="#6aa36f", icon_size="2x")

if audio:
    st.audio(audio, format="audio/wav")

    if st.button("📤 上傳語音進行辨識"):
        with st.spinner("辨識中...請稍候"):
            try:
                files = {"file": ("voice.wav", audio, "audio/wav")}
                res = requests.post(f"{API_BASE}/whisper?user_id=1", files=files, timeout=60)
                res.raise_for_status()
                result = res.json()
                st.success("✅ 語音辨識完成！")

                st.subheader("📝 語音文字內容")
                st.text_area("語音辨識結果", result["text"], height=200)

                if result.get("fields"):
                    st.subheader("🤖 LLaMA 欄位萃取結果")
                    fields = result["fields"]
                    st.markdown(f'''
                    - 👤 **姓名**：{fields.get("name", "N/A")}
                    - 📞 **電話**：{fields.get("phone", "N/A")}
                    - ✉️ **信箱**：{fields.get("email", "N/A")}
                    - 🧳 **職稱**：{fields.get("title", "N/A")}
                    - 🏢 **公司**：{fields.get("company_name", "N/A")}
                    ''')
            except Exception as e:
                st.error(f"❌ Whisper 發生錯誤：{e}")
