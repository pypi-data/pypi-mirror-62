# -*- coding: utf-8 -*-

from typing import Tuple, Union, List

import codecs

from sklearn.model_selection import train_test_split


def load_ner_data_and_labels(filename: str,
                             delimiter: str = '\t',
                             split: bool = False,
                             split_size: float = 0.1,
                             seed: int = 42):
    """Load ner data and label from a file.

    The file should follow CoNLL format:
    Each line is a token and its label separated by 'delimiter', or a blank line indicating the end of
    a sentence. Like:
    ```
    我 O
    在 O
    上 B-LOC
    海 I-LOC
    上 O
    学 O

    ...
    ```

    Args:
        filename: str. Path to ner file.
        delimiter: str. Delimiter to split token and label.
        split: Boolean. Whether to split into train and test subsets.
        split_size: float. The proportion of test subset, between 0.0 and 1.0
        seed: int. Random seed.

    Returns: If split: return a tuple of 4 list: train data and labels as well as test data and
             labels.
             Otherwise: return a tuple of 2 list: data and labels

    """
    with codecs.open(filename, 'r', encoding='utf8') as reader:
        token_seqs, label_seqs = [], []
        tokens, labels = [], []
        for i, line in enumerate(reader):
            line = line.rstrip()
            if line:
                line_split = line.split(delimiter)
                if len(line_split) == 2:
                    token, label = line_split
                    tokens.append(token)
                    labels.append(label)
                else:
                    raise Exception(f'Format Error at line {i}!'
                                    f' Input file should follow CoNLL format.')
            else:
                if tokens:
                    token_seqs.append(tokens)
                    label_seqs.append(labels)
                    tokens, labels = [], []

        if tokens:  # in case there's no blank line at the end of the file
            token_seqs.append(tokens)
            label_seqs.append(labels)

    if split:
        x_train, x_test, y_train, y_test = train_test_split(token_seqs, label_seqs,
                                                            test_size=split_size, random_state=seed)
        return x_train, y_train, x_test, y_test
    else:
        return token_seqs, label_seqs


def load_text_classification_data_and_labels(
        filename, label_index=0, text_index=1, delimiter='\t', split_mode=0, split_size=0.1,
        use_header=False, seed=42):
    """Load text classification data and label from a file.

    Args:
        filename: str, path to ner file
        delimiter: str, delimiter to split token and label
        label_index: int, refer to which column store the classification label
        text_index:int, refer to which column store the text information
        split_mode: int, if `split_mode` is 1, it will split the dataset into train and valid;
                         if `split_mode` is 2, it will split the dataset into train, valid and test

        split_size: float, the proportion of test subset, between 0.0 and 1.0
        use_header: bool, whether to use first line as the header
        seed: int, random seed

    Returns: If split: tuple(list, list, list, list), train data and labels as well as test data and
             labels.
             Otherwise: tuple(list, list), data and labels

    """
    with codecs.open(filename, 'r', encoding='utf8') as reader:
        token_seqs, label_seqs = [], []
        for i, line in enumerate(reader):
            if use_header and i == 0:
                continue
            line_items = line.strip().split(delimiter)

            text, label = line_items[text_index], line_items[label_index]
            token_seqs.append(list(text))
            label_seqs.append(label)

    if split_mode == 1:
        x_train, x_valid, y_train, y_valid = train_test_split(
            token_seqs, label_seqs, test_size=split_size, stratify=label_seqs, random_state=seed)
        return x_train, y_train, x_valid, y_valid
    elif split_mode == 2:
        x_train, x_holdout, y_train, y_holdout = train_test_split(
            token_seqs, label_seqs, test_size=split_size, stratify=label_seqs, random_state=seed)
        x_valid, x_test, y_valid, y_test = train_test_split(
            x_holdout, y_holdout, test_size=0.5, stratify=y_holdout, random_state=seed)
        return x_train, y_train, x_valid, y_valid, x_test, y_test
    else:
        return token_seqs, label_seqs


def load_spm_data_and_labels(filename: str, delimiter: str = '\t', split_mode: int = 0,
                             split_size: float = 0.2, seed: int = 42) -> \
    Union[Tuple[Tuple[List[str], List[str]], List[str]],
          Tuple[Tuple[List[str], List[str]], List[str], Tuple[List[str], List[str]], List[str]],
          Tuple[Tuple[List[str], List[str]], List[str], Tuple[List[str], List[str]], List[str],
                Tuple[List[str], List[str]], List[str]]]:
    """Load spm data and label from a file.

    The file should follow fixed format:
    Each line is a pair of sentences and its label separated by tab, like text_a \t text_b \t label.

    Args:
        filename: str, path to spm file
        delimiter: str, delimiter to split texts and label
        split_mode: int, if `split_mode` is 1, it will split the dataset into train and valid;
                         if `split_mode` is 2, it will split the dataset into train, valid and test
        split_size: float, the proportion of test subset, between 0.0 and 1.0
        seed: int, random seed

    Returns: If split: tuple((list_a, list_b), list, (list_a, list_b), list), train data pairs and
             labels as well as test data pairs and labels.
             Otherwise: tuple((list_a, list_b), list), data pairs and labels

    """
    # read data file
    with codecs.open(filename, 'r', encoding='utf8') as reader:
        text_a, text_b, labels = [], [], []
        for i, line in enumerate(reader):
            line = line.rstrip()
            line_split = line.split(delimiter)
            if line:
                if len(line_split) == 3:
                    a, b, label = line_split
                    text_a.append(a)
                    text_b.append(b)
                    labels.append(label)
                else:
                    raise Exception(f'Format Error at line {i}!'
                                    f'Input file should follow fixed spm format.')

    # randomly split train data and valid data
    if split_mode == 1:
        x_a_train, x_a_valid, x_b_train, x_b_valid, y_train, y_valid = train_test_split(
            text_a, text_b, labels, test_size=split_size, stratify=labels, random_state=seed)
        return (x_a_train, x_b_train), y_train, (x_a_valid, x_b_valid), y_valid
    # randomly split train data, valid data and test data
    elif split_mode == 2:
        x_a_train, x_a_holdout, x_b_train, x_b_holdout, y_train, y_holdout = train_test_split(
            text_a, text_b, labels, test_size=split_size, stratify=labels, random_state=seed)
        x_a_valid, x_a_test, x_b_valid, x_b_test, y_valid, y_test = train_test_split(
            x_a_holdout, x_b_holdout, y_holdout, test_size=0.5, stratify=y_holdout,
            random_state=seed)
        return (x_a_train, x_b_train), y_train, (x_a_valid, x_b_valid), y_valid, \
               (x_a_test, x_b_test), y_test
    else:
        return (text_a, text_b), labels
