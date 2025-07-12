from preprocessing import preprocess
from embeddings import generate_embeddings
import os
from concurrent.futures import ThreadPoolExecutor
from annoy_runner import lsh_runner
import numpy as np
import json
import multiprocessing
from faiss_gpu_bda import faiss_runner
from lsh_tree import lsh_tree_runner

if __name__ == '__main__':

    print("*"*50)
    print("PREPROCESSING DATA")
    print("*"*50)
    DATA_DIR = 'data'
    TEXT_FILE_PATH = os.path.join(DATA_DIR, 'texts.txt')
    OUTPUT_FILE_PATH = os.path.join(DATA_DIR, 'preprocessed_data.txt')
    RAW_OUTPUT_FILE_PATH = os.path.join(DATA_DIR, 'texts.txt')
    preprocess(TEXT_FILE_PATH, OUTPUT_FILE_PATH)
    print("*"*50)
    print("PREPROCESSING COMPLETED")
    print("*"*50)
    print("\n")

    print("*"*50)
    print("GENERATING EMBEDDINGS")
    print("*"*50)
    EMBEDDINGS_DIR = 'embeddings'
    
    # Check if the directory exists
    if not os.path.exists(EMBEDDINGS_DIR):
        os.makedirs(EMBEDDINGS_DIR)
        
    EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, 'embeddings.npy')
    EMBEDDINGS_RAW_FILE = os.path.join(EMBEDDINGS_DIR, 'embeddings_raw.npy')
    GPU_ID = [0, 1]
    files = [OUTPUT_FILE_PATH, RAW_OUTPUT_FILE_PATH]
    emb_files = [EMBEDDINGS_FILE, EMBEDDINGS_RAW_FILE]
    for _ in range(2):
        p = multiprocessing.Process(target=generate_embeddings, args=(files[_], emb_files[_],GPU_ID[_]))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    print("*"*50)
    print("EMBEDDINGS GENERATED")
    print("*"*50)
    print("\n")

    print("*"*50)
    print("LSH WITH ANNOY")
    print("*"*50)

    EMBEDDINGS = np.load(EMBEDDINGS_FILE)
    EMBEDDINGS_RAW = np.load(EMBEDDINGS_RAW_FILE)

    TRUTH_DICT = {}
    with open(f'{DATA_DIR}/ids.txt', 'r') as file:
        documents = [line.strip() for line in file.readlines()]

    for i in range(len(documents)):
        TRUTH_DICT[i+1] = int(documents[i])

    CORRECT_TOP_5 = {}
    with open(f'{DATA_DIR}/items.json') as file:
        data = json.load(file)

    for docs in documents:
        CORRECT_TOP_5[int(docs)] = [int(x) for x in data[docs]]

    RESULTS_DIR = 'results'
    RESULTS_DIR_RAW = 'results_raw'

    # Check if the directories exist
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(RESULTS_DIR_RAW):
        os.makedirs(RESULTS_DIR_RAW)

    METRICS = ['angular', 'euclidean', 'manhattan', 'hamming']
    rawness = [False, True]

    # Function to call lsh_runner with the appropriate parameters
    def run_lsh(raw, metric):
        if raw:
            lsh_runner(EMBEDDINGS_RAW, metric, RESULTS_DIR_RAW, TRUTH_DICT, CORRECT_TOP_5)
        else:
            lsh_runner(EMBEDDINGS, metric, RESULTS_DIR, TRUTH_DICT, CORRECT_TOP_5)

    # Use ThreadPoolExecutor to run LSH operations in parallel
    with ThreadPoolExecutor(max_workers=len(METRICS) * 2) as executor:
        futures = [
            executor.submit(run_lsh, raw, metric)
            for raw in rawness for metric in METRICS
        ]
        # Wait for all tasks to complete
        for future in futures:
            future.result()

    print("*"*50)
    print("LSH WITH ANNOY COMPLETED")
    print("*"*50)
    print("\n")

    print("*"*50)
    print("LSH WITH FAISS")
    print("*"*50)

    # Function to call faiss_runner with the appropriate parameters
    def run_faiss(raw, metric):
        if raw:
            faiss_runner(EMBEDDINGS_RAW, metric, RESULTS_DIR_RAW, TRUTH_DICT, CORRECT_TOP_5)
        else:
            faiss_runner(EMBEDDINGS, metric, RESULTS_DIR, TRUTH_DICT, CORRECT_TOP_5)

    # Use ThreadPoolExecutor to run LSH operations in parallel
    with ThreadPoolExecutor(max_workers=len(METRICS) * 2) as executor:
        futures = [
            executor.submit(run_faiss, raw, metric)
            for raw in rawness for metric in METRICS
        ]
        # Wait for all tasks to complete
        for future in futures:
            future.result()

    print("*"*50)
    print("LSH WITH FAISS COMPLETED")
    print("*"*50)
    print("\n")

    print("*"*50)
    print("LSH WITH MINHASH")
    print("*"*50)

    # Function to call lsh_tree_runner with the appropriate parameters
    def run_lsh_tree(raw):
        if raw:
            lsh_tree_runner(EMBEDDINGS_RAW, RESULTS_DIR_RAW, TRUTH_DICT, CORRECT_TOP_5, threshold=0.001)
        else:
            lsh_tree_runner(EMBEDDINGS, RESULTS_DIR, TRUTH_DICT, CORRECT_TOP_5, threshold=0.001)

    # Use ThreadPoolExecutor to run LSH operations in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(run_lsh_tree, raw)
            for raw in rawness
        ]
        # Wait for all tasks to complete
        for future in futures:
            future.result()

    print("*"*50)
    print("LSH WITH MINHASH COMPLETED")
    print("*"*50)






