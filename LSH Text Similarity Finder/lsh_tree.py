import numpy as np
from datasketch import MinHash, MinHashLSH
import tqdm
import time

def lsh_tree_runner(embeddings, results_dict, truth_dict, correct_top_5, threshold=0.001, num_perm=128):
    """
    Finds similar documents using Locality Sensitive Hashing (LSH) with MinHash.
    
    Parameters:
        embeddings: np.ndarray
            The embeddings for which to find similar documents.
        results_dict: str
            Directory to save results.
        truth_dict: dict
            Dictionary mapping document indices to true document identifiers.
        correct_top_5: dict
            Dictionary mapping document identifiers to the correct top 5 similar documents.
        threshold: float
            The threshold for MinHashLSH.
        num_perm: int
            The number of permutations for MinHash.
    """

    # Start measuring time
    start_time = time.time()
    num_dimensions = embeddings.shape[1]

    # Function to create MinHash for each embedding
    def create_minhash(embeddings):
        minhashes = []
        for i in tqdm.tqdm(range(len(embeddings)), desc="Creating MinHash", unit="doc"):
            m = MinHash(num_perm=num_perm)
            # Update MinHash with the embedding
            for value in embeddings[i]:
                m.update(value.tobytes())  # Convert the value to bytes
            minhashes.append(m)
        return minhashes

    # Function to build LSH
    def build_lsh(minhashes):
        lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)  # Set threshold and number of permutations
        for i, m in enumerate(tqdm.tqdm(minhashes, desc="Building LSH", unit="doc")):
            lsh.insert(i, m)  # Insert MinHash into LSH
        return lsh

    # Create MinHashes for each embedding
    minhashes = create_minhash(embeddings)

    # Build LSH
    lsh = build_lsh(minhashes)

    # Find similar documents
    similar_indices = {}
    for i in tqdm.tqdm(range(len(embeddings)), desc="Finding Similar Documents", unit="doc"):
        # Query the LSH for similar items
        indices = lsh.query(minhashes[i])  # Use the MinHash for the query
        if len(indices) > 6:
            indices = indices[1:6]  # Get the top 5 similar indices
        else:
            indices = indices[1:]
        similar_indices[i] = indices  # Get similar indices
    
    # Process results to match truth_dict
    final_similar_indices = {}
    for key, value in similar_indices.items():
        final_similar_indices[truth_dict[key+1]] = [truth_dict[val+1] for val in value]

    # Calculate accuracy
    correct = 0
    total = 0
    for key, value in final_similar_indices.items():
        correct_array = correct_top_5[key]
        for val in value:
            if val in correct_array:
                correct += 1
        total += len(correct_array)  # Assuming correct_top_5 has exactly 5 elements
    
    accuracy = correct / total if total > 0 else 0

    # Save the similar indices to a file
    with open(f'{results_dict}/lsh_results.txt', 'w') as file:
        for i, indices in final_similar_indices.items():
            file.write(f"Document {i}: {indices}\n")
        file.write(f"Accuracy: {accuracy}\n")

    print(f"LSH with MinHash complete. Results saved to '{results_dict}/lsh_results.txt'")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
