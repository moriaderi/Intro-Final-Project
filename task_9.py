from collections import defaultdict
from typing import List
from pathlib import Path
import csv
from task_1 import Task1
import json


class Task9:
    def __init__(self, sentences_file: str, remove_file: str, question_number: int = 9, threshold: int = None,
                 preprocessed_file: str = None):
        """
        Initializes the Task9 class with the files required for processing.
        """
        self.task1 = Task1(sentences_file, None, remove_file)  # Initialize Task1 for text cleaning
        self.sentences_file = sentences_file
        self.remove_file = remove_file
        self.threshold = threshold
        self.question_number = question_number
        self.graph = defaultdict(set)  # Dictionary to hold the graph
        self.sentences = []  # List to store sentences
        self.remove_words = None

        if preprocessed_file:
            # Load preprocessed sentences if the preprocessed file is provided
            try:
                with open(preprocessed_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "Question 1" in data and "Processed Sentences" in data["Question 1"]:
                        self.sentences = data["Question 1"]["Processed Sentences"]
            except Exception as e:
                print(f"Error loading preprocessed file: {str(e)}")
                raise
        else:
            # Load the words to remove if no preprocessed file is provided
            self.remove_words = self.task1.load_remove_words(self.remove_file)

    def clean_and_get_words(self, sentence: str) -> List[str]:
        """
        Cleans a sentence by removing unwanted words and returns a list of words.
        """
        cleaned_text = self.task1.clean_text([sentence], self.remove_words)
        if not cleaned_text:
            return []
        return cleaned_text[0].split()  # Return the cleaned sentence as a list of words

    def build_graph(self):
        """
        Builds a graph based on sentences that share at least 'threshold' number of words.
        """
        sentence_count = len(self.sentences)
        for i in range(sentence_count):
            for j in range(i + 1, sentence_count):
                # Compare shared words between two sentences
                shared_words = set(self.sentences[i]).intersection(set(self.sentences[j]))
                if len(shared_words) >= self.threshold:  # If shared words meet the threshold
                    self.graph[i].add(j)  # Add edge from sentence i to sentence j
                    self.graph[j].add(i)  # Add edge from sentence j to sentence i

    def find_groups(self):
        """
        Finds all connected components (groups) in the graph using Depth-First Search (DFS).
        """
        visited = set()  # Set of visited nodes
        groups = []  # List to store all groups

        def dfs(node, group):
            """Helper DFS function to explore connected nodes."""
            visited.add(node)
            group.append(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, group)

        # Traverse each sentence and group them based on DFS
        for node in range(len(self.sentences)):
            if node not in visited:
                group = []
                dfs(node, group)  # Start a DFS from the unvisited node
                groups.append(group)

        return groups  # Return the list of groups

    def group_sentences(self):
        """
        Groups sentences based on shared words and outputs them in a JSON-compatible format.
        """
        self.build_graph()  # Build the graph of sentence connections
        groups = self.find_groups()  # Find all groups (connected components)

        group_output = []
        for group in groups:
            group_sentences = [self.sentences[i] for i in group]  # Collect sentences in each group
            group_sentences.sort()  # Sort sentences within each group
            group_output.append(group_sentences)

        group_output.sort(key=lambda g: (len(g), " ".join(sorted(map(lambda x: " ".join(x), g)))))

        result = []
        for i, group in enumerate(group_output, 1):
            result.append([f"Group {i}", group])  # Add group information to the result

        return {"Question 9": {"group Matches": result}}  # Return the result in the required format

    def run_task_9(self, preprocessed_data: dict = None) -> dict:
        """
        Main processing method that handles loading, cleaning, and grouping sentences.
        """
        try:
            if not self.sentences:
                # If sentences are not already loaded, process them
                if preprocessed_data and "Question 1" in preprocessed_data:
                    self.sentences = preprocessed_data["Question 1"]["Processed Sentences"]
                else:
                    sentences = []
                    # Read sentences from the provided file
                    with Path(self.sentences_file).open('r', encoding='utf-8') as file:
                        csv_reader = csv.reader(file)
                        next(csv_reader)  # Skip the header
                        for row in csv_reader:
                            if row and row[0].strip():
                                sentences.append(row[0].strip())  # Add each sentence to the list
                    # Clean the sentences and store them as lists of words
                    self.sentences = [self.clean_and_get_words(sentence) for sentence in sentences]

            # Group the sentences based on shared words
            return self.group_sentences()

        except Exception as e:
            print(f"Error processing files: {e}")
            # Return empty result in case of an error
            return {
                "Question 9": {
                    "group Matches": []
                }
            }
