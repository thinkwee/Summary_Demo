from __future__ import unicode_literals
from myapp import models
from django.shortcuts import render
from snownlp import SnowNLP
import astropy.constants.tests.test_pickle
import argparse
import online_infer
import pickle
import json
import math
from .metrics import get_all_metrics

# 固定加载参数
print("loading model......")

args_0 = pickle.load(open("./args_0", "rb"))
infer_model_0 = online_infer.infer_model(args_0)
print("model 0  loaded")

args_1 = pickle.load(open("./args_1", "rb"))
infer_model_1 = online_infer.infer_model(args_1)
print("model 1  loaded")


def show(request):
    if request.method == "POST":
        article_raw = request.POST.get("article", None)
        if article_raw:
            if " . " not in article_raw:
                article_raw = article_raw.replace(". ", " . ")
            article = article_raw.replace(" . ", "。")
            article_length = len(article.split("。"))
            if article_length <= 3:
                article = "。".join([article] * 5)[:700]
                article_raw = " . ".join([article_raw] * 5)[:700]
            print(article_length)
            print(article)
            print(article_raw)

            s = SnowNLP(article)
            extract_summary = s.summary(3)
            print("extract summarization finished")
            processed_article = " ".join(article_raw.split(" ")[:700])

            src_str, sentence_score_0, summary_0, token_score_0, align_0 = infer_model_0.infer(
                [processed_article])
            token_score_0 = token_score_0[1:]
            token_score_0 = [math.exp(ts) for ts in token_score_0]
            alignments_0 = []
            for t_score, align_single in zip(token_score_0, align_0):
                alignments_0.append(
                    [t_score, align_single[1], align_single[0]])
            metrics_0 = get_all_metrics(src_str, summary_0)

            src_str, sentence_score_1, summary_1, token_score_1, align_1 = infer_model_1.infer(
                [processed_article])
            token_score_1 = token_score_1[1:]
            token_score_1 = [math.exp(ts) for ts in token_score_1]

            alignments_1 = []
            for t_score, align_single in zip(token_score_1, align_1):
                alignments_1.append(
                    [t_score, align_single[1], align_single[0]])
            metrics_1 = get_all_metrics(src_str, summary_1)

    else:
        src_str = ""
        extract_summary = ["None", "None", "None"]
        summary_0 = ""
        sentence_score_0 = ""
        token_score_0 = [0, 0, 0, 0, 0, 0]
        align_0 = ""
        alignments_0 = []
        summary_1 = ""
        sentence_score_1 = ""
        token_score_1 = [0, 0, 0, 0, 0, 0]
        align_1 = ""
        alignments_1 = []
        metrics_0 = []
        metrics_1 = []

    return render(
        request, 'show.html', {
            "article": src_str,
            "extract_summary": extract_summary,
            "abstract_summary_0": summary_0,
            "sentence_score_0": sentence_score_0,
            "token_score_0": str(token_score_0),
            "align_0": str(align_0),
            "y_point_0": json.dumps(token_score_0),
            "x_point_0": json.dumps(summary_0.split(" ")),
            "alignments_0": json.dumps(alignments_0),
            "abstract_summary_1": summary_1,
            "sentence_score_1": sentence_score_1,
            "token_score_1": str(token_score_1),
            "align_1": str(align_1),
            "y_point_1": json.dumps(token_score_1),
            "x_point_1": json.dumps(summary_1.split(" ")),
            "alignments_1": json.dumps(alignments_1),
            "metrics_0": metrics_0,
            "metrics_1": metrics_1,
        })
