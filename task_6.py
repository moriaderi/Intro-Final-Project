from collections import defaultdict  # Import defaultdict to count pairs efficiently
from typing import List  # Import necessary type hints for lists and sets
from task_1 import Task1  # Import Task1 class to handle sentence data and cleaning
import json  # Import the json module to handle JSON file operations


class Task6:
    def __init__(self, sentences_file: str = None, people_file: str = None, remove_file: str = None,
                 windowsize: int = None, threshold: int = None, question_number: int = 6,
                 preprocessed_file: str = None):
        """Initializes Task6 with either raw files or preprocessed JSON"""
        self.windowsize = windowsize  # Store the window size for co-occurrence analysis
        self.threshold = threshold  # Store the threshold for counting co-occurrence pairs
        self.question_number = question_number  # Store the question number
        self.cleaned_sentences = []  # Initialize an empty list for cleaned sentences
        self.cleaned_names = []  # Initialize an empty list for cleaned names
        self.processed_names = []  # Initialize an empty list for processed names and aliases
        self.people_data = []  # Initialize an empty list for raw people data

        if preprocessed_file:
            # If preprocessed data is provided, load it
            self.load_from_preprocessed(preprocessed_file)
        else:
            # Otherwise, load and process raw data
            self.load_from_raw_files(sentences_file, people_file, remove_file)

    def load_from_preprocessed(self, preprocessed_file: str):
        """Loads preprocessed data from Task1's JSON output."""
        try:
            with open(preprocessed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse the JSON data from the preprocessed file
                if "Question 1" not in data:
                    raise ValueError("Invalid JSON structure")  # Raise error if the structure is incorrect

                if "Processed Sentences" in data["Question 1"]:
                    # Load the cleaned sentences from the preprocessed data
                    self.cleaned_sentences = [
                        " ".join(sentence)  # Join the words of each sentence into a single string
                        for sentence in data["Question 1"]["Processed Sentences"]
                    ]

                if "Processed Names" in data["Question 1"]:
                    # Load the processed names and aliases
                    self.cleaned_names = data["Question 1"]["Processed Names"]
                    self.processed_names = self.process_people_names()  # Process names and aliases
                else:
                    raise ValueError("Missing processed names in JSON")  # Raise error if names are missing

        except Exception as e:
            print(f"Error loading preprocessed file: {str(e)}")  # Handle errors during file reading or parsing
            raise

    def load_from_raw_files(self, sentences_file: str, people_file: str, remove_file: str):
        """Loads and processes data from raw input files."""
        self.task1 = Task1(sentences_file, people_file,
                           remove_file)  # Initialize Task1 for cleaning sentences and people data

        # Load raw data (sentences and words to remove)
        self.sentences = self.task1.load_data(sentences_file)  # Load the sentences from the given file
        self.remove_words = self.task1.load_remove_words(remove_file)  # Load the words to remove from sentences

        # Load the raw people data
        self.people_data = self.task1.load_data(people_file)  # Load the people data from the provided file

        if not self.people_data:
            # Raise an error if the people data is not loaded correctly
            raise ValueError("No people data loaded correctly. Please check your people file.")

        # Clean the sentences by removing unwanted words
        self.cleaned_sentences = self.task1.clean_text(self.sentences, self.remove_words)
        # Process the people names after loading the people data
        self.processed_names = self.process_people_names()

    def process_people_names(self):
        """This function processes the names and aliases of the people, cleaning and preparing them for use."""
        processed = []  # Initialize an empty list to store the processed names and aliases
        for person in self.people_data:  # Loop through each person in the people data
            name = person[0]  # Extract the main name (first entry in the list)
            aliases = person[1:] if len(person) > 1 else []  # Extract any aliases (if they exist)

            # Clean the main name and aliases
            name_cleaned = self.task1.clean_text([name], self.remove_words)[0].split()  # Clean the main name
            aliases_cleaned = [
                self.task1.clean_text([alias], self.remove_words)[0].split()  # Clean each alias
                for alias in aliases if alias.strip()  # Only include non-empty aliases
            ]
            processed.append([name_cleaned, aliases_cleaned])  # Add the cleaned name and aliases to the processed list
        return processed  # Return the list of cleaned names and aliases

    def generate_windowed_sentences(self, sentences: List[str]) -> List[List[str]]:
        """This function generates overlapping windows of sentences of the specified window size."""
        return [
            sentences[i:i + self.windowsize]  # Create a sub-list of sentences for each window
            for i in range(
                len(sentences) - self.windowsize + 1  # Ensure the windows do not exceed the number of sentences
            )
        ]

    def get_mentioned_people(self, window: List[str]) -> List[List[str]]:
        """This function returns the list of people mentioned in a specific window of sentences."""
        mentioned_people_list = []  # Initialize an empty list to store the mentioned people
        window_text = ' '.join(window)  # Combine the sentences in the window into one string
        window_words = set(
            window_text.split())  # Split the window text into words and convert it to a set for quick lookup

        for person in self.processed_names:  # Loop through the processed names and aliases
            name = person[0]  # Get the main name (first entry in the list)
            aliases = person[1]  # Get the aliases (remaining entries in the list)

            found_name = False  # Flag to check if the main name is found in the window
            for word in name:  # Loop through each word in the main name
                if word in window_words:  # If the word is in the window, set the flag and break
                    found_name = True
                    break

            found_alias = False  # Flag to check if any alias is found in the window
            for alias_group in aliases:  # Loop through each alias group
                for alias_word in alias_group:  # Loop through each word in the alias
                    if alias_word in window_words:  # If the alias word is in the window, set the flag and break
                        found_alias = True
                        break
                if found_alias:  # If an alias is found, break out of the loop
                    break

            if found_name or found_alias:  # If the main name or any alias is found, add the person to the list
                mentioned_people_list.append(name)

        return mentioned_people_list  # Return the list of people mentioned in the window

    def run_task_6(self) -> dict:
        """This function processes the sentences and counts pairs of people that appear together frequently."""
        windows = self.generate_windowed_sentences(
            self.cleaned_sentences)  # Generate overlapping windows from the cleaned sentences
        pair_count = defaultdict(int)  # Initialize a defaultdict to count pairs of people efficiently

        for window in windows:  # Loop through each window of sentences
            mentioned_people = self.get_mentioned_people(window)  # Get the list of people mentioned in this window

            for i in range(len(mentioned_people)):  # Loop through each person in the list of mentioned people
                for j in range(i + 1, len(mentioned_people)):  # Loop through the remaining people to form pairs
                    pair = tuple(sorted(
                        [tuple(mentioned_people[i]), tuple(mentioned_people[j])]))  # Create a sorted pair of people
                    pair_count[pair] += 1  # Increment the count for this pair

        result_pairs = []  # Initialize a list to store the resulting pairs that meet the threshold
        for pair, count in pair_count.items():  # Loop through the pairs and their counts
            if count >= self.threshold:  # If the count meets the threshold, add the pair to the result list
                result_pairs.append([list(pair[0]), list(pair[1])])  # Convert the pair to a list and add to the results

        return {
            "Question 6": {  # Return the result in the required format for Question 6
                "Pair Matches": sorted(result_pairs, key=lambda x: (' '.join(x[0]), ' '.join(x[1])))
            }
        }
