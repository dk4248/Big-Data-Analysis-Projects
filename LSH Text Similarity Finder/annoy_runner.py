from annoy import AnnoyIndex
import numpy as np
import tqdm
import threading
import time

def lsh_runner(embeddings, metric, results_dict, truth_dict, correct_top_5, num_trees=10):
    start_time = time.time()
    num_dimensions = embeddings.shape[1]
    annoy_index = AnnoyIndex(num_dimensions, metric)

    # Add embeddings to the index with progress tracking
    for i in tqdm.tqdm(range(len(embeddings)), desc=f"Adding embeddings to the index ({results_dict}/{metric})", unit="doc"):
        annoy_index.add_item(i, embeddings[i])

    # Build the index
    annoy_index.build(num_trees)

    # Find the top 5 similar documents for each document
    similar_indices = {}
    for i in tqdm.tqdm(range(len(embeddings)), desc=f"Getting similar documents ({results_dict}/{metric})", unit="doc"):
        temp = annoy_index.get_nns_by_item(i, 6)  # Top 5 similar
        temp = temp[1:]  # Remove the first element which is the document itself
        similar_indices[i] = temp
    
    final_similar_indices = {}

    # Convert similar indices dict to truth dict
    for key, value in similar_indices.items():
        final_similar_indices[truth_dict[key+1]] = [truth_dict[val+1] for val in value]

    # save the results to a text file
    with open(f'{results_dict}/annoy_{metric}.txt', 'w') as file:
        for key, value in final_similar_indices.items():
            file.write(f'{key}: {value}\n')

    correct = 0
    total = 0

    for key, value in final_similar_indices.items():
        correct_array = correct_top_5[key]
        for val in value:
            if val in correct_array:
                correct += 1
                
        total += 5
    
    accuracy = correct / total

    with open(f'{results_dict}/annoy_{metric}.txt', 'a') as file:
        file.write(f'Accuracy: {accuracy}\n')

    print(f"LSH with metric {metric} complete. Results saved to '{results_dict}/{metric}.txt'")