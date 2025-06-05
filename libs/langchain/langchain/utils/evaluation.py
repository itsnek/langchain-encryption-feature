from typing import Sequence, Hashable

def _confusion_counts(
    y_true: Sequence[Hashable], 
    y_pred: Sequence[Hashable], 
    positive: Hashable = None
):
    """
    Return TP, FP, FN, TN counts for *binary* tasks.
    If `positive` is None, the first label in y_true is treated as the positive class.
    """
    if positive is None:
        positive = next(iter(set(y_true)))
    tp = fp = fn = tn = 0
    for t, p in zip(y_true, y_pred):
        if p == positive:
            if t == positive:
                tp += 1
            else:
                fp += 1
        else:
            if t == positive:
                fn += 1
            else:
                tn += 1
    return tp, fp, fn, tn


def accuracy_score(y_true: Sequence, y_pred: Sequence) -> float:
    """
    Accuracy = (TP + TN) / total
    """
    correct = sum(t == p for t, p in zip(y_true, y_pred))
    return correct / len(y_true) if y_true else 0.0

def precision_score(y_true: Sequence, y_pred: Sequence) -> float:
    """
    Precision = TP / (TP + FP)
    """
    tp, fp, *_ = _confusion_counts(y_true, y_pred)
    return tp / (tp + fp) if tp + fp else 0.0

def recall_score(y_true: Sequence, y_pred: Sequence):
    """
    Recall = TP / (TP + FN)
    """
    tp, _, fn, _ = _confusion_counts(y_true, y_pred)
    return tp / (tp + fn) if tp + fn else 0.0
