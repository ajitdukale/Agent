# # app/rag_qa.py

# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# model_id = "mistralai/Mistral-7B-v0.1"

# # Load tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     device_map="auto",         # Automatically maps to GPU if available
#     torch_dtype="auto"
# )

# # Use transformers pipeline for text generation
# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# def generate_rag_answer(query, retrieved_chunks):
#     context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
#     prompt = f"""Answer the following question based on the context below.

# Context:
# {context}

# Question: {query}

# Answer:"""

#     response = pipe(prompt, max_new_tokens=300, do_sample=False)
#     return response[0]["generated_text"]

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login

from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Manually download config.json with a timeout setting
hf_hub_download("mistralai/Mistral-7B-v0.1", "config.json")


# Authenticate with Hugging Face
login(token="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")

model_id = "mistralai/Mistral-7B-v0.1"

# Load tokenizer and model with authentication
tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token="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")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",         # Automatically maps to GPU if available
    torch_dtype="auto",
    use_auth_token="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"
)

# Use transformers pipeline for text generation
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_rag_answer(query, retrieved_chunks):
    context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
    prompt = f"""Answer the following question based on the context below.

Context:
{context}

Question: {query}

Answer:"""

    response = pipe(prompt, max_new_tokens=300, do_sample=False)
    return response[0]["generated_text"]