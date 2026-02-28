from task_1 import Task1  # Import Task1 class to process data from Task 1
from typing import Dict, List  # Import type hinting for Dictionary and List
import json  # Import JSON module for file reading and writing

class Task2:
    def __init__(self, sentences_file: str = None, remove_file: str = None, maximal_n: int = None, question_number: int = 2, preprocessed_file: str = None):
        """Initializes Task2 with either raw files or preprocessed JSON"""
        self.maximal_n = maximal_n  # Maximum sequence length (up to maximal_n)
        self.question_number = question_number  # The question number for the task (default is 2)
        self.cleaned_sentences = []  # Initialize an empty list for storing cleaned sentences

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

    def generate_k_seqs(self, text: str, max_k: int) -> list:
        """Generates all possible sequences of length 1 up to max_k from a given text"""
        words = text.split()  # Split the input text into a list of individual words
        all_seqs = []  # Initialize an empty list to store all generated sequences

        # Generate sequences of lengths from 1 to max_k
        for k in range(1, max_k + 1):  # Iterate over each sequence length from 1 to max_k
            for i in range(len(words) - k + 1):  # Slide a window of size k over the list of words
                # Append the sequence of words of length k to the list of all sequences
                all_seqs.append(' '.join(words[i:i + k]))  # Join the words together and add to the list

        return all_seqs  # Return the list of all generated sequences

    def count_sequences(self) -> Dict[str, int]:
        """Counts the occurrences of each sequence in the cleaned sentences"""
        seq_counts: Dict[str, int] = {}  # Initialize an empty dictionary to store sequence counts

        # Iterate through each cleaned sentence
        for sentence in self.cleaned_sentences:
            for seq in self.generate_k_seqs(sentence, self.maximal_n):  # Generate sequences for each sentence
                # Count each sequence occurrence in the dictionary
                seq_counts[seq] = seq_counts.get(seq, 0) + 1  # Increment the count of the sequence

        return seq_counts  # Return the dictionary of sequence counts

    def run_task_2(self) -> dict:
        """Organizes the counted sequences by length and returns the final formatted result"""
        # Get the sequence counts
        seq_counts = self.count_sequences()

        # Organize sequences by their lengths (1 to maximal_n)
        seq_by_length = {k: [] for k in range(1, self.maximal_n + 1)}  # Initialize dictionary for sequences by length

        # For each sequence, determine its length and group it by length
        for seq, count in seq_counts.items():
            seq_by_length[len(seq.split())].append([seq, count])  # Group sequences by their length

        # Sort sequences in lexicographic order within each length category
        for seqs in seq_by_length.values():
            seqs.sort(key=lambda x: x[0])  # Sort each list of sequences lexicographically

        # Return the result in the expected format
        return {
            f"Question {self.question_number}": {
                f"{self.maximal_n}-Seq Counts": [
                    [f"{k}_seq", seq_by_length[k]]  # Prepare the result with the sequence count for each length
                    for k in range(1, self.maximal_n + 1)  # Iterate through sequence lengths from 1 to maximal_n
                ]
            }
        }
