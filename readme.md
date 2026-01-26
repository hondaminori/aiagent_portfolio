PDFを基に、質問に回答するチャットボットです。
以下のアプリで構成されます。

## アプリ構成

### RAG_CORE
RAG検索の本体です。  
PDF等の内容を取得し、整形し、チャンク化やベクトルDBへの格納、検索の実行をします。

### WebAPI
WebAPI経由で質問を受け取り、回答を返します。
FastAPIを使用して開発しました。

### WebUI
検索を試すためのデモ画面です。Streamlitを使用して開発しました。  
今後、管理系画面を順次追加していきますが、それらもStreamlitを使用して開発します。  
別途Webサーバを立ち上げる手間を省きます。  

## ディレクトリ構成

project-root/  
├─ config  
│　　└─ .env          文字列ベースの設定値を保存  
├─ product/     本番環境用のDockerfile関連  
└─ src/  
　　│  
　　├─ rag_core/         RAG検索の本体  
　　│　　└─ preprocessing/ PDF読み込みや整形、チャンク化、ベクトルDBへの取り込み  
　　│　　└─ query/         検索実行  
　　│  
　　├─ common/  
　　│　　└─ paths.py       各種パス取得  
　　│　　└─ config.py      設定値（Pythonの型で格納する必要があるもの）  
　　│　　└─ propmts.py     プロンプト  
　　│  
　　├─ api/       WebAPI（FastAPI）  
　　│　　└─ app/  
　　└─ web/       WebUIサンプル、管理系画面  
　　 　　└─ app/  


ランサーズ、クラウドワークスで dms3lj という名前で活動しています。
お手伝いできることがあればぜひ連絡ください！