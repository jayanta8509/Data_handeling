import pandas as pd
import time

def compare_csv_texts_efficient(csv1_path, csv2_path):
    """
    Compare ARTIST_TITLE with name columns between two CSV files efficiently.
    
    csv1_path: CSV with 'ARTIST_TITLE' column
    csv2_path: CSV with 'id' and 'name' columns
    
    Returns: List of IDs where name is unique (not in ARTIST_TITLE)
    """
    
    start_time = time.time()
    
    # Step 1: Load first CSV and create a Set for O(1) lookup
    print("Loading first CSV...")
    df1 = pd.read_csv(csv1_path)
    
    # Create set of all ARTIST_TITLE from first CSV - O(n) operation
    existing_artist_titles = set(df1['ARTIST_TITLE'].astype(str).str.strip().str.lower())
    
    load_time = time.time()
    print(f"First CSV loaded in {load_time - start_time:.3f} seconds")
    print(f"Found {len(existing_artist_titles)} unique ARTIST_TITLE in first CSV")
    
    # Step 2: Load second CSV
    print("Loading second CSV...")
    df2 = pd.read_csv(csv2_path)
    
    # Step 3: Find unique names - O(m) operation with O(1) lookups
    unique_ids = []
    
    for index, row in df2.iterrows():
        name = str(row['name']).strip().lower()
        
        # O(1) lookup in set
        if name not in existing_artist_titles:
            unique_ids.append(row['id'])
    
    end_time = time.time()
    
    print(f"Comparison completed in {end_time - load_time:.3f} seconds")
    print(f"Total execution time: {end_time - start_time:.3f} seconds")
    print(f"Found {len(unique_ids)} unique names in second CSV")
    
    return unique_ids

# Even more optimized version using vectorized operations
def compare_csv_texts_vectorized(csv1_path, csv2_path):
    """
    Ultra-fast vectorized approach using pandas operations
    Compares ARTIST_TITLE with name columns
    """
    
    start_time = time.time()
    
    # Load both CSVs
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    
    # Normalize text (strip whitespace, lowercase)
    df1['artist_title_clean'] = df1['ARTIST_TITLE'].astype(str).str.strip().str.lower()
    df2['name_clean'] = df2['name'].astype(str).str.strip().str.lower()
    
    load_time = time.time()
    
    # Use pandas isin() for vectorized comparison - very fast
    mask = ~df2['name_clean'].isin(df1['artist_title_clean'])
    unique_ids = df2.loc[mask, 'id'].tolist()
    
    end_time = time.time()
    
    print(f"Vectorized comparison completed in {end_time - start_time:.3f} seconds")
    print(f"Found {len(unique_ids)} unique names")
    
    return unique_ids

# Memory-efficient version for very large files
def compare_csv_texts_chunked(csv1_path, csv2_path, chunk_size=10000):
    """
    Memory-efficient approach for very large CSV files
    Compares ARTIST_TITLE with name columns
    """
    
    # Load first CSV into set (assuming it fits in memory)
    df1 = pd.read_csv(csv1_path)
    existing_artist_titles = set(df1['ARTIST_TITLE'].astype(str).str.strip().str.lower())
    
    unique_ids = []
    
    # Process second CSV in chunks
    for chunk in pd.read_csv(csv2_path, chunksize=chunk_size):
        chunk['name_clean'] = chunk['name'].astype(str).str.strip().str.lower()
        
        # Find unique names in this chunk
        mask = ~chunk['name_clean'].isin(existing_artist_titles)
        chunk_unique_ids = chunk.loc[mask, 'id'].tolist()
        unique_ids.extend(chunk_unique_ids)
    
    return unique_ids

# # Example usage
# if __name__ == "__main__":
#     # Replace with your actual file paths
#     csv1_file = "outpt2.csv"      # Has 'ARTIST_TITLE' column
#     csv2_file = "output_letest.csv"     # Has 'id' and 'name' columns
    
#     print("=== Method 1: Set-based approach ===")
#     unique_ids_1 = compare_csv_texts_efficient(csv1_file, csv2_file)


#     print(f"\nUnique IDs (names not in ARTIST_TITLE): {unique_ids_1[:10]}...")  # Show first 10 IDs

#     # Save results to file
#     with open("unique_ids_method_1.txt", "w") as f:
#         for uid in unique_ids_1:
#             f.write(f"{uid}\n")


#     print(f"--------------------Results saved to unique_ids_method1.txt--------------------------------")



    
#     print("\n=== Method 2: Vectorized approach (fastest) ===")
#     unique_ids_2 = compare_csv_texts_vectorized(csv1_file, csv2_file)
    
#     print(f"\nUnique IDs (names not in ARTIST_TITLE): {unique_ids_2[:10]}...")  # Show first 10 IDs
    
#     # Save results to file
#     with open("unique_ids_method_2.txt", "w") as f:
#         for uid in unique_ids_2:
#             f.write(f"{uid}\n")
    
#     print(f"--------------------Results saved to unique_ids_method2.txt--------------------------------")



#     print("\n=== Method 3: Memory-efficient version for very large files ===")
#     unique_ids_3 = compare_csv_texts_chunked(csv1_file, csv2_file)
    
#     print(f"\nUnique IDs (names not in ARTIST_TITLE): {unique_ids_3[:10]}...")  # Show first 10 IDs
    
#     # Save results to file
#     with open("unique_ids_method_3.txt", "w") as f:
#         for uid in unique_ids_2:
#             f.write(f"{uid}\n")
    
#     print(f"--------------------Results saved to unique_ids_method3.txt--------------------------------")