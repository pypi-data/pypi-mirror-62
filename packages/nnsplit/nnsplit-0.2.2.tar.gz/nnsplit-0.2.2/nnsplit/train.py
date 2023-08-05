from pathlib import Path
import random
import re
import pickle
from xml.etree import ElementTree
from lxml.etree import iterparse
from tqdm.auto import tqdm
import numpy as np
import torch
from torch.nn import functional as F
from torch.utils import data
from sklearn import metrics
from fastai.train import Learner, DataBunch
from .utils import text_to_id
from .defaults import CUT_LENGTH
from .models import Network

REMOVE_DOT_CHANCE = 0.5
LOWERCASE_START_CHANCE = 0.5
MIN_LENGTH = 300
MAX_LENGTH = 5000
N_CUTS = 2


def label_paragraph(tokenized_paragraph):
    full_text = ""
    labels = []

    for sentence in tokenized_paragraph:
        for i, token in enumerate(sentence):
            text = token.text
            whitespace = token.whitespace

            # add more whitespace with a small chance so that multiple whitespace is split
            # correctly too
            while True:
                if random.random() < 0.8:
                    break

                whitespace += " "

            text_to_append = text + whitespace

            if (
                text == "."
                and i == len(sentence) - 1
                and random.random() < REMOVE_DOT_CHANCE
            ):
                text_to_append = whitespace
                if len(text_to_append) > 0 and len(labels) > 1:
                    labels[-1][0] = 0.0

            if i == 0 and random.random() < LOWERCASE_START_CHANCE:
                text_to_append = text.lower() + whitespace

            for _ in range(len(text_to_append)):
                labels.append([0.0, 0.0])

            if len(labels) > 0:
                labels[-1][0] = 1.0

            full_text += text_to_append

        labels[-1][1] = 1.0

    return full_text, labels


def paragraph_to_text_and_labels(paragraph, n_cuts, cut_length):
    try:
        p_text, p_labels = label_paragraph(paragraph)
    except IndexError:
        print("Faulty paragraph:")
        print(paragraph)
        return [], []

    assert len(p_text) == len(p_labels)

    inputs = [[] for _ in range(n_cuts)]
    labels = [[] for _ in range(n_cuts)]

    for j in range(n_cuts):
        start = random.randint(0, len(p_text) + cut_length) - cut_length

        for k in range(cut_length):
            if start + k < 0 or start + k >= len(p_text):
                inputs[j].append(0)
                labels[j].append([0.0, 0.0])
            else:
                inputs[j].append(text_to_id(p_text[start + k]))
                labels[j].append(p_labels[start + k])

    return inputs, labels


def xml_to_paragraphs(
    corpus,
    max_n_paragraphs,
    min_length=MIN_LENGTH,
    max_length=MAX_LENGTH,
    store_path=None,
):
    def fast_iter(context):
        for event, elem in context:
            text = ElementTree.tostring(elem, encoding="utf8").decode("utf-8")
            text = re.sub(r"(<h>(.*?)<\/h>)", "\n", text)
            text = re.sub(r"<.*?>", "", text)
            text = text.strip()
            yield text

            # It's safe to call clear() here because no descendants will be
            # accessed
            elem.clear()
            # Also eliminate now-empty references from the root node to elem
            for ancestor in elem.xpath("ancestor-or-self::*"):
                while ancestor.getprevious() is not None:
                    parent = ancestor.getparent()

                    if parent is not None:
                        del parent[0]
                    else:
                        break

    i = 0
    paragraphs = []
    bar = tqdm(total=max_n_paragraphs)

    for p in fast_iter(iterparse(str(corpus), tag="p")):
        if not (min_length <= len(p) <= max_length):
            continue

        paragraphs.append(p)
        i += 1
        bar.update(1)

        if i >= max_n_paragraphs:
            break

    if store_path is not None:
        store_path = Path(store_path)
        store_path.parents[0].mkdir(exist_ok=True, parents=True)
        torch.save(paragraphs, store_path)

    return paragraphs


def prepare_tokenized_paragraphs(
    tokenized_paragraph_path,
    data_directory=None,
    subsample=None,
    remove_dot_chance=REMOVE_DOT_CHANCE,
    lowercase_start_chance=LOWERCASE_START_CHANCE,
    min_length=MIN_LENGTH,
    max_length=MAX_LENGTH,
    n_cuts=N_CUTS,
    cut_length=CUT_LENGTH,
):
    if data_directory is not None:
        data_directory = Path(data_directory)
        data_directory.mkdir(exist_ok=True, parents=True)

    all_sentences = []
    all_labels = []

    bar = tqdm()
    i = 0

    with open(tokenized_paragraph_path, "rb") as f:
        while True:
            try:
                paragraph = pickle.load(f)
                bar.update(1)

                i += 1

                if subsample is not None and i >= subsample:
                    break
            except EOFError:
                break

            text, labels = paragraph_to_text_and_labels(paragraph, n_cuts, cut_length)

            all_sentences.append(torch.tensor(text, dtype=torch.uint8))
            all_labels.append(torch.tensor(labels, dtype=torch.bool))

    all_sentences = torch.cat(all_sentences, 0)
    all_labels = torch.cat(all_labels, 0)

    if data_directory is not None:
        torch.save(all_sentences, data_directory / "all_sentences.pt")
        torch.save(all_labels, data_directory / "all_labels.pt")

    return all_sentences, all_labels


def loss(inputs, targets):
    weight = torch.tensor([1, 20]).view((1, 1, 2)).to(targets.device)
    return F.binary_cross_entropy_with_logits(inputs, targets.float(), weight=weight)


def train(
    sentences_train,
    labels_train,
    sentences_valid,
    labels_valid,
    batch_size=128,
    n_epochs=10,
):
    train_dataset = data.TensorDataset(sentences_train, labels_train)
    valid_dataset = data.TensorDataset(sentences_valid, labels_valid)

    model = Network()

    train_loader = data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, pin_memory=False
    )
    valid_loader = data.DataLoader(
        valid_dataset, batch_size=batch_size, shuffle=False, pin_memory=False
    )

    databunch = DataBunch(train_dl=train_loader, valid_dl=valid_loader)
    learn = Learner(databunch, model, loss_func=loss)

    if torch.cuda.is_available():
        learn = learn.to_fp16()

    learn.fit_one_cycle(n_epochs)

    return learn.model


def evaluate(model, sentences_valid, labels_valid, threshold=0.5, batch_size=1024):
    assert len(sentences_valid) == len(labels_valid)

    preds = np.zeros(labels_valid.shape)

    for i in tqdm(range((len(sentences_valid) // batch_size) + 1)):
        idx = slice(i * batch_size, (i + 1) * batch_size)

        if next(model.parameters()).is_cuda:
            out = model(sentences_valid[idx].cuda())
        else:
            out = model(sentences_valid[idx])

        preds[idx] = out.detach().cpu().numpy()

    preds = preds.reshape((-1, 2)) > threshold
    labels_valid = labels_valid.cpu().numpy().reshape((-1, 2))

    for (i, name) in zip([0, 1], ["Tokenize", "Sentencize"]):
        print(f"Target: {name} \n")

        for (metric, name) in [
            [metrics.f1_score, "F1"],
            [metrics.precision_score, "Precision"],
            [metrics.recall_score, "Recall"],
        ]:
            print(f"{name}:", metric(preds[:, i], labels_valid[:, i]))

        print("\n\n")
