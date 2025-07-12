import os
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from tqdm import tqdm
import time 

def embed_document(text, tokenizer, model, device):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    # Get the GPU ID used by the model for the current batch
    current_gpu = inputs['input_ids'].device.index

    return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy(), current_gpu

def generate_embeddings(input_path, output_path, gpu_id):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = BertModel.from_pretrained('bert-base-uncased')
    model = torch.nn.DataParallel(model).to(device)

    start_time = time.time()
    with open(input_path, 'r') as file:
        documents = [line.strip() for line in file.readlines()]

    print("Document data loaded. Number of documents:", len(documents))

    embeddings = []

    for doc in tqdm(documents, desc=f"Generating embeddings (GPU {gpu_id})", unit="doc"):
        embedding, current_gpu = embed_document(doc, tokenizer, model, device)
        embeddings.append(embedding)

    print("Embeddings generated. Shape:", np.array(embeddings).shape)

    np.save(output_path, embeddings)

    print(f"Embeddings saved to '{output_path}' in {time.time() - start_time} seconds.")
