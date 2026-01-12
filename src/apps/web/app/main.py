from common.logging_config import log_start_end
from rag_core.query.service import create_service_from_env
from common.bootstrap import init_app
import streamlit as st
import logging

init_app("web")
logger = logging.getLogger(__name__)

# --- 起動時に1回だけ Service を作って使い回す ---
@log_start_end
@st.cache_resource
def get_service():
    return create_service_from_env()

def main():
    st.set_page_config(page_title="RAG Chat", page_icon="💬", layout="centered")
    st.title("💬 ChatBotサンプル")

    # サービス初期化（キャッシュされるので初回だけ重い）
    try:
        service = get_service()
    except Exception as e:
        st.error(f"初期化に失敗しました: {e}")
        st.stop()

    # 入力欄
    query = st.text_area("質問を入力してください", height=120, placeholder="例）育児休業について教えてください。")

    # 送信ボタン
    if st.button("送信", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("質問を入力してください。")
            st.stop()

        with st.spinner("回答生成中..."):
            try:
                response = service.ask(query.strip())
            except Exception as e:
                st.error(f"回答生成に失敗しました: {e}")
                st.stop()

        st.subheader("回答")
        st.write(response["answer"])

        # --- 運用・分析用の追加表示 ---
        with st.expander("参照したドキュメント"):
            for doc in response["source_documents"]:
                st.info(doc.page_content) # 根拠となるチャンクを表示

if __name__ == "__main__":
    main()
