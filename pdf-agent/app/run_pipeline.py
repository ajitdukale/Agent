from page_index import page_index
from app.chunker import extract_chunks_from_tree
from app.embedder import embed_chunks
from app.retriever import VectorStore
from app.rag_qa import generate_rag_answer

def main(pdf_path, question):
    result = page_index(
        doc=pdf_path,
        model="mistral",  # Ollama LLM name
        toc_check_page_num=15,
        max_page_num_each_node=5,
        max_token_num_each_node=8000,
        if_add_node_id="yes",
        if_add_node_summary="no",
        if_add_doc_description="no",
        if_add_node_text="no"
    )

    page_list = result.get("page_list") or []  # May need to extract from internal state
    structure = result["structure"]

    print("✅ Chunking document...")
    chunks = extract_chunks_from_tree(structure, page_list)

    print("✅ Embedding chunks...")
    chunk_embeddings = embed_chunks(chunks)

    print("✅ Indexing into vector store...")
    vs = VectorStore(dim=len(chunk_embeddings[0][1]))
    vs.add(chunk_embeddings)

    print("✅ Processing query...")
    query_embedding = embed_chunks([{"text": question}])[0][1]
    retrieved = vs.search(query_embedding, top_k=5)
    answer = generate_rag_answer(question, retrieved)

    print("\n🧠 Answer:\n", answer)

if __name__ == "__main__":
    main("D:/projects/pdf-agent/docs/sample_pdf.pdf", "What are the key takeaways from the document?")
