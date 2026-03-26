import streamlit as st
import openai
import os
from datetime import datetime

st.set_page_config(page_title="Quora答案生成器", page_icon="📝", layout="wide")

st.markdown("""
<style>
    .main { padding: 2rem; }
    .stTextArea textarea { font-size: 16px; min-height: 150px; }
    .generated-answer { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #ff6a00; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Quora答案生成器")
st.markdown("使用AI自动生成高质量的Quora回答")

with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("OpenAI API Key", type="password", 
                           help="输入你的OpenAI API Key")
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("1. 输入API Key\n2. 输入Quora问题\n3. 点击生成\n4. 复制发布")

if not api_key:
    st.warning("⚠️ 请在左侧输入OpenAI API Key")
    st.stop()

openai.api_key = api_key

question = st.text_area("📝 输入Quora问题", 
                       placeholder="例如：How do I start a clothing brand?",
                       height=100)

col1, col2, col3 = st.columns(3)
with col1:
    tone = st.selectbox("语气", ["专业", "友好", "简洁"])
with col2:
    length = st.selectbox("长度", ["中等 (400词)", "简短", "详细"])
with col3:
    include_brand = st.checkbox("提及品牌", value=True)

if st.button("🚀 生成答案", type="primary", use_container_width=True):
    if not question.strip():
        st.error("❌ 请输入问题")
    else:
        with st.spinner("🤖 正在生成..."):
            try:
                prompt = f"""Write a helpful Quora answer:
                
Question: {question}
Requirements:
- Tone: {tone}
- Start with direct answer
- Use bullet points
- Include specific examples
- {"Mention 'Sanchuan Apparel' naturally once" if include_brand else "No brand mention"}
- 400 words
- End with engaging question"""

                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                answer = response.choices[0].message.content
                
                st.markdown("---")
                st.subheader("✅ 生成的答案")
                st.text_area("复制以下内容", value=answer, height=300)
                
                word_count = len(answer.split())
                st.metric("字数", word_count)
                
                st.success("✅ 生成成功！复制上方内容到Quora发布")
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")