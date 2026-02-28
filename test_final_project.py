import unittest
from task_3 import *
from task_4 import *
from task_5 import *
from task_7 import *
from task_8 import *
import tempfile
from task_9 import *
import json
import unittest
from tempfile import NamedTemporaryFile
import os
from task_6 import Task6


class TestTask1(unittest.TestCase):

    def setUp(self):
        """creating temporary files for the test of task 1"""

        # Create temporary files with sample data
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Sample data for sentences file
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("Harry rode on a silver chariot\n")
        self.sentences_file.write("It shined! like a star of platinum\n")
        self.sentences_file.write("He was known as the red magician\n")
        self.sentences_file.close()

        # Sample data for people file (with header row)
        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter, "The Boy Who Lived"\n')
        self.people_file.write('Hermione Granger, "Granger"\n')
        self.people_file.write('Ron Weasley, "Weasley"\n')
        self.people_file.close()

        # Sample data for words to remove
        self.remove_file.write("on\n")
        self.remove_file.write("a\n")
        self.remove_file.write("he\n")
        self.remove_file.write("as\n")
        self.remove_file.write("of\n")
        self.remove_file.write("it\n")
        self.remove_file.write("was\n")
        self.remove_file.write("the\n")
        self.remove_file.close()

        # Create empty files for testing empty file scenarios
        self.empty_sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.empty_people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.empty_sentences_file.close()
        self.empty_people_file.close()

    def test_run_task_1(self):
        """Test the main function of Task1"""
        # Create Task1 object with paths to the temporary files
        task = Task1(self.sentences_file.name, self.people_file.name, self.remove_file.name)

        # Run task to process data
        result = task.run_task_1()

        # Extract processed sentences and names from the result
        processed_sentences = result[f"Question {task.question_number}"]["Processed Sentences"]
        processed_names = result[f"Question {task.question_number}"]["Processed Names"]

        # Check the number of processed sentences and names
        self.assertEqual(len(processed_sentences), 3, "There should be 3 processed sentences.")
        self.assertEqual(len(processed_names), 3, "There should be 3 processed names.")

        # Check the content of the processed sentences
        self.assertEqual(processed_sentences[0], ["harry", "rode", "silver", "chariot"])
        self.assertEqual(processed_sentences[1], ["shined", "like", "star", "platinum"])
        self.assertEqual(processed_sentences[2], ["known", "red", "magician"])

        # Check the processed names
        self.assertEqual(processed_names[0][0], ["harry", "potter"])
        self.assertEqual(processed_names[0][1], [["boy", "who", "lived"]])
        self.assertEqual(processed_names[1][0], ["hermione", "granger"])
        self.assertEqual(processed_names[1][1], [["granger"]])
        self.assertEqual(processed_names[2][0], ["ron", "weasley"])
        self.assertEqual(processed_names[2][1], [["weasley"]])

    def close_files(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.sentences_file.name,
            self.people_file.name,
            self.remove_file.name,
            self.empty_sentences_file.name,
            self.empty_people_file.name
        ]

        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask2(unittest.TestCase):
    def setUp(self):
        """Create temporary files needed for testing Task2"""
        # Create temporary files
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Sample data for words to remove
        self.remove_file.write("on\n")
        self.remove_file.write("a\n")
        self.remove_file.write("he\n")
        self.remove_file.write("as\n")
        self.remove_file.write("of\n")
        self.remove_file.write("it\n")
        self.remove_file.write("was\n")
        self.remove_file.write("the\n")
        self.remove_file.close()

        # Create a file for repeated sequences in Task2
        self.repeated_sequences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.repeated_sequences_file.write("sentence\n")
        self.repeated_sequences_file.write("Hello world hello\n")
        self.repeated_sequences_file.write("World hello world\n")
        self.repeated_sequences_file.close()

        # Create empty file for testing empty file scenarios
        self.empty_sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.empty_sentences_file.close()

    def test_file_exists(self):
        """Test if the files exist and are accessible"""
        self.assertTrue(os.path.exists(self.repeated_sequences_file.name), "Repeated sequences file does not exist.")
        self.assertTrue(os.path.exists(self.remove_file.name), "Remove words file does not exist.")
        self.assertTrue(os.path.exists(self.empty_sentences_file.name), "Empty sentences file does not exist.")

    def test_can_open_file(self):
        """Test to check if the Task2 files can be opened successfully"""
        try:
            # Open and read the repeated sequences file
            with open(self.repeated_sequences_file.name, 'r', encoding='utf-8') as file:
                file.read()
            # Open and read the remove file
            with open(self.remove_file.name, 'r', encoding='utf-8') as file:
                file.read()
            # Open and read the empty sentences file
            with open(self.empty_sentences_file.name, 'r', encoding='utf-8') as file:
                file.read()
        except Exception as e:
            self.fail(f"Error while opening file: {e}")

    def test_task2(self):
        """Test the main functionalities of Task2"""
        # Testing multiple values of N (1, 2, 3) in a single test
        for n in range(1, 4):  # Test N=1, N=2, N=3
            task = Task2(self.repeated_sequences_file.name, self.remove_file.name, n)
            result = task.run_task_2()

            seq_counts = result["Question 2"][f"{task.maximal_n}-Seq Counts"]
            for seq_count in seq_counts:
                seq_length = seq_count[0]
                sequences = dict(seq_count[1])

                # Ensure the sequences are counted correctly
                if seq_length == 1:
                    self.assertEqual(sequences.get("hello"), 3, "Should find 'hello' 3 times")
                    self.assertEqual(sequences.get("world"), 3, "Should find 'world' 3 times")
                elif seq_length == 2:
                    self.assertEqual(sequences.get("hello world"), 2, "Should find 'hello world' 2 times")
                    self.assertEqual(sequences.get("world hello"), 2, "Should find 'world hello' 2 times")
                elif seq_length == 3:
                    self.assertEqual(sequences.get("hello world hello"), 1, "Should find 'hello world hello' once")
                    self.assertEqual(sequences.get("world hello world"), 1, "Should find 'world hello world' once")

            # Check lexicographic order
            sequences_list = [seq[0] for seq in seq_counts[n - 1][1]]
            self.assertEqual(sequences_list, sorted(sequences_list),
                             f"Sequences of length {n} should be sorted lexicographically")

    def close_files(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.remove_file.name,
            self.repeated_sequences_file.name,
            self.empty_sentences_file.name
        ]

        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask3(unittest.TestCase):
    """Test the main functionalities of Task3 with edge cases"""

    def setUp(self):
        """Prepare test files for Task3"""
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Write test sentences
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("sentence Harry Potter caught the Snitch.\n")
        self.sentences_file.write("sentence The boy who lived saw the game.\n")  # כינוי של Harry Potter
        self.sentences_file.write("sentence Hermione saw the Snitch.\n")
        self.sentences_file.write("sentence Harry Potter was chosen as the wizard.\n")
        self.sentences_file.write("sentence clever witch solved the puzzle.\n")  # כינוי של Hermione
        self.sentences_file.close()

        # Write people data with valid names and aliases (no overlaps)
        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter,"The Boy Who Lived"\n')  # כינוי תקין - אין חפיפה
        self.people_file.write('Hermione Granger,"Clever Witch"\n')   # כינוי תקין - אין חפיפה
        self.people_file.write('Ron Weasley,"King"\n')               # כינוי תקין - אין חפיפה
        self.people_file.close()

        # Write remove words
        self.remove_file.write("the\n")
        self.remove_file.write("a\n")
        self.remove_file.write("as\n")
        self.remove_file.close()

    def test_task3(self):
        task = Task3(self.sentences_file.name, self.people_file.name, self.remove_file.name)
        result = task.run_task_3()
        name_mentions = result["Question 3"]["Name Mentions"]
        self.assertIn(("harry potter", 14), name_mentions)
        self.assertIn(("hermione granger", 6), name_mentions)

    def close_files(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.remove_file.name,
            self.sentences_file.name,
            self.people_file.name
        ]

        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask4(unittest.TestCase):
    """Test the main functionalities of Task4 with edge cases"""

    def setUp(self):
        """Prepare test files for Task4"""
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("the quick brown fox jumps\n")
        self.sentences_file.write("brown fox sleeps\n")
        self.sentences_file.write("quick brown runs\n")
        self.sentences_file.write("fox jumps high\n")
        self.sentences_file.close()

        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file.write("the\n")
        self.remove_file.write("a\n")
        self.remove_file.close()

        self.kseq_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        kseq_data = {
            "keys": [
                ["quick", "brown"],
                ["fox"],
                ["nonexistent"],
                ["fox", "jumps"]
            ]
        }
        json.dump(kseq_data, self.kseq_file)
        self.kseq_file.close()

    def test_task4(self):
        task = Task4(
            sentences_file=self.sentences_file.name,
            remove_file=self.remove_file.name,
            k_seqs_file=self.kseq_file.name
        )
        result = task.run_task_4()
        self.assertIn("Question 4", result)
        self.assertIn("K-Seq Matches", result["Question 4"])

    def tearDown(self):
        """Clean up temporary files"""
        for file_name in [self.sentences_file.name, self.remove_file.name, self.kseq_file.name]:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask5MainFunction(unittest.TestCase):

    def setUp(self):

        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        self.sentences_file.write("sentence\n")
        self.sentences_file.write("Harry Potter fought against Voldemort\n")
        self.sentences_file.write("The Boy Who Lived survived\n")
        self.sentences_file.write("Hermione cast a powerful spell\n")
        self.sentences_file.close()

        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter,"The Boy Who Lived"\n')
        self.people_file.write('Hermione Granger,"Granger"\n')
        self.people_file.close()

        self.remove_file.write("the\n")
        self.remove_file.write("a\n")
        self.remove_file.write("against\n")
        self.remove_file.close()

    def test_run_task_5(self):

        task = Task5(self.sentences_file.name, self.people_file.name, self.remove_file.name, 2)
        result = task.run_task_5()

        self.assertIn("Question 5", result)
        self.assertIn("Person Contexts and K-Seqs", result["Question 5"])

        results = result["Question 5"]["Person Contexts and K-Seqs"]

        self.assertTrue(len(results) > 0)

        for i in range(len(results) - 1):
            self.assertTrue(results[i][0] <= results[i + 1][0])

        for person_result in results:
            sequences = person_result[1]
            for i in range(len(sequences) - 1):
                self.assertTrue(' '.join(sequences[i]) <= ' '.join(sequences[i + 1]))

        for person_result in results:
            for seq in person_result[1]:
                self.assertTrue(1 <= len(seq) <= 2)

    def tearDown(self):
        for file_path in [self.sentences_file.name, self.people_file.name, self.remove_file.name]:
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error removing file {file_path}: {e}")





class TestTask6(unittest.TestCase):
    """Test the main functionality of Task6"""

    def setUp(self):
        """Create temporary test files for Task6"""
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Sample sentences with clear connections
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("Harry Potter talked to Hermione Granger\n")
        self.sentences_file.write("The Boy Who Lived met Granger again\n")
        self.sentences_file.write("Ron Weasley joined the group\n")
        self.sentences_file.close()

        # People data with names and aliases
        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter,"The Boy Who Lived"\n')
        self.people_file.write('Hermione Granger,"Granger"\n')
        self.people_file.write('Ron Weasley,"King"\n')
        self.people_file.close()

        # Words to remove
        self.remove_file.write("the\n")
        self.remove_file.write("to\n")
        self.remove_file.write("again\n")
        self.remove_file.close()

    def test_process(self):
        """Test the main process function of Task6"""
        task = Task6(self.sentences_file.name, self.people_file.name, self.remove_file.name,
                     windowsize=2, threshold=2)
        result = task.run_task_6()

        # Check basic structure
        self.assertIn("Question 6", result)
        self.assertIn("Pair Matches", result["Question 6"])

        # Get the pairs
        pairs = result["Question 6"]["Pair Matches"]

        # Check that pairs exist
        self.assertTrue(len(pairs) > 0, "Should find at least one pair")

        # Verify pair format and order
        for pair in pairs:
            # Each pair should be a list of two lists
            self.assertEqual(len(pair), 2)
            self.assertTrue(isinstance(pair[0], list))
            self.assertTrue(isinstance(pair[1], list))

            # Pairs should be ordered alphabetically
            self.assertTrue(' '.join(pair[0]) <= ' '.join(pair[1]))

    def tearDown(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.sentences_file.name,
            self.people_file.name,
            self.remove_file.name
        ]

        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask7(unittest.TestCase):
    def setUp(self):
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.connections_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.preprocessed_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')

        # Write test data
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("Harry Potter and Ron Weasley studying\n")
        self.sentences_file.write("Ron Weasley with Hermione Granger\n")
        self.sentences_file.close()

        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter,"The Boy Who Lived"\n')
        self.people_file.write('Ron Weasley,"Weasley"\n')
        self.people_file.close()

        self.remove_file.write("and\nwith\n")
        self.remove_file.close()

        json.dump({"keys": [["Harry Potter", "Hermione Granger"]]}, self.connections_file)
        self.connections_file.close()

        json.dump({
            "Question 6": {
                "Pair Matches": [["harry potter", "hermione granger"]]
            }
        }, self.preprocessed_file)
        self.preprocessed_file.close()

    def test_clean_name(self):
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )
        self.assertEqual(task._clean_name("The Harry Potter"), "the harry potter")

    def test_load_task6_pairs(self):
        """Test loading of Task6 pairs"""
        task = Task7(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            maximal_distance=2,
            remove_file=self.remove_file.name,
            windowsize=2,
            threshold=1
        )
        self.assertTrue(hasattr(task, 'task6_pairs'))
        self.assertTrue(isinstance(task.task6_pairs, list))
        self.assertTrue(len(task.task6_pairs) > 0)

    def test_load_pairs_from_json_error(self):
        with open(self.preprocessed_file.name, 'w', encoding='utf-8') as f:
            json.dump({
                "Question 6": {
                    "Pair Matches": [["harry potter", "hermione granger"]]
                }
            }, f)

        task = Task7(
            preprocessed_file=self.preprocessed_file.name,
            people_connections=self.connections_file.name,
            maximal_distance=2
        )

    def test_find_path(self):
        """Test the _find_path method with various scenarios"""
        task = Task7(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            maximal_distance=2,
            remove_file=self.remove_file.name,
            windowsize=2,
            threshold=1
        )

        # Test path to self
        visited = set()
        path = ["harry potter"]
        self.assertTrue(task._find_path("harry potter", "harry potter", visited, path))

        # Test path too long
        task.maximal_distance = 0
        visited = set()
        path = ["harry potter"]
        self.assertFalse(task._find_path("harry potter", "hermione granger", visited, path))

        # Test valid path
        task.maximal_distance = 2
        visited = set()
        path = ["harry potter"]
        self.assertTrue(task._find_path("harry potter", "ron weasley", visited, path))

    def test_is_connected_in_task6(self):
        json_data = {
            "Question 6": {
                "Pair Matches": [["harry potter", "hermione granger"]]
            }
        }
        with open(self.preprocessed_file.name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
        task = Task7(
            preprocessed_file=self.preprocessed_file.name,
            people_connections=self.connections_file.name,
            maximal_distance=2
        )

    def test_run_task_7(self):
        json_data = {
            "Question 6": {
                "Pair Matches": [["harry potter", "hermione granger"]]
            }
        }
        with open(self.preprocessed_file.name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
            f.flush()

        task = Task7(
            preprocessed_file=self.preprocessed_file.name,
            people_connections=self.connections_file.name,
            maximal_distance=2,
            threshold=1
        )
        result = task.run_task_7()
        self.assertIn("Question 7", result)


        self.assertIn("Question 7", result)
        self.assertIn("Pair Matches", result["Question 7"])
        pairs = result["Question 7"]["Pair Matches"]
        self.assertTrue(len(pairs) > 0)

        # Test pair format and sorting
        for pair in pairs:
            self.assertEqual(len(pair), 3)
            self.assertTrue(isinstance(pair[0], str))
            self.assertTrue(isinstance(pair[1], str))
            self.assertTrue(isinstance(pair[2], bool))
            self.assertTrue(pair[0].lower() <= pair[1].lower())

    def test_find_path(self):
        task = Task7(
            sentences_file=self.sentences_file.name,
            people_file=self.people_file.name,
            people_connections=self.connections_file.name,
            maximal_distance=2,
            remove_file=self.remove_file.name,
            windowsize=2,
            threshold=1
        )

    def test_load_task6_pairs(self):
        preprocessed_data = {
            "Question 6": {
                "Pair Matches": [["harry potter", "hermione granger"]]
            }
        }
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            json.dump(preprocessed_data, f)
            preprocessed_file = f.name

        task = Task7(
            preprocessed_file=preprocessed_file,
            people_connections=self.connections_file.name,
            maximal_distance=2
        )
        self.assertTrue(hasattr(task, 'task6_pairs'))
        self.assertTrue(isinstance(task.task6_pairs, list))
        self.assertTrue(len(task.task6_pairs) > 0)
        os.remove(preprocessed_file)



    def tearDown(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.sentences_file.name,
            self.people_file.name,
            self.remove_file.name,
            self.connections_file.name
        ]
        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")


class TestTask8(unittest.TestCase):
    def setUp(self):
        """Set up test files with known content"""
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.people_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.connections_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Sample sentences
        self.sentences_file.write("sentence\n")
        self.sentences_file.write("Harry Potter and Ron Weasley studying\n")
        self.sentences_file.write("Ron Weasley with Hermione Granger\n")
        self.sentences_file.write("The Boy Who Lived with Ron Weasley\n")
        self.sentences_file.write("Hermione Granger working alone\n")
        self.sentences_file.close()

        # People data
        self.people_file.write("Name,Other Names\n")
        self.people_file.write('Harry Potter,"The Boy Who Lived"\n')
        self.people_file.write('Ron Weasley,"Weasley"\n')
        self.people_file.write('Hermione Granger,"Granger"\n')
        self.people_file.close()

        # Words to remove including common articles and prepositions
        self.remove_file.write("and\nwith\nalone\nthe\na\nan\nworking\nstudying\n")
        self.remove_file.close()

        # Connections
        connections_data = {
            "keys": [
                ["Harry Potter", "Ron Weasley"],
                ["Harry Potter", "Hermione Granger"]
            ]
        }
        json.dump(connections_data, self.connections_file)
        self.connections_file.close()

    def test_clean_name(self):
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )
        self.assertEqual(task._clean_name("The Harry Potter"), "the harry potter")
    def test_build_graph(self):
        """Test graph building functionality"""
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )

        graph = task._build_graph()
        self.assertIn("harry potter", graph)
        self.assertIn("ron weasley", graph)
        self.assertTrue(isinstance(graph["harry potter"], set))
        self.assertTrue(isinstance(graph["ron weasley"], set))

    def test_find_paths_of_length_k(self):
        """Test path finding with different k values"""
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )

        # Create a test graph
        graph = {
            "harry potter": {"ron weasley"},
            "ron weasley": {"harry potter", "hermione granger"},
            "hermione granger": {"ron weasley"}
        }

        task.k = 0
        self.assertTrue(task._find_paths_of_length_k("harry potter", "harry potter", graph))

        task.k = 1
        self.assertTrue(task._find_paths_of_length_k("harry potter", "ron weasley", graph))

        task.k = 2
        self.assertTrue(task._find_paths_of_length_k("harry potter", "hermione granger", graph))

    def test_dfs(self):
        """Test depth-first search functionality"""
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )

        # Create a test graph
        graph = {
            "harry potter": {"ron weasley"},
            "ron weasley": {"hermione granger"},
            "hermione granger": set()
        }

        # Test successful path
        visited = {"harry potter"}
        path = ["harry potter"]
        task.k = 2
        self.assertTrue(task.dfs("harry potter", "hermione granger", visited, path, graph))

        # Test path too long
        visited = {"harry potter"}
        path = ["harry potter"]
        task.k = 1
        self.assertFalse(task.dfs("harry potter", "hermione granger", visited, path, graph))

    def test_run_task_8(self):
        """Test the main task execution"""
        task = Task8(
            self.sentences_file.name,
            self.people_file.name,
            self.connections_file.name,
            k=2,
            remove_file=self.remove_file.name,
            window_size=2,
            threshold=1
        )

        result = task.run_task_8([])

        self.assertIn("Question 8", result)
        self.assertIn("Pair Matches", result["Question 8"])
        pairs = result["Question 8"]["Pair Matches"]

        self.assertTrue(len(pairs) > 0)
        for pair in pairs:
            self.assertEqual(len(pair), 3)
            self.assertTrue(isinstance(pair[0], str))
            self.assertTrue(isinstance(pair[1], str))
            self.assertTrue(isinstance(pair[2], bool))
            self.assertTrue(pair[0].lower() <= pair[1].lower())

    def tearDown(self):
        """Clean up temporary files"""
        files_to_remove = [
            self.sentences_file.name,
            self.people_file.name,
            self.remove_file.name,
            self.connections_file.name
        ]
        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")





class TestTask9(unittest.TestCase):
    def setUp(self):
        """Set up the necessary files and environment for testing."""
        self.sentences_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.remove_file = NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        self.sentences_file.write("sentence\n")  # Header
        self.sentences_file.write("The quick brown fox jumped over the lazy dog.\n")
        self.sentences_file.write("A fast brown dog jumped over the lazy fox.\n")
        self.sentences_file.close()

        self.remove_file.write("the\n")
        self.remove_file.write("a\n")
        self.remove_file.write("over\n")
        self.remove_file.close()

        self.threshold = 1

    def test_run_task_9(self):
        """Test the main run_task_9 function."""
        task = Task9(
            self.sentences_file.name,
            self.remove_file.name,
            threshold=self.threshold
        )
        result = task.run_task_9()

        self.assertIn("Question 9", result)
        self.assertIn("group Matches", result["Question 9"])
        groups = result["Question 9"]["group Matches"]
        self.assertTrue(len(groups) > 0)

    def tearDown(self):
        """Clean up temporary files."""
        files_to_remove = [
            self.sentences_file.name,
            self.remove_file.name
        ]

        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except OSError as e:
                print(f"Error removing file {file_name}: {e}")

if __name__ == "__main__":
    unittest.main()






