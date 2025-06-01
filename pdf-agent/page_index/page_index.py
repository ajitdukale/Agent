import PyPDF2
from page_index.utils import (
    get_number_of_pages,
    get_text_of_pages,
    post_processing,
    add_node_text
)

# Main page index builder
def page_index(
    doc,
    model="mistral",
    toc_check_page_num=10,
    max_page_num_each_node=5,
    max_token_num_each_node=8000,
    if_add_node_id="yes",
    if_add_node_summary="no",
    if_add_doc_description="no",
    if_add_node_text="yes",  # Enable to inject section text
    pdf_parser="PyPDF2"
):
    print("✅ Reading PDF...")
    pdf_reader = PyPDF2.PdfReader(doc)
    num_pages = get_number_of_pages(doc)

    print(f"✅ Extracting text from first {toc_check_page_num} pages for TOC detection...")
    toc_text = get_text_of_pages(doc, 1, min(toc_check_page_num, num_pages), tag=True)

    # 🚧 Simulated ToC structure (replace with actual ToC logic if needed)
    structure = [
        {"structure": "1", "title": "Introduction", "physical_index": 1},
        {"structure": "2", "title": "Methodology", "physical_index": 3},
        {"structure": "3", "title": "Results", "physical_index": 5},
        {"structure": "4", "title": "Conclusion", "physical_index": 7},
    ]

    structure = post_processing(structure, num_pages)

    print("✅ Extracting full page text for chunking...")
    page_list = []
    for i in range(num_pages):
        page_text = pdf_reader.pages[i].extract_text()
        page_list.append((page_text, len(page_text)))

    if if_add_node_text == "yes":
        print("✅ Adding section text into structure...")
        add_node_text(structure, page_list)

    return {
        "structure": structure,
        "page_list": page_list
    }
