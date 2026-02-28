import sys
import json
import os
import argparse
from task_1 import Task1
from task_2 import Task2
from task_3 import Task3
from task_4 import Task4
from task_5 import Task5
from task_6 import Task6
from task_7 import Task7
from task_8 import Task8
from task_9 import Task9


def load_preprocessed_data(preprocessed_file):
    """Load preprocessed data from a JSON file"""
    try:
        with open(preprocessed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "Question 1" not in data or "Processed Sentences" not in data["Question 1"]:
                return None
            return [" ".join(sentence) for sentence in data["Question 1"]["Processed Sentences"]]
    except PermissionError:
            print(f"Error: Permission denied when trying to read file: {preprocessed_file}")
            sys.exit(1)
    except Exception as e:
        print(f"Error reading file {preprocessed_file}: {str(e)}")
        return None


def load_task6_data(preprocessed_file):
    """Load Task 6 pair matches from a preprocessed JSON file"""
    try:
        with open(preprocessed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "Question 6" in data and "Pair Matches" in data["Question 6"]:
                return data["Question 6"]["Pair Matches"]
            else:
                print(f"Error: File {preprocessed_file} does not contain Task 6 data")
                return None
    except PermissionError:
        print(f"Error: Permission denied when trying to read file: {preprocessed_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading preprocessed file: {str(e)}")
        return None



def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                       help="task number",
                       required=True
                       )
    parser.add_argument('-s', '--sentences',
                       help="Sentence file path",
                       )
    parser.add_argument('-n', '--names',
                       help="Names file path",
                       )
    parser.add_argument('-r', '--removewords',
                       help="Words to remove file path",
                       )
    parser.add_argument('-p', '--preprocessed',
                       action='append',
                       help="json with preprocessed data",
                       )
    # Task specific arguments
    parser.add_argument('--maxk',
                       type=int,
                       help="Max k",
                       )
    parser.add_argument('--fixed_length',
                       type=int,
                       help="fixed length to find",
                       )
    parser.add_argument('--windowsize',
                       type=int,
                       help="Window size",
                       )
    parser.add_argument('--pairs',
                       help="json file with list of pairs",
                       )
    parser.add_argument('--threshold',
                       type=int,
                       help="graph connection threshold",
                       )
    parser.add_argument('--maximal_distance',
                       type=int,
                       help="maximal distance between nodes in graph",
                       )
    parser.add_argument('--qsek_query_path',
                       help="json file with query path",
                       )
    return parser.parse_args(args)


def validate_file_content(file_path: str, file_type: str) -> bool:
    """A function that validate file content"""
    try:
        if file_type == 'qsek_query_path':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'keys' not in data or not data['keys']:
                    return False
                return True

        if file_type == 'preprocessed':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "Question 1" in data and "Processed Sentences" in data["Question 1"]:
                    return bool(data["Question 1"]["Processed Sentences"])
                elif "Question 6" in data and "Pair Matches" in data["Question 6"]:
                    return bool(data["Question 6"]["Pair Matches"])
                return False

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        if not content:
            return False

        if file_type == 'remove words':
            return True
        return len(content) > 1

    except PermissionError:
        print(f"Error: Permission denied when trying to read file: {file_path}")
        sys.exit(1)

    except Exception:
        return False


def check_required_files(files_to_check):
    """A function that checks if all the required files exist"""
    missing = []
    empty_required = False

    for file_path, file_desc in files_to_check:
        if not file_path or not os.path.exists(file_path):
            missing.append(f"Error: The {file_desc} file does not exist: {file_path}")
            continue

        if not validate_file_content(file_path, file_desc):
            if file_desc != 'remove words':
                empty_required = True

    if missing:
        for error in missing:
            print(error)
        return False

    if empty_required:
        print(json.dumps({"result": []}, indent=4))
        sys.exit(0)

    return True


def validate_task_parameters(task_num, args):
    """A function that validates task parameters"""
    if task_num == '2':
        if args.maxk is None:
            print("Error: maxk parameter is required for task 2")
            return False
        if args.maxk < 0:
            print(f"Error: maxk must be a positive number, got {args.maxk}")
            return False

    elif task_num == '5':
        if args.maxk is None:
            print("Error: maxk parameter is required for task 5")
            return False
        if args.maxk < 0:
            print(f"Error: maxk must be a positive number, got {args.maxk}")
            return False

    elif task_num == '6':
        if args.windowsize is None or args.threshold is None:
            print("Error: Both window_size and threshold must be specified for task 6")
            return False
        if args.windowsize < 0:
            print(f"Error: windowsize must be non-negative, got {args.windowsize}")
            return False
        if args.threshold < 0:
            print(f"Error: threshold must be non-negative, got {args.threshold}")
            return False

    elif task_num == '7':
        if args.maximal_distance is None:
            print("Error: maximal_distance parameter is required for task 7")
            return False
        if not args.preprocessed and (args.windowsize is None or args.threshold is None):
            print("Error: windowsize and threshold are required when not using preprocessed data")
            return False
        if args.windowsize is not None and args.windowsize < 0:
            print(f"Error: windowsize must be non-negative, got {args.windowsize}")
            return False
        if args.threshold is not None and args.threshold < 0:
            print(f"Error: threshold must be non-negative, got {args.threshold}")
            return False

    elif task_num == '8':
        if args.fixed_length is None:
            print("Error: fixed_length parameter is required for task 8")
            return False
        if not args.preprocessed and (args.windowsize is None or args.threshold is None):
            print("Error: windowsize and threshold are required when not using preprocessed data")
            return False
        if args.windowsize is not None and args.windowsize < 0:
            print(f"Error: windowsize must be non-negative, got {args.windowsize}")
            return False
        if args.threshold is not None and args.threshold < 0:
            print(f"Error: threshold must be non-negative, got {args.threshold}")
            return False

    elif task_num == '9':
        if args.threshold is None:
            print("Error: threshold parameter is required for task 9")
            return False
        if args.threshold < 0:
            print(f"Error: threshold must be non-negative, got {args.threshold}")
            return False

    return True


def main():
    try:
        args = readargs()

        if args.sentences:
            args.sentences = os.path.normpath(args.sentences)
        if args.names:
            args.names = os.path.normpath(args.names)
        if args.removewords:
            args.removewords = os.path.normpath(args.removewords)
        if args.pairs:
            args.pairs = os.path.normpath(args.pairs)

        # Load preprocessed data if available
        preprocessed_data = None
        preprocessed_task6_data = None

        # Check for preprocessed data first
        if args.preprocessed:
            if args.task in ['2', '3', '4', '5', '6', '9']:
                for prep_file in args.preprocessed:
                    if not os.path.exists(prep_file):
                        print(f"Error: The preprocessed file does not exist: {prep_file}")
                        sys.exit(1)
                    loaded_data = load_preprocessed_data(prep_file)
                    if loaded_data:
                        preprocessed_data = loaded_data
                        break
                if not preprocessed_data:
                    print(f"Error: Could not load valid preprocessed data from {args.preprocessed}")
                    sys.exit(1)

            elif args.task in ['7', '8']:
                for prep_file in args.preprocessed:
                    if not os.path.exists(prep_file):
                        print(f"Error: The preprocessed file does not exist: {prep_file}")
                        sys.exit(1)
                    loaded_pairs = load_task6_data(prep_file)
                    if loaded_pairs:
                        preprocessed_task6_data = loaded_pairs
                        break
                if not preprocessed_task6_data:
                    print(f"Error: Could not load valid preprocessed data from {args.preprocessed}")
                    sys.exit(1)

        if args.task == '1':

            if not check_required_files([
                (args.removewords, 'remove words'),
                (args.sentences, 'sentences'),
                (args.names, 'names')

            ]) or not validate_task_parameters(args.task, args):
                sys.exit(1)

            task = Task1(sentences_file=args.sentences,
                        people_file=args.names,
                        remove_file=args.removewords,
                        question_number=1)
            result = task.run_task_1()
            print(json.dumps(result, indent=4))

        elif args.task in ['2', '3', '4', '5', '6']:
            if not validate_task_parameters(args.task, args):
                sys.exit(1)

            # Only check for required files if no preprocessed data
            if not preprocessed_data and not args.preprocessed:
                required_files = [(args.removewords, 'remove words'),
                                (args.sentences, 'sentences')]

                if args.task in ['3', '5', '6']:
                    required_files.append((args.names, 'names'))

                if not check_required_files(required_files):
                    sys.exit(1)

            if args.task == '2':
                task = Task2(sentences_file=args.sentences if not preprocessed_data else None,
                           remove_file=args.removewords if not preprocessed_data else None,
                           maximal_n=args.maxk,
                           preprocessed_file=args.preprocessed[0] if args.preprocessed else None)
                result = task.run_task_2()
                print(json.dumps(result, indent=4))

            elif args.task == '3':
                task = Task3(sentences_file=args.sentences if not preprocessed_data else None,
                             people_file=args.names if not preprocessed_data else None,
                             remove_file=args.removewords if not preprocessed_data else None,
                             preprocessed_file=args.preprocessed[0] if args.preprocessed else None)
                result = task.run_task_3()
                print(json.dumps(result, indent=4))


            elif args.task == '4':
                if not args.qsek_query_path:
                    print("Error: qsek_query_path is required for task 4")
                    sys.exit(1)
                task = Task4(sentences_file=args.sentences if not preprocessed_data else None,
                             remove_file=args.removewords if not preprocessed_data else None,
                             k_seqs_file=args.qsek_query_path,
                             preprocessed_file=args.preprocessed[0] if args.preprocessed else None)
                result = task.run_task_4()
                print(json.dumps(result, indent=4))

            elif args.task == '5':
                task = Task5(sentences_file=args.sentences if not preprocessed_data else None,
                             people_file=args.names if not preprocessed_data else None,
                             remove_file=args.removewords if not preprocessed_data else None,
                             maximal_n=args.maxk,
                             preprocessed_file=args.preprocessed[0] if args.preprocessed else None)
                result = task.run_task_5()
                print(json.dumps(result, indent=4))


            elif args.task == '6':
                task = Task6(sentences_file=args.sentences if not preprocessed_data else None,
                             remove_file=args.removewords if not preprocessed_data else None,
                             people_file=args.names if not preprocessed_data else None,
                             windowsize=args.windowsize,
                             threshold=args.threshold,
                             preprocessed_file=args.preprocessed[0] if args.preprocessed else None)
                result = task.run_task_6()
                print(json.dumps(result, indent=4))

        elif args.task in ['7', '8']:
            if not validate_task_parameters(args.task, args):
                sys.exit(1)
            # When using preprocessed data from task 6, only check for pairs file
            if args.preprocessed:
                required_files = [(args.pairs, 'pairs')]

            else:
                required_files = [
                    (args.pairs, 'pairs'),
                    (args.removewords, 'remove words'),
                    (args.sentences, 'sentences'),
                    (args.names, 'names')

                ]

            if not check_required_files(required_files):
                sys.exit(1)

            try:
                with open(args.pairs, 'r', encoding='utf-8') as f:
                    connections_data = json.load(f)
                    if 'keys' not in connections_data:
                        print("Error: The pairs file must contain 'keys' field")
                        sys.exit(1)
            except Exception as e:
                print(f"Error reading pairs file: {str(e)}")
                sys.exit(1)

            if args.task == '7':
                task = Task7(
                    preprocessed_file=args.preprocessed[0] if args.preprocessed else None,
                    sentences_file=None if args.preprocessed else args.sentences,
                    people_file=None if args.preprocessed else args.names,
                    people_connections=args.pairs,
                    maximal_distance=args.maximal_distance,
                    remove_file=None if args.preprocessed else args.removewords,
                    windowsize=None if args.preprocessed else args.windowsize,
                    threshold=None if args.preprocessed else args.threshold)
                result = task.run_task_7()
                print(json.dumps(result, indent=4))

            elif args.task == '8':
                task = Task8(
                    sentences_file=None if args.preprocessed else args.sentences,
                    people_file=None if args.preprocessed else args.names,
                    people_connections=args.pairs,
                    k=args.fixed_length,
                    remove_file=None if args.preprocessed else args.removewords,
                    window_size=None if args.preprocessed else args.windowsize,
                    threshold=None if args.preprocessed else args.threshold,
                    preprocessed_pairs=preprocessed_task6_data if args.preprocessed else None)
                result = task.run_task_8(connections_data['keys'])
                print(json.dumps(result, indent=4))

        elif args.task == '9':
            if not validate_task_parameters(args.task, args):
                sys.exit(1)
            # Only check for required files if no preprocessed data
            if not preprocessed_data and not args.preprocessed:
                required_files = [
                    (args.removewords, 'remove words'),
                    (args.sentences, 'sentences')
                ]
                if not check_required_files(required_files):
                    sys.exit(1)
            # Load preprocessed data if available
            preprocessed_json = None
            if args.preprocessed:
                try:
                    with open(args.preprocessed[0], 'r', encoding='utf-8') as f:
                        preprocessed_json = json.load(f)
                except PermissionError:
                    print(f"Error: Permission denied when trying to read preprocessed file")
                    sys.exit(1)
                except Exception as e:
                    print(f"Error loading preprocessed file: {str(e)}")
                    sys.exit(1)
            task = Task9(
                sentences_file=args.sentences if not args.preprocessed else None,
                remove_file=args.removewords if not args.preprocessed else None,
                threshold=args.threshold,
                preprocessed_file=args.preprocessed[0] if args.preprocessed else None
            )
            result = task.run_task_9(preprocessed_json)
            print(json.dumps(result, indent=4))
        else:
            if not args.task.isdigit() or int(args.task) < 1 or int(args.task) > 9:
                print("Invalid task number")
                sys.exit(1)

    except Exception as e:
        print(f"Error during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()