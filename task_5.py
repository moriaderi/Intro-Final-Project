from task_1 import Task1  # Import Task1 for handling sentence cleaning and people data processing
from task_2 import Task2  # Import Task2 for handling k-sequences generation
import json  # Import json module to handle JSON file operations

class Task5:
    def __init__(self, sentences_file: str = None, people_file: str = None, remove_file: str = None,
                 maximal_n: int = None, question_number: int = 5, preprocessed_file: str = None):
        """Initializes Task5 with either raw files or preprocessed JSON"""
        self.max_n = maximal_n  # Store the maximal sequence length
        self.question_number = question_number  # Store the question number (default 5)

        if preprocessed_file:
            # If preprocessed file is provided, load data from the preprocessed JSON
            self.load_from_preprocessed(preprocessed_file)
        else:
            # Otherwise, process raw data files for sentences, remove words, and people
            self.task1 = Task1(sentences_file, people_file, remove_file)  # Initialize Task1 for processing sentences and people data
            self.task2 = Task2(sentences_file, remove_file, maximal_n)  # Initialize Task2 for generating K-sequences
            self.removed_words = self.task1.load_remove_words(remove_file)  # Load words to remove from sentences
            self.sentences = self.task1.load_data(sentences_file)  # Load sentences from file
            self.cleaned_sentences = self.task1.clean_text(self.sentences, self.removed_words)  # Clean the sentences by removing unwanted words
            # Load and sort people data from the people file
            self.people_data = sorted(self.task1.load_data(people_file), key=lambda x: x[0].lower())

    def load_from_preprocessed(self, preprocessed_file: str):
        """Loads preprocessed data from Task1's JSON output"""
        try:
            # Attempt to open and read the preprocessed file
            with open(preprocessed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse the JSON data from the file
                if "Question 1" not in data:  # Check if the expected structure is present in the data
                    raise ValueError("Invalid JSON structure")

                # Load sentences
                if "Processed Sentences" in data["Question 1"]:
                    # If valid, extract and clean the processed sentences
                    self.cleaned_sentences = [
                        " ".join(sentence) if isinstance(sentence, list) else sentence  # Join lists of words into sentences
                        for sentence in data["Question 1"]["Processed Sentences"]
                    ]

                # Load people data
                if "Processed Names" in data["Question 1"]:
                    # If valid, extract and sort processed names (people data)
                    self.people_data = sorted(data["Question 1"]["Processed Names"],
                                              key=lambda x: x[0] if isinstance(x, list) and x else '')
                else:
                    raise ValueError("Missing processed names in JSON")  # Raise error if missing processed names

        except Exception as e:
            # Handle any errors during file reading or data extraction
            print(f"Error loading preprocessed file: {str(e)}")
            raise

    def find_person_mentions(self, person_name, aliases, sentence):
        """Finds mentions of a person's name or aliases in a given sentence"""
        full_name = ' '.join(person_name)  # Join the person's name into a single string
        if full_name in sentence:  # Check if the full name appears in the sentence
            return True

        for alias_group in aliases:  # Check for aliases
            full_alias = ' '.join(alias_group)  # Join each alias group into a single string
            if full_alias in sentence:  # Check if the alias appears in the sentence
                return True

        for name_part in person_name:  # Check for partial name mentions
            if name_part in sentence.split():  # If any part of the name appears as a word in the sentence
                return True

        return False  # Return False if no mentions were found

    def run_task_5(self):
        """Runs Task 5 by processing people mentions and their K-sequences"""
        person_contexts = {}  # Dictionary to store context and K-sequences for each person

        for person in self.people_data:
            main_name = person[0]  # Extract the main name of the person
            aliases = person[1:] if len(person) > 1 else []  # Extract aliases if they exist

            # Handle case where the main name is preprocessed (a list of words)
            if isinstance(main_name, list):
                main_name_cleaned = main_name  # Use the preprocessed name directly
            else:
                # Clean the raw name and split it into words
                main_name_cleaned = self.task1.clean_text([main_name], self.removed_words)[0].split()

            # Handle aliases: check if aliases are preprocessed (list of lists) or raw data
            if isinstance(aliases[0], list) if aliases else False:
                aliases_cleaned = aliases  # Use the preprocessed aliases directly
            else:
                # Clean the raw aliases and split them into words
                aliases_cleaned = [self.task1.clean_text([alias], self.removed_words)[0].split()
                                   for alias in aliases if alias.strip()]

            person_key = ' '.join(main_name_cleaned)  # Combine cleaned main name into a single string key
            seqs = set()  # Set to store unique sequences related to the person

            # Loop through each cleaned sentence to find mentions of the person
            for sentence in self.cleaned_sentences:
                if self.find_person_mentions(main_name_cleaned, aliases_cleaned, sentence):
                    # If the person is mentioned in the sentence, generate K-sequences
                    if not hasattr(self, 'task2'):
                        self.task2 = Task2(None, None, self.max_n)  # Initialize Task2 if not already done
                    for seq in self.task2.generate_k_seqs(sentence, self.max_n):
                        seqs.add(tuple(seq.split()))  # Add each generated K-sequence to the set

            if seqs:
                person_contexts[person_key] = seqs  # Store the sequences for this person in the dictionary

        # Prepare results by sorting each person's sequences lexicographically
        results = []
        for person in sorted(person_contexts.keys()):
            seqs = sorted([list(seq) for seq in person_contexts[person]], key=lambda x: ' '.join(x))
            results.append([person, seqs])  # Append the person's name and their sorted sequences

        # Return the results in the expected format
        return {
            f"Question {self.question_number}": {
                "Person Contexts and K-Seqs": results  # Return the final result with persons and their K-sequences
            }
        }
