from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, max_tokens=512, overlap=64):
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_tokens, chunk_overlap=overlap)
    return splitter.split_text(text)

def extract_chunks_from_tree(tree, page_list):
    chunks = []
    def recurse(node):
        if "physical_index" in node:
            start = node["physical_index"] - 1
            end = node.get("end_index", start + 1)
            text = "\n".join([page_list[i][0] for i in range(start, end)])
            for chunk in chunk_text(text):
                chunks.append({
                    "title": node["title"],
                    "text": chunk
                })
        if "nodes" in node:
            for child in node["nodes"]:
                recurse(child)
    for node in tree:
        recurse(node)
    return chunks
