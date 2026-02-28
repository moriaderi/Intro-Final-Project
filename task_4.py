import json  # Importing the json module to handle JSON file operations
from task_1 import Task1  # Import Task1 for handling sentence data and cleaning
from task_2 import Task2  # Import Task2 for handling k-sequences and their generation
from typing import List  # Import List for type hinting


class Task4:
    def __init__(self, sentences_file: str, remove_file: str, k_seqs_file: str = None, question_number: int = 4,
                 preprocessed_file: str = None):
        """Initializes Task4 with file paths and creates an instance of Task1 for cleaning sentences"""
        self.sentences_file = sentences_file  # Store path to sentences file
        self.remove_file = remove_file  # Store path to remove words file
        self.k_seqs_file = k_seqs_file  # Store path to k-sequences file
        self.question_number = question_number  # Store the question number (default 4)
        self.task1 = Task1(sentences_file, "", remove_file, 1)  # Initialize Task1 instance

        # If preprocessed file is provided, load data from the preprocessed JSON
        if preprocessed_file:
            self.load_from_preprocessed(preprocessed_file)
        else:
            # Otherwise, load raw files for sentences and remove words
            self.load_from_raw_files(sentences_file, remove_file)

    def load_from_preprocessed(self, preprocessed_file: str):
        """Loads preprocessed data from Task1's JSON output"""
        try:
            # Attempt to open and read the preprocessed file
            with open(preprocessed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse the JSON data from the file
                # Check if the expected structure is present in the data
                if "Question 1" in data and "Processed Sentences" in data["Question 1"]:
                    # If valid, extract and clean the processed sentences
                    self.cleaned_sentences = [
                        " ".join(sentence)  # Join words into sentences
                        for sentence in data["Question 1"]["Processed Sentences"]
                    ]
                else:
                    raise ValueError("Invalid JSON structure")  # Raise error if structure is invalid
        except Exception as e:
            # Handle any errors that occur during file reading or data extraction
            print(f"Error loading preprocessed file: {str(e)}")
            raise

    def load_from_raw_files(self, sentences_file: str, remove_file: str):
        """Loads and processes data from raw input files"""
        task1 = Task1(sentences_file, "", remove_file, 2)  # Initialize Task1 for processing
        # Clean the text by removing unwanted words using Task1's methods
        self.cleaned_sentences = task1.clean_text(
            task1.load_data(sentences_file),  # Load sentence data from the raw sentences file
            task1.load_remove_words(remove_file)  # Load the list of words to be removed from the text
        )

    def load_k_seqs(self, json_file_path: str) -> List[List[str]]:
        """Loads K-sequences from the provided JSON file and returns the list of sequences"""
        try:
            # Attempt to open and read the K-sequences file
            with open(json_file_path, 'r') as file:
                k_seqs_data = json.load(file)  # Parse the JSON data from the K-sequences file
                # Check if "keys" exists and is not empty
                if not k_seqs_data.get("keys"):
                    print(f"Warning: No K-sequences found in {json_file_path}")
                    return []  # Return an empty list if no K-sequences are found
                return k_seqs_data["keys"]  # Return the list of K-sequences
        except Exception as e:
            # Handle any errors during file reading or data extraction
            print(f"Error loading K-seq JSON file: {e}")
            return []  # Return an empty list if there's an error

    def search_k_seqs_in_sentences(self, k_seqs: List[List[str]], sentences: List[str]) -> List[List]:
        """Searches for K-sequences in sentences and returns a list of matches"""
        if not k_seqs:  # Handle empty k_seqs case
            return []  # Return an empty list if no K-sequences are provided
        result = []  # Initialize an empty list to store results
        max_seq_length = max(
            len(seq) for seq in k_seqs)  # Find the maximum sequence length in the provided K-sequences
        task2 = Task2(self.sentences_file, self.remove_file,
                      max_seq_length)  # Initialize Task2 to generate K-sequences of the correct length

        sequences_dict = {}  # Dictionary to hold sequences and corresponding sentences they appear in
        # Loop through each cleaned sentence
        for sentence in sentences:
            sentence_words = tuple(sentence.split())  # Split each sentence into words and convert to tuple
            # Loop over sequence lengths from 1 to max_seq_length
            for num in range(1, max_seq_length + 1):
                seqs_in_sentence = task2.generate_k_seqs(sentence,
                                                         num)  # Generate k-sequences for the current sentence and length
                # Loop through the generated sequences
                for seq in seqs_in_sentence:
                    if seq not in sequences_dict:  # If the sequence is not already in the dictionary
                        sequences_dict[seq] = set()  # Initialize a new set for this sequence
                    sequences_dict[seq].add(sentence_words)  # Add the sentence to the set for this sequence

        # Loop through each provided K-sequence
        for sequence in k_seqs:
            sequence_str = " ".join(sequence)  # Convert the K-sequence from a list of words to a string
            if sequence_str in sequences_dict:  # If the K-sequence is found in the dictionary
                result.append([sequence_str, [list(s) for s in sequences_dict[
                    sequence_str]]])  # Add the sequence and its matching sentences to the result list

        # Sort the results first by sequence length, then lexicographically
        return sorted(result, key=lambda x: (len(x[0].split()), x[0].lower()))  # Sort by sequence length and lexicographically

    def remove_duplicates(self, results: List[List]) -> List[List]:
        """Removes duplicate K-sequences from the results and returns only unique sequences"""
        unique_results = []  # Initialize an empty list to store unique results
        taken_keys = set()  # Set to track already added keys to avoid duplicates
        # Sort results by sequence string lexicographically
        for result in sorted(results, key=lambda x: x[0].lower()):
            key = result[0]  # Get the sequence key (the first element in the result)
            if key not in taken_keys:  # If the sequence hasn't been added already
                unique_results.append(result)  # Add the result to the list of unique results
                taken_keys.add(key)  # Mark this sequence as added
        return unique_results  # Return the list of unique results

    def run_task_4(self):
        """Runs Task 4 by processing K-sequences and finding them in the cleaned sentences"""
        if not self.k_seqs_file:  # If no K-sequences file is provided, raise an error
            raise ValueError("K-sequences file path is required")

        k_seqs = self.load_k_seqs(self.k_seqs_file)  # Load the K-sequences from the provided file
        k_seqs.sort(key=lambda seq: " ".join(seq))  # Sort the K-sequences lexicographically
        results = self.search_k_seqs_in_sentences(k_seqs, self.cleaned_sentences)  # Search for matches in the sentences

        # Sort sentences in each result lexicographically
        for result in results:
            result[1].sort(key=lambda x: " ".join(x).lower())

        unique_results = self.remove_duplicates(results)  # Remove duplicates from the results

        return {
            "Question 4": {
                "K-Seq Matches": unique_results  # Return the final result with unique matches
            }
        }
