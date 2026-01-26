"""
Ragasの実行ファイル
使用頻度は高くないし、これにあまり汎用性を持たせるようなことは不要。
よって、必要に応じてここでゴリゴリと直接処理を書く。
claim_qa.csvもあまり深く考えず、このragasディレクトリに直接入れる。

20260126:
serviceに何もかも押し込んだ故に、個別に何かを使おうとすると非常に面倒になってしまった。
出力内容も整形しておらず見にくい。結果ファイルはプロジェクトルートに出力されてしまう。
'ragas.metrics' is deprecated and will be removed in v1.0.と出るが対応方法不明。
本気で使い始めるときにもう一度十分な精査が必要。今のところ使い物にならない。
しかし、もうこれ以上追究するのはやめておく。
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from common.config import CHAT_MODEL_NAME
from common.paths import ENV_PATH
from common.prompts import SYSTEM_PROMPT
from rag_core.preprocessing.embed import create_embedding
from rag_core.preprocessing.vector_backend import load_vectorstore
from rag_core.query.generate import create_chain
from rag_core.query.retrieve import create_retriever
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate

import os
import pandas as pd

load_dotenv(ENV_PATH)

df = pd.read_csv('src/ragas/claim_qa.csv')

api_key = os.getenv("OPENAI_API_KEY")

# 結果を収集するためのリストを定義
results = []

embedding = create_embedding()

vectordb = load_vectorstore(embedding=embedding)

retriever = create_retriever(
    vectordb=vectordb
)

llm = ChatOpenAI(
    model_name=CHAT_MODEL_NAME,
    temperature=0,
    api_key=api_key,
    # max_completion_tokens=600,
    # reasoning_effort="none"
)

chain = create_chain(
    retriever=retriever,
    llm=llm,
    system_prompt=SYSTEM_PROMPT
)


# 評価用データセットを行ごとにループ
for _, row in df.iterrows():
    question = row["question"]
    ground_truth = row["ground_truth"]

    result = chain.invoke(question)

    # resultが何の型で返ってくるかによって処理を分岐
    if isinstance(result, dict):
        answer = result.get("answer", "")
    elif hasattr(result, "content"):
        answer = result.content
    else:
        answer = str(result)

    # リトリーバーから取得したコンテキストを収集
    context_docs = retriever.invoke(question)
    context = [doc.page_content for doc in context_docs]

    # 結果をリストへ格納
    results.append({
        "question": question,
        "ground_truth": ground_truth,
        "answer": answer,
        "retrieved_contexts": context
    })

evaluation_df = pd.DataFrame(results)
evaluation_df.head()

llm = ChatOpenAI(
    model_name=CHAT_MODEL_NAME,
    temperature=0.3,
    api_key=api_key,
    n=3,
    # max_completion_tokens=600,
    # reasoning_effort="none"
)

# 評価データセットを evaluate() の処理形式に変換
eval_dataset = Dataset.from_pandas(evaluation_df)

# 評価の実行
evaluation_results = evaluate(
    dataset=eval_dataset,
    metrics=[
        faithfulness,       # 回答が取得したコンテキストに忠実か
        answer_relevancy,   # 回答が質問に関連しているか
        context_precision,  # 取得したコンテキストが質問に適切か
        context_recall      # 必要な情報がコンテキストに含まれているか
    ],
    llm=llm,
    embeddings=embedding
)

# 結果の表示
evaluation_results.to_pandas().head()
df = evaluation_results.to_pandas()
print(df)

# ファイルに文字列を書き込む
with open("output.txt", "w", encoding="utf-8") as f:
   f.write(df.to_string())
