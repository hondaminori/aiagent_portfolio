import os
import streamlit as st
from dotenv import load_dotenv

from rag_core.query.service import create_service_from_env
from common.paths import ENV_PATH


# --- 起動時に1回だけ Service を作って使い回す ---
@st.cache_resource
def get_service():
    """
    環境変数を読み込み、サービスを初期化して返します。

    必須の環境変数:
        - OPENAI_API_KEY: OpenAI APIのキー。
        - EMBEDDING_MODEL_NAME: 使用する埋め込みモデルの名前。
        - CHAT_MODEL_NAME: 使用するチャットモデルの名前。

    オプションの環境変数:
        - COLLECTION_NAME: コレクション名 (デフォルト: "WorkRules")。
        - TOP_K: 検索結果の上位K件を返す (デフォルト: 3)。
        - SEARCH_TYPE: 検索タイプ (デフォルト: "similarity")。

    Returns:
        object: 環境変数に基づいて初期化されたサービスオブジェクト。

    Raises:
        RuntimeError: 必須の環境変数が設定されていない場合。
    """
    load_dotenv(ENV_PATH)

    api_key = os.getenv("OPENAI_API_KEY")
    embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
    chat_model_name = os.getenv("CHAT_MODEL_NAME")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が見つかりません (.env を確認してください)")
    if not embedding_model_name:
        raise RuntimeError("EMBEDDING_MODEL_NAME が見つかりません (.env を確認してください)")
    if not chat_model_name:
        raise RuntimeError("CHAT_MODEL_NAME が見つかりません (.env を確認してください)")

    return create_service_from_env(
        api_key=api_key,
        embedding_model_name=embedding_model_name,
        chat_model_name=chat_model_name,
        collection_name=os.getenv("COLLECTION_NAME", "WorkRules"),
        k=int(os.getenv("TOP_K", "3")),
        search_type=os.getenv("SEARCH_TYPE", "similarity"),
    )


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
                answer = service.ask(query.strip())
            except Exception as e:
                st.error(f"回答生成に失敗しました: {e}")
                st.stop()

        st.subheader("回答")
        st.write(answer)


if __name__ == "__main__":
    main()
