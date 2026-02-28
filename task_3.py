import json
from task_1 import Task1


class Task3:
    def __init__(self, sentences_file: str = None, people_file: str = None, remove_file: str = None,
                 question_number: int = 3, preprocessed_file: str = None):
        """
        Initializes Task3 with either raw files or preprocessed JSON.
        Either sentences_file, people_file, and remove_file OR preprocessed_file must be provided.
        """
        self.question_number = question_number  # Set the question number for the task (default is 3)
        self.cleaned_sentences = []  # Initialize an empty list for cleaned sentences
        self.cleaned_names = []  # Initialize an empty list for cleaned names

        if preprocessed_file:
            self.load_from_preprocessed(preprocessed_file)  # If preprocessed file is given, load it
        else:
            self.load_from_raw_files(sentences_file, people_file, remove_file)  # Otherwise, load raw files

    def load_from_preprocessed(self, preprocessed_file: str):
        """Loads preprocessed data from Task1's JSON output"""
        try:
            with open(preprocessed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Read the preprocessed JSON data
                if "Question 1" not in data:  # Check if the data contains the correct structure
                    raise ValueError("Invalid JSON structure")  # Raise an error if the structure is invalid

                # Load processed sentences from the JSON file
                if "Processed Sentences" in data["Question 1"]:
                    self.cleaned_sentences = [
                        " ".join(sentence)
                        for sentence in data["Question 1"]["Processed Sentences"]
                    ]  # Convert sentence lists into strings and store in cleaned_sentences

                # Load processed names from the JSON file
                if "Processed Names" in data["Question 1"]:
                    self.cleaned_names = data["Question 1"]["Processed Names"]  # Store processed names
                else:
                    raise ValueError("Missing processed names in JSON")  # Raise an error if names are missing

        except Exception as e:
            print(f"Error loading preprocessed file: {str(e)}")  # Print any error that occurs while loading
            raise  # Re-raise the error to stop further execution

    def load_from_raw_files(self, sentences_file: str, people_file: str, remove_file: str):
        """Loads and processes data from raw input files"""
        task1 = Task1(sentences_file, people_file, remove_file, 3)  # Initialize Task1 to process the raw files
        self.sentences = task1.load_data(sentences_file)  # Load sentences data from the file
        self.remove_words = task1.load_remove_words(remove_file)  # Load the remove words list
        self.cleaned_sentences = task1.clean_text(self.sentences, self.remove_words)  # Clean sentences using remove words
        self.person_names = task1.load_data(people_file)  # Load the people data from the file

        # Clean names and aliases, ensuring no overlap
        for name_data in self.person_names:  # Loop through each name and its aliases
            cleaned_parts = task1.clean_text(name_data, self.remove_words)  # Clean the name and aliases
            if not self.has_overlap(cleaned_parts[0], cleaned_parts[1:]):  # Check for overlap with aliases
                self.cleaned_names.append(cleaned_parts)  # If no overlap, add to cleaned names list
            else:
                print(f"Warning: Overlap found in {name_data[0]} and aliases {name_data[1:]}, skipping.")  # Warning for overlap

    def has_overlap(self, main_name: str, aliases: list) -> bool:
        """Checks if there is any overlap between the main name and its aliases"""
        main_name_words = set(main_name.split())  # Convert the main name to a set of words
        for alias in aliases:  # Loop through each alias
            alias_words = set(alias.split())  # Convert the alias to a set of words
            if not main_name_words.isdisjoint(alias_words):  # Check if there's any overlap between main name and alias
                return True  # Return True if there's overlap
        return False  # Return False if no overlap

    def check_name_mentions(self, sentence: str, name_data: list) -> int:
        """Counts the mentions of a name or its aliases in a sentence"""
        count = 0  # Initialize mention count
        sentence_words = sentence.split()  # Split the sentence into words

        main_name = " ".join(name_data[0]) if isinstance(name_data[0], list) else name_data[0]  # Get the main name
        aliases = name_data[1] if len(name_data) > 1 else []  # Get the aliases (if any)

        # Count mentions of the main name
        for word in main_name.split():
            if word in sentence_words:  # If the word is in the sentence, increment the count
                count += sentence_words.count(word)

        if aliases:  # If there are aliases, count mentions of each alias
            for alias in aliases:
                alias_str = " ".join(alias) if isinstance(alias, list) else alias  # Join alias parts into a string
                alias_words = alias_str.split()  # Split alias into words
                for i in range(len(sentence_words) - len(alias_words) + 1):
                    if sentence_words[i:i + len(alias_words)] == alias_words:  # Check if alias matches a part of the sentence
                        count += 1  # Increment the count if alias is found
                        break  # Break after the first match to avoid double counting

        return count  # Return the total count of mentions

    def count_mentions_in_sentences(self):
        """Counts the mentions of each name in the cleaned sentences"""
        mentions = {}  # Initialize a dictionary to store mentions for each name
        for name_data in self.cleaned_names:  # Loop through each name and its aliases
            main_name = " ".join(name_data[0]) if isinstance(name_data[0], list) else name_data[0]  # Get the main name
            mentions[main_name] = 0  # Initialize the mention count for the main name
            for sentence in self.cleaned_sentences:  # Loop through each cleaned sentence
                mentions[main_name] += self.check_name_mentions(sentence, name_data)  # Count the mentions in each sentence
        return mentions  # Return the dictionary of mentions

    def run_task_3(self):
        """Runs Task 3 to count name mentions and return a sorted list of mentions"""
        mentions = self.count_mentions_in_sentences()  # Get the mentions for each name
        filtered_mentions = {name: count for name, count in mentions.items() if count > 0}  # Filter out names with zero mentions
        sorted_mentions = sorted(filtered_mentions.items(), key=lambda x: x[0])  # Sort mentions alphabetically by name

        return {
            "Question 3": {
                "Name Mentions": sorted_mentions  # Return the sorted list of name mentions
            }
        }
