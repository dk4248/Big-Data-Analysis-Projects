import faiss
import numpy as np
import tqdm
import time

def faiss_runner(embeddings, metric, results_dict, truth_dict, correct_top_5, num_hash_tables=100):
    start_time = time.time()
    num_dimensions = embeddings.shape[1]

    # Set up FAISS index on CPU
    if metric == 'angular':
        index = faiss.IndexFlatIP(num_dimensions)  # Inner product for cosine similarity
    else:
        index = faiss.IndexFlatL2(num_dimensions)  # L2 distance for Euclidean similarity

    # Add embeddings to index
    index.add(embeddings.astype('float32'))  # Convert to float32 for FAISS
    print("FAISS index built on CPU.")

    # Find the top 5 similar documents for each document
    similar_indices = {}
    for i in tqdm.tqdm(range(len(embeddings)), desc=f"Getting similar documents ({results_dict}/{metric})", unit="doc"):
        query_vector = embeddings[i].reshape(1, -1)
        distances, indices = index.search(query_vector, 6)  # Find 6 nearest neighbors (self + top 5)
        temp = indices[0][1:]  # Remove self index
        similar_indices[i] = temp.tolist()  # Convert to list for compatibility

    final_similar_indices = {}

    # Convert similar indices dict to truth dict
    for key, value in similar_indices.items():
        final_similar_indices[truth_dict[key+1]] = [truth_dict[val+1] for val in value]

    # Save the results to a text file
    with open(f'{results_dict}/faiss_{metric}.txt', 'w') as file:
        for key, value in final_similar_indices.items():
            file.write(f'{key}: {value}\n')

    correct = 0
    total = 0

    # Calculate accuracy
    for key, value in final_similar_indices.items():
        correct_array = correct_top_5[key]
        for val in value:
            if val in correct_array:
                correct += 1
                
        total += 5
    
    accuracy = correct / total

    with open(f'{results_dict}/faiss_{metric}.txt', 'a') as file:
        file.write(f'Accuracy: {accuracy}\n')

    print(f"FAISS LSH with metric {metric} complete. Results saved to '{results_dict}/faiss_{metric}.txt'")
