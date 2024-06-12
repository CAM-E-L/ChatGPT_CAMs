import pandas as pd
import string
import csv
import os

import csv
import os


def save_results_to_csv(filename, data, header="text"):

    directory, base_filename = os.path.split(filename)
    base_name, extension = os.path.splitext(base_filename)

    directory = "./output"

    if not os.path.exists(directory):
        os.makedirs(directory)

    new_filename = os.path.join(directory, base_filename)

    counter = 1
    while os.path.exists(new_filename):
        new_filename = os.path.join(directory, f"{base_name}_{counter}{extension}")
        counter += 1

    if new_filename != os.path.join(directory, base_filename):
        print("File already exists. Using new filename:", new_filename)

    with open(new_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([header])
        for entry in data:
            writer.writerow([entry])

    print("Data has been written to", new_filename)
    return new_filename


def preprocess(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def format_results(results):
    formatted_output = "Missing Words:\n"
    if not results["Missing Words"]:
        formatted_output += "None\n"
    else:
        for word, phrase in results["Missing Words"]:
            formatted_output += f"- '{word}' from the phrase '{phrase}'\n"

    formatted_output += "\nPartial Matches:\n"
    if not results["Partial Matches"]:
        formatted_output += "None\n"
    else:
        for word, matched_word, phrase in results["Partial Matches"]:
            formatted_output += (
                f"- '{word}' (from the phrase '{phrase}') partially matches with "
                f"'{matched_word}' in the text.\n"
            )

    return formatted_output


def check_for_missing_matching_words(text, df, partitions, match_threshold_ratio=0.5):
    text = text[0]
    text = preprocess(text.lower())
    words_in_text = set(text.split())

    filtered_df = df[df["partition"].isin(partitions)]

    missing_words = []
    partial_matches = []

    for index, row in filtered_df.iterrows():
        phrase = row["words"]
        individual_words = phrase.lower().split()

        for word in individual_words:
            preprocessed_word = preprocess(word)
            if preprocessed_word not in words_in_text:
                partial_match_found = False
                for text_word in words_in_text:
                    if (
                        preprocessed_word in text_word or text_word in preprocessed_word
                    ) and (
                        len(preprocessed_word) >= len(text_word) * match_threshold_ratio
                        or len(text_word)
                        >= len(preprocessed_word) * match_threshold_ratio
                    ):
                        partial_matches.append((preprocessed_word, text_word, phrase))
                        partial_match_found = True
                        break
                if not partial_match_found:
                    missing_words.append((preprocessed_word, phrase))

    text_check = {"Missing Words": missing_words, "Partial Matches": partial_matches}

    formatted_results = format_results(text_check)
    return formatted_results
