import json
from typing import List, Dict
from task_6 import Task6  # Import Task6 to use its results


class Task8:
    def __init__(self, sentences_file: str = None, people_file: str = None, people_connections: str = None,
                 k: int = None, remove_file: str = None, window_size: int = None, threshold: int = None,
                 question_number: int = 8, preprocessed_pairs: list = None):
        """Initializes Task8 with either preprocessed pairs or raw files"""
        if k is None:
            raise ValueError("k parameter is required")  # Raise error if 'k' is not provided

        self.k = k  # Store the required path length 'k'
        self.question_number = question_number  # Store the question number (default 8)
        self.task6_pairs = []  # Initialize an empty list to store Task6 pairs

        if preprocessed_pairs:
            # If preprocessed pairs are provided, use them directly
            self.task6_pairs = preprocessed_pairs
        else:
            # If preprocessed pairs are not available, process the raw files with Task6
            if not all([sentences_file, people_file, remove_file, window_size, threshold]):
                raise ValueError("Missing required parameters for non-preprocessed mode")
            self.task6 = Task6(sentences_file, people_file, remove_file, window_size, threshold)
            task6_results = self.task6.run_task_6()  # Run Task6 to get pair matches
            self.task6_pairs = task6_results["Question 6"]["Pair Matches"]  # Store the pair matches from Task6

        # Load people connections from the given file
        with open(people_connections, 'r') as f:
            data = json.load(f)  # Load the connections data from the JSON file
            self.connections = data['keys']  # Store the pairs of people to check for connections

    def _clean_name(self, name: str) -> str:
        """
        Cleans the name by removing unwanted words (e.g., making lowercase and splitting by spaces)
        """
        words = name.lower().split()  # Convert the name to lowercase and split it by spaces
        return " ".join(words)  # Return the cleaned name as a single string

    def _build_graph(self) -> Dict[str, set]:
        """Builds a graph where each node represents a person, and edges represent relationships between people"""
        graph = {}  # Initialize an empty dictionary to represent the graph
        for pair in self.task6_pairs:  # Iterate through each pair in the Task6 pairs
            name1 = ' '.join(pair[0])  # Convert the first name in the pair to a string
            name2 = ' '.join(pair[1])  # Convert the second name in the pair to a string

            cleaned_name1 = self._clean_name(name1)  # Clean the first name
            cleaned_name2 = self._clean_name(name2)  # Clean the second name

            if cleaned_name1 and cleaned_name2:  # Ensure both names are valid (non-empty)
                # Add the names to the graph if not already present
                if cleaned_name1 not in graph:
                    graph[cleaned_name1] = set()
                if cleaned_name2 not in graph:
                    graph[cleaned_name2] = set()

                # Add an edge between the two names (mutual connection)
                graph[cleaned_name1].add(cleaned_name2)
                graph[cleaned_name2].add(cleaned_name1)

        return graph  # Return the built graph

    def _find_paths_of_length_k(self, start: str, target: str, graph: Dict[str, set]) -> bool:
        """Finds if there's a path of length 'k' from 'start' to 'target' in the graph"""

        if self.k == 0:  # If the path length is 0, we are already at the target
            return start == target  # Return True if the start and target are the same

        if self.k == 1:  # If the path length is 1, check for a direct connection
            return target in graph[start]  # Return True if there's an edge between start and target

        visited = {start}  # Set of visited nodes, starting with the 'start' node
        path = [start]  # Initialize the path with the start node
        return self.dfs(start, target, visited, path, graph)  # Use DFS to find a valid path

    def dfs(self, current: str, target: str, visited: set, path: List[str], graph: Dict[str, set]) -> bool:
        """
        Performs Depth-First Search (DFS) to find a path of the required length from 'current' to 'target'.
        """
        if len(path) == self.k + 1 and current == target:  # If we've reached the target at the required path length
            return True
        if len(path) > self.k:  # If we've exceeded the desired path length, return False
            return False

        # Explore the neighbors of the current node
        for next_node in sorted(graph[current]):  # Sort neighbors for consistent order
            if next_node not in visited:  # If the neighbor hasn't been visited yet
                visited.add(next_node)  # Mark the neighbor as visited
                path.append(next_node)  # Add the neighbor to the current path
                if self.dfs(next_node, target, visited, path, graph):  # Recursively search the path
                    return True
                path.pop()  # Backtrack if no path is found
                visited.remove(next_node)  # Remove from visited for further exploration

        return False  # Return False if no valid path is found

    def run_task_8(self, pairs: List[List[str]]) -> dict:
        """A dictionary with the results, including each pair and whether a valid path of length 'k' exists.
        """
        result = []  # Initialize an empty list to store the results
        graph = self._build_graph()  # Build the graph of people connections

        # Iterate over each pair in the connections to check if they are connected with a path of length 'k'
        for pair in self.connections:
            names = sorted([pair[0], pair[1]], key=str.lower)  # Sort the pair alphabetically
            name1, name2 = names[0], names[1]  # Assign the sorted names

            cleaned_name1 = self._clean_name(name1)  # Clean the first name in the pair
            cleaned_name2 = self._clean_name(name2)  # Clean the second name in the pair

            # Check if both names exist in the graph
            if cleaned_name1 not in graph or cleaned_name2 not in graph:
                is_valid = False  # If either name is not in the graph, the pair is not valid
            else:
                # Check if there is a path of length 'k' between the two names
                is_valid = self._find_paths_of_length_k(cleaned_name1, cleaned_name2, graph)

            result.append([name1, name2, is_valid])  # Add the pair and its validity status to the result

        return {
            "Question 8": {
                "Pair Matches": result  # Return the results with pair matches and their validity
            }
        }
