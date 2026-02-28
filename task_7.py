import json  # Import the JSON module for reading and writing JSON files
from task_6 import *  # Import all from Task6 (presumably to use its results)
from typing import Set  # Import Set for type hinting


# Task7 class to process and analyze connections between pairs of people
class Task7:
    def __init__(self, preprocessed_file: str = None, sentences_file: str = None,
                 people_file: str = None, people_connections: str = None,
                 maximal_distance: int = None, remove_file: str = None,
                 windowsize: int = None, threshold: int = None,
                 question_number: int = 7):
        """Initialize Task7 with either preprocessed data or raw data"""
        if maximal_distance is None:
            raise ValueError("maximal_distance parameter is required")  # Ensure maximal distance is provided

        self.maximal_distance = maximal_distance  # Store the maximal distance
        self.connections_file = people_connections  # Store the path for the people connections file
        self.question_number = question_number  # Store the question number
        self.task6_pairs = []  # Initialize an empty list for Task6 pairs

        if preprocessed_file:
            # If preprocessed data is provided, load it
            self.load_from_preprocessed(preprocessed_file)
        else:
            # If no preprocessed data, use raw files and perform Task6
            if not all([sentences_file, people_file, remove_file, windowsize, threshold]):
                raise ValueError("Missing required parameters for non-preprocessed mode")
            self.task6 = Task6(sentences_file, people_file, remove_file, windowsize, threshold)
            task6_results = self.task6.run_task_6()  # Run Task6 to get pair matches
            self.task6_pairs = task6_results["Question 6"]["Pair Matches"]  # Store the pair matches

        # Load pairs from the connections file to check for connections
        self._load_pairs_from_json()

    def load_from_preprocessed(self, preprocessed_file: str):
        """Loads preprocessed data from Task6's JSON output."""
        try:
            with open(preprocessed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Load the preprocessed JSON data
                if "Question 6" in data and "Pair Matches" in data["Question 6"]:
                    # Extract the pair matches from the preprocessed data
                    self.task6_pairs = data["Question 6"]["Pair Matches"]
                else:
                    raise ValueError(
                        "Invalid JSON structure: Missing Question 6 data")  # Raise error if the structure is incorrect
        except Exception as e:
            raise ValueError(f"Error loading preprocessed file: {str(e)}")  # Handle loading errors

    def _load_pairs_from_json(self):
        """Load pairs to check from the connections file."""
        try:
            with open(self.connections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Load the JSON file containing pairs to check
                self.pairs_to_check = data.get("keys", [])  # Extract the pairs under "keys"
        except Exception as e:
            raise ValueError(f"Error loading pairs from JSON: {str(e)}")  # Handle loading errors

    def _find_path(self, start: str, end: str, visited: Set[str], path: List[str]) -> bool:
        """Search for an indirect connection between two names"""
        if len(path) > self.maximal_distance + 1:  # If path exceeds the maximal allowed distance, return False
            return False
        if start == end:  # If the start and end names are the same, return True (indicating a path exists)
            return True

        visited.add(start)  # Add the start name to the visited set to avoid cycles

        # Find neighbors (people directly connected to the current name)
        neighbors = set()  # Initialize a set to store neighboring people
        for pair in self.task6_pairs:  # Loop through each pair in the Task6 results
            name1 = ' '.join(pair[0])  # Convert the first name in the pair to a string
            name2 = ' '.join(pair[1])  # Convert the second name in the pair to a string
            if name1 == start and name2 not in visited:  # If start matches and name2 is unvisited
                neighbors.add(name2)  # Add name2 to the neighbors list
            elif name2 == start and name1 not in visited:  # If start matches and name1 is unvisited
                neighbors.add(name1)  # Add name1 to the neighbors list

        # Recursively search through the neighbors
        for neighbor in neighbors:  # Loop through each neighbor
            path.append(neighbor)  # Add the neighbor to the current path
            if self._find_path(neighbor, end, visited, path):  # Recursively search from neighbor to end
                return True  # Return True if a path is found
            path.pop()  # If no path is found, backtrack by removing the neighbor from the path

        return False  # Return False if no path is found

    def is_connected_in_task6(self, name1: str, name2: str) -> bool:
        """
        Check if there is a direct or indirect connection between two names
        """
        # Check direct connection from Task6 results
        for pair in self.task6_pairs:  # Loop through each pair in the Task6 results
            pair_name1 = ' '.join(pair[0])  # Convert the first name to a string
            pair_name2 = ' '.join(pair[1])  # Convert the second name to a string
            if (name1 == pair_name1 and name2 == pair_name2) or \
                    (name1 == pair_name2 and name2 == pair_name1):  # If names match the pair, return True
                return True

        # Check indirect connection (with the maximal distance constraint)
        visited = set()  # Set to track visited names
        path = [name1]  # Initialize the path with the start name
        return self._find_path(name1, name2, visited, path)  # Recursively search for an indirect path

    def run_task_7(self) -> dict:
        """Process the connections and return the search results."""
        result = []  # List to store the results of each pair check
        seen = set()  # Set to track pairs we've already checked to avoid duplicates

        for name1, name2 in self.pairs_to_check:  # Loop through each pair of names to check
            # Sort the names alphabetically
            sorted_names = sorted([name1, name2], key=str.lower)  # Sort pair by lowercase name for consistent ordering
            pair_key = tuple(sorted_names)  # Create a tuple of the sorted names as the key

            # Skip checking if the pair has already been checked
            if pair_key in seen:  # If pair has already been checked
                continue  # Skip this iteration
            seen.add(pair_key)  # Add the pair to the seen set

            # Check if the pair is connected (either directly or indirectly)
            is_connected = self.is_connected_in_task6(sorted_names[0], sorted_names[1])  # Check connection
            result.append([sorted_names[0], sorted_names[1], is_connected])  # Append the result

        # Sort the results by the first name and then by the second name
        result.sort(key=lambda x: (x[0].lower(), x[1].lower()))  # Sort by lexicographical order

        return {
            "Question 7": {  # Return the result in the required format for Question 7
                "Pair Matches": result  # Include the sorted pair matches with connection statuses
            }
        }
