import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader

# files = os.listdir(path='./doc')
# files = [f for f in os.listdir('./doc') if os.path.isfile(os.path.join('./doc', f))]
files = [f for f in os.listdir('./doc') if os.path.isfile(os.path.join('./doc', f))]
# print(files)

from typing import List

documents = []

for file in files:
    loader = PyPDFLoader(os.path.join('./doc', file))
    documents.append(loader.load())


with open("output.txt", "w", encoding="utf-8") as f:
    f.write(documents.__str__())

print(documents)