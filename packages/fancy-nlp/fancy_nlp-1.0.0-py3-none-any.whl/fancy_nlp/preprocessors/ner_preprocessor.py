# -*- coding: utf-8 -*-

import pickle
from typing import List, Optional, Tuple, Dict, Any

import tensorflow as tf
import numpy as np
import jieba
from absl import logging

from fancy_nlp.preprocessors.preprocessor import Preprocessor
from fancy_nlp.utils import pad_sequences_2d, get_len_from_corpus, ChineseBertTokenizer


class NERPreprocessor(Preprocessor):
    """NER preprocessor, which is used to
    1) build all kinds of vocabulary (char, word , label) from training data;
    2) pre-trained embedding matrix using training corpus;
    3) prepare feature input for ner model;
    4) decode model predictions to tagging sequence.
    """

    def __init__(self,
                 train_data: List[List[str]],
                 train_labels: List[List[str]],
                 min_count: int = 2,
                 use_char: bool = True,
                 use_bert: bool = False,
                 use_word: bool = False,
                 external_word_dict: Optional[List[str]] = None,
                 bert_vocab_file: Optional[str] = None,
                 char_embed_type: Optional[str] = None,
                 char_embed_dim: int = 300,
                 word_embed_type: Optional[str] = None,
                 word_embed_dim: int = 300,
                 max_len: Optional[int] = None,
                 padding_mode: str = 'post',
                 truncating_mode: str = 'post') -> None:
        """Build vocabulary, pre-trained embedding.

        Args:
            train_data: List of List of str. List of tokenized (in char level) texts for training,
                like ``[['我', '在', '上', '海', '上'， '学'], ...]``.
            train_labels: List of List of str. The labels of train_data, usually in BIO or BIOES
                format, like ``[['O', 'O', 'B-LOC', 'I-LOC', 'O', 'O'], ...]``.
            min_count: int. Token of which frequency is lower than min_count will be ignored when
                building vocabulary.
            use_char：Boolean. Whether to use character embedding as input.
            use_bert: Boolean. Whether to use bert embedding as input.
            use_word: Boolean. Whether to use word embedding as additional input.
            external_word_dict: Optional List of str, can be None. List of words, external word
                dictionary that will be used to loaded in jieba. It can be regarded as one kind
                of gazetter that contain a number of correct named-entities.
                Such as ``['南京市', '长江大桥']``. Only applied when use_word is True.
            bert_vocab_file: Optional str, can be None. Path to bert's vocabulary file.
            char_embed_type:  Optional str, can be None. The type of char embedding, can be a
                pre-trained embedding filename that used to load pre-trained embedding,
                or a embedding training method (one of {'word2vec', 'fasttext'}) that used to
                train character embedding with dataset. If None, do not apply anr pre-trained
                embedding, and use randomly initialized embedding instead.
            char_embed_dim: int. Dimensionality of char embedding.
            word_embed_type: str. Same as char_embed_type, only applied when use_word is True.
            word_embed_dim: int. Dimensionality of word embedding
            max_len: Optional int, can be None. Max length of one sequence. If None, we dynamically
                use the max length of each batch as max_len. However, max_len must be provided
                when using bert as input.
            padding_mode: str. 'pre' or 'post': pad either before or after each sequence, used when
                preparing feature input for ner model.
            truncating_mode: str. pre' or 'post': remove values from sequences larger than
                `maxlen`, either at the beginning or at the end of the sequences, used when
                preparing feature input for ner model.
        """
        super(NERPreprocessor, self).__init__(max_len, padding_mode, truncating_mode)

        self.train_data = train_data
        self.train_labels = train_labels
        self.min_count = min_count
        self.use_char = use_char
        self.use_bert = use_bert
        self.use_word = use_word
        self.external_word_dict = external_word_dict
        self.char_embed_type = char_embed_type
        self.word_embed_type = word_embed_type

        assert self.use_char or self.use_bert, "must use char or bert embedding as main input"
        special_token = 'bert' if self.use_bert else 'standard'

        # build char vocabulary and char embedding
        if self.use_char:
            self.char_vocab_count, self.char_vocab, self.id2char = \
                self.build_vocab(self.train_data, self.min_count, special_token)
            self.char_vocab_size = len(self.char_vocab)
            self.char_embeddings = self.build_embedding(char_embed_type, self.char_vocab,
                                                        self.train_data, char_embed_dim,
                                                        special_token)
            if self.char_embeddings is not None:
                self.char_embed_dim = self.char_embeddings.shape[1]
            else:
                self.char_embed_dim = char_embed_dim
        else:
            self.char_vocab_count, self.char_vocab, self.id2char = None, None, None
            self.char_vocab_size = -1
            self.char_embeddings = None
            self.char_embed_dim = -1

        # build bert vocabulary
        if self.use_bert:
            # lower case for non-chinese character
            self.bert_tokenizer = ChineseBertTokenizer(bert_vocab_file, do_lower_case=True)

        # build word vocabulary and word embedding
        if self.use_word:
            self.load_word_dict()

            untokenized_texts = [''.join(text) for text in self.train_data]
            word_corpus = self.build_corpus(untokenized_texts, cut_func=lambda x: jieba.lcut(x))

            self.word_vocab_count, self.word_vocab, self.id2word = \
                self.build_vocab(word_corpus, self.min_count, special_token)
            self.word_vocab_size = len(self.word_vocab)
            self.word_embeddings = self.build_embedding(word_embed_type, self.word_vocab,
                                                        word_corpus, word_embed_dim,
                                                        special_token)
            if self.word_embeddings is not None:
                self.word_embed_dim = self.word_embeddings.shape[1]
            else:
                self.word_embed_dim = word_embed_dim
        else:
            self.word_vocab_count, self.word_vocab, self.id2word = None, None, None
            self.word_vocab_size = -1
            self.word_embeddings = None
            self.word_embed_dim = -1

        # build label vocabulary
        self.label_vocab, self.id2label = self.build_label_vocab(self.train_labels)
        self.num_class = len(self.label_vocab)

        if self.use_bert and self.max_len is None:
            # max_len must be provided when use bert as input!
            # We will reset max_len from train_data when max_len is not provided.
            self.max_len = get_len_from_corpus(self.train_data)

            # make sure max_len is shorted than bert's max length (512)
            # since there are 2 more special token: <CLS> and <SEQ>, so add 2
            self.max_len = min(self.max_len + 2, 512)

    def load_word_dict(self):
        """Load external word dictionary in jieba"""
        if self.external_word_dict:
            for word in self.external_word_dict:
                jieba.add_word(word, freq=1000000)

    def build_label_vocab(self,
                          labels: List[List[str]]) -> Tuple[Dict[str, int], Dict[int, str]]:
        """Build label vocabulary.

        Args:
            labels: List of list of str, the label sequences, like
            ``[['O', 'O', 'B-LOC', 'I-LOC', 'O', 'O'], ...]``.

        Returns:
            Tuple of 2 dict

        """
        label_count = {}
        for sequence in labels:
            for label in sequence:
                label_count[label] = label_count.get(label, 0) + 1

        # sorted by frequency, so that the label with the highest frequency will be given
        # id of 0, which is the default id for unknown labels
        sorted_label_count = sorted(label_count.items(), key=lambda x: x[1], reverse=True)
        sorted_label_count = dict(sorted_label_count)

        label_vocab = {}
        for label in sorted_label_count:
            label_vocab[label] = len(label_vocab)

        id2label = dict((idx, label) for label, idx in label_vocab.items())

        logging.info('Build label vocabulary finished, '
                     'vocabulary size: {}'.format(len(label_vocab)))
        return label_vocab, id2label

    def prepare_input(self,
                      data: List[List[str]],
                      labels: Optional[List[List[str]]] = None) -> Tuple[np.ndarray, Any]:
        """Prepare input (features and labels) for NER model.
        Here we not only use character embeddings (or bert embeddings) as main input, but also
        support word embeddings and other hand-crafted features embeddings as additional input.

        Args:
            data: List of List of str. List of tokenized (in char level) texts for training,
                like ``[['我', '在', '上', '海', '上'， '学'], ...]``.
            labels: Optional List of List of str, can be None. The labels of train_data, usually in
            BIO or BIOES format, like ``[['O', 'O', 'B-LOC', 'I-LOC', 'O', 'O'], ...]``.

        Returns: Tuple:
            features: id matrix
            y: label id matrix only if labels is provided, otherwise None,

        """
        batch_char_ids, batch_bert_ids, batch_bert_seg_ids, batch_word_ids = [], [], [], []
        batch_label_ids = []
        for i, char_text in enumerate(data):
            if self.use_char:
                if self.use_bert:
                    text_for_char_input = [self.cls_token] + char_text + [self.seq_token]
                else:
                    text_for_char_input = char_text
                char_ids = [self.char_vocab.get(token, self.char_vocab[self.unk_token])
                            for token in text_for_char_input]
                batch_char_ids.append(char_ids)

            if self.use_bert:
                indices, segments = self.bert_tokenizer.encode(first_text=''.join(char_text),
                                                               max_length=self.max_len)
                batch_bert_ids.append(indices)
                batch_bert_seg_ids.append(segments)

            if self.use_word:
                word_text = jieba.lcut(''.join(char_text))
                word_ids = self.get_word_ids(word_text)
                batch_word_ids.append(word_ids)

            if labels is not None:
                if self.use_bert:
                    label_str = [self.cls_token] + labels[i] + [self.cls_token]
                else:
                    label_str = labels[i]
                label_ids = [self.label_vocab.get(l, self.get_unk_label_id()) for l in label_str]
                label_ids = tf.keras.utils.to_categorical(label_ids, self.num_class).astype(int)
                batch_label_ids.append(label_ids)

        features = []
        if self.use_char:
            features.append(self.pad_sequence(batch_char_ids))
        if self.use_bert:
            features.append(self.pad_sequence(batch_bert_ids))
            features.append(self.pad_sequence(batch_bert_seg_ids))
        if self.use_word:
            features.append(self.pad_sequence(batch_word_ids))

        if len(features) == 1:
            features = features[0]

        if not batch_label_ids:
            return features, None
        else:
            y = pad_sequences_2d(batch_label_ids, max_len_1=self.max_len, max_len_2=self.num_class,
                                 padding=self.padding_mode, truncating=self.truncating_mode)
            return features, y

    def get_word_ids(self, word_cut: List[str]) -> List[int]:
        """Given a word-level tokenized text, return the corresponding word ids in char-level
           sequence. We add the same word id to each character in the word.

        Args:
            word_cut: List of str, like ['我', '是'. '中国人']

        Returns: List of int, id sequence

        """
        word_ids = []
        for word in word_cut:
            for _ in word:
                word_ids.append(self.word_vocab.get(word, self.word_vocab[self.unk_token]))
        if self.use_bert:
            word_ids = [self.word_vocab[self.cls_token]] + word_ids + \
                       [self.word_vocab[self.seq_token]]
        return word_ids

    def label_decode(self,
                     pred_probs: np.ndarray,
                     lengths: Optional[List[int]] = None) -> List[List[str]]:
        """Decode model predictions to label strings

        Args:
            pred_probs: np.ndarray, shaped [num_samples, max_len, num_class], the ner model's
                predictions
            lengths: Optional List of int. Length of each sample;

        Returns：
            List of List of str, the tagging sequences of each sample.

        """
        pred_ids = np.argmax(pred_probs, axis=-1)
        pred_labels = [[self.id2label[label_id] for label_id in ids] for ids in pred_ids]
        if lengths is not None:
            pred_labels = [labels[:length] for labels, length in zip(pred_labels, lengths)]
        return pred_labels

    def get_unk_label_id(self):
        """return a default id for label that does not exist in the label vocab

        Returns: int

        """
        if 'O' in self.label_vocab:
            return self.label_vocab['O']
        elif 'o' in self.label_vocab:
            return self.label_vocab['o']
        else:
            return 0  # id of 0 is the label with the highest frequency

    def save(self, preprocessor_file: str):
        """Save preprocessor to disk

        Args:
            preprocessor_file: str, path to save preprocessor

        Returns:

        """
        pickle.dump(self, open(preprocessor_file, 'wb'))

    @classmethod
    def load(cls, preprocessor_file):
        """Load preprocessor from disk

        Args:
            preprocessor_file: str, path to load preprocessor.

        Returns:

        """
        p = pickle.load(open(preprocessor_file, 'rb'))
        p.load_word_dict()  # reload external word dict into jieba
        return p
