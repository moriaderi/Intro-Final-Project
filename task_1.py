import string
import csv
import re
from pathlib import Path
from typing import List, Set


class Task1:
    def __init__(self, sentences_file: str, people_file: str, remove_file: str, question_number: int = 1):
        """Initializes the Task1 class with file paths for sentences, people, remove words, and an optional question number."""
        self.sentences_file = sentences_file
        self.people_file = people_file
        self.remove_file = remove_file
        self.question_number = question_number

    def load_remove_words(self, file_path: str) -> Set[str]:
        """Loads a set of words to remove from the specified file"""
        try:
            with Path(file_path).open('r') as file:
                remove_words = set()  # Initialize an empty set to store words to remove
                for row in csv.reader(file):
                    if row:
                        word = row[0].strip()  # Convert the word to lowercase and strip whitespace
                        cleaned_word = self.clean_text([word], set())  # clean_text expects a list, so I wrap word in a list
                        if cleaned_word:
                            remove_words.add(cleaned_word[0])  # Add the cleaned word (first element of the list)
                return remove_words  # Return the set of words

        except Exception as e:
            print(f"Error: {e}")
            return set()

    def load_data(self, file_path: str) -> List[List[str]]:
        """Loads data from a CSV file, processing either sentences or names"""
        try:
            with Path(file_path).open('r', encoding='utf-8') as file:
                data = []
                csv_reader = csv.reader(file, quotechar='"')
                next(csv_reader)  # Skip the header row

                # Check the number of columns in the first row
                first_row = next(csv_reader)
                if len(first_row) == 2:  #it's the names file
                    if first_row and first_row[0].strip():
                        full_name = first_row[0].strip()
                        aliases = first_row[1].strip() if len(first_row) > 1 else ""
                        aliases_list = [alias.strip() for alias in aliases.split(",")] if aliases else []
                        data.append([full_name] + aliases_list)

                    for row in csv_reader:
                        if row and row[0].strip():
                            full_name = row[0].strip()
                            aliases = row[1].strip() if len(row) > 1 else ""
                            aliases_list = [alias.strip() for alias in aliases.split(",")] if aliases else []
                            data.append([full_name] + aliases_list)
                else:  # Sentences file
                    data.append(first_row[0].strip())  # Ensure I add the first sentence
                    for row in csv_reader:
                        if row and row[0].strip():
                            data.append(row[0].strip())
                return data

        except Exception as e:
            print(f"Error: {e}")
            return []

    def remove_punctuation(self, text: str) -> str:
        """Removes punctuation characters from the provided text"""
        text_without_punctuation = ""  # Initialize an empty string to store the cleaned text
        for char in text:  # Iterate through each character in the text
            if char in string.punctuation:  # If the character is punctuation
                text_without_punctuation += ' '  # Replace punctuation with a space
            else:
                text_without_punctuation += char  # Otherwise, keep the character as is
        return text_without_punctuation  # Return the cleaned text without punctuation

    def remove_unwanted_words(self, text: str, remove_words: Set[str]) -> str:
        """Removes unwanted words from the text based on a set of words to remove"""
        words = text.split()
        cleaned_list = []
        for word in words:
            if word not in remove_words:
                cleaned_list.append(word)
        return ' '.join(cleaned_list)  # Return the cleaned text after removing unwanted words

    def convert_to_lowercase(self, text: str) -> str:
        """Converts the given text to lowercase"""
        return text.lower() # Convert to lowercase and remove leading/trailing whitespace

    def remove_consecutive_whitespaces(self, text: str) -> str:
        """Removes consecutive whitespaces from the provided text"""
        return re.sub(r'\s+', ' ', text).strip()  # Use regular expression to replace multiple spaces with a single space

    def split_sentences_to_words(self, sentences: List[str]) -> List[List[str]]:
        """Splits each sentence into a list of words"""
        result = []
        for sentence in sentences:
            words = sentence.split()
            result.append(words)
        return result

    def clean_text(self, text: List[str], remove_words: Set[str]) -> List[str]:
        """Cleans the text by removing punctuation, unwanted words, converting to lowercase, and removing extra spaces"""
        cleaned_text = []  # Initialize an empty list to store the cleaned text
        for line in text:  # Iterate over each line of text
            if not isinstance(line, str):  # Skip non string lines
                continue
            line = self.remove_punctuation(line)  # Remove punctuation from the line
            line = self.convert_to_lowercase(line)  # Convert the line to lowercase
            line = self.remove_consecutive_whitespaces(line)  # Remove extra whitespaces from the line
            line = self.remove_unwanted_words(line, remove_words)  # Remove unwanted words from the line
            if line.strip():  # If the line is not empty after cleaning (because we don't want to add empty lines)
                cleaned_text.append(line)  # Add the cleaned line to the list
        return cleaned_text  # Return the list of cleaned lines

    def clean_and_split_name(self, name: str, remove_words: Set[str]) -> List[str]:
        """Cleans and splits a name into words after removing unwanted words"""
        cleaned_name = self.clean_text([name], remove_words)
        if not cleaned_name:
            return []
        split_words = cleaned_name[0].split()
        return [word for word in split_words if word.strip()]

    def remove_duplicates_from_names(self, names: List[List[str]]) -> List[List[str]]:
        """Removes duplicate names based on the base name"""
        taken_names = set()  # Set to track names already seen
        unique_names = []
        for name in names:
            # Convert the list of words back to a string for comparison
            full_name = ' '.join(name[0])
            if full_name not in taken_names:
                unique_names.append(name)
                taken_names.add(full_name)
        return unique_names

    def run_task_1(self) -> dict:
        """Runs the main task and returns the cleaned and processed sentences and names"""
        sentences = self.load_data(self.sentences_file)
        removed = self.load_remove_words(self.remove_file)
        cleaned_sentences = self.clean_text(sentences, removed)
        names = self.load_data(self.people_file)
        processed_names = []

        # Process the names and clean them
        for name in names:
            base_name = name[0]
            aliases = name[1:]

            # Clean and split the base name (base_name)
            cleaned_base_name = self.clean_and_split_name(base_name, removed)

            if not cleaned_base_name: #not adding people with an empty main name
                continue
            cleaned_aliases = []
            # If there are aliases, clean and split each alias
            for alias in aliases:
                alias_words = self.clean_and_split_name(alias, removed)
                if alias_words:
                    cleaned_aliases.append(alias_words)
            # Add the base name and the list of processed aliases (or an empty list if no aliases)
            processed_names.append([cleaned_base_name, cleaned_aliases])
        # Remove duplicates based on full names (base names)
        processed_names = self.remove_duplicates_from_names(processed_names)

        return {
            f"Question {self.question_number}": {
                "Processed Sentences": self.split_sentences_to_words(cleaned_sentences),  # Split sentences into words
                "Processed Names": processed_names
            }
        }
