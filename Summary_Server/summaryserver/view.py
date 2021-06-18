from django.shortcuts import render
from .check import get_results
from .rouge_eval import get_rouge
import shutil
import os
import numpy as np
from .jaccard_sim import jacsim


def get_summary_list(s):
    sum_list = []
    for sentence in s.split(" ."):
        if len(sentence) > 2:
            temp = {
                "text": sentence + " . ",
                "max_idx": 0,
                "max_ratio": 0.0,
                "bp": 0
            }
            sum_list.append(temp)
    return sum_list


def get_src_list(s):
    src_list = []
    for sentence in s.split(' .'):
        temp = {"text": sentence + " . ", "bp_a": 0, "bp_b": 0}
        src_list.append(temp)
    return src_list


def tag_most_relevant(src_list, summary_list):
    for idx, src in enumerate(src_list):
        for summary in summary_list:
            ratio = jacsim(summary['text'].split(' '), src['text'].split(' '))
            if ratio > summary['max_ratio']:
                summary['max_ratio'] = ratio
                summary['max_idx'] = idx
    return summary_list


def show_result(request):
    id, s_fairseq, s_other, s_system, s_src = get_results()
    print("yes")

    shutil.rmtree("./summaryserver/models_A")
    shutil.rmtree("./summaryserver/models_B")
    shutil.rmtree("./summaryserver/systems")
    os.mkdir("./summaryserver/models_A")
    os.mkdir("./summaryserver/models_B")
    os.mkdir("./summaryserver/systems")

    with open("./summaryserver/models_A/model." + str(id) + ".txt", "w") as f:
        f.writelines(s_fairseq.replace("UNK", ""))
    with open("./summaryserver/models_B/model." + str(id) + ".txt", "w") as f:
        f.writelines(s_other.replace("UNK", ""))
    with open("./summaryserver/systems/system." + str(id) + ".txt", "w") as f:
        f.writelines(s_system.replace("UNK", ""))

    print("yes")

    rouge_result_a = get_rouge("models_A")
    rouge_result_b = get_rouge("models_B")

    context = {}
    context['system'] = s_system
    context['id'] = id
    context['r1fa'] = rouge_result_a["rouge_1_f_score"]
    context['r2fa'] = rouge_result_a["rouge_2_f_score"]
    context['rlfa'] = rouge_result_a["rouge_l_f_score"]
    context['r1fb'] = rouge_result_b["rouge_1_f_score"]
    context['r2fb'] = rouge_result_b["rouge_2_f_score"]
    context['rlfb'] = rouge_result_b["rouge_l_f_score"]

    fairseq_list = get_summary_list(s_fairseq)
    lw_list = get_summary_list(s_other)
    src_list = get_src_list(s_src)

    fairseq_list = tag_most_relevant(src_list, fairseq_list)
    lw_list = tag_most_relevant(src_list, lw_list)

    for idx, summary in enumerate(fairseq_list):
        summary["bp"] = idx + 1
        max_id = summary['max_idx']
        if src_list[max_id]['bp_a'] != 0:
            summary["bp"] = src_list[max_id]['bp_a']
        else:
            src_list[max_id]['bp_a'] = idx + 1

    for idx, summary in enumerate(lw_list):
        summary["bp"] = idx + 1
        max_id = summary['max_idx']
        if src_list[max_id]['bp_b'] != 0:
            summary["bp"] = src_list[max_id]['bp_b']
        else:
            src_list[max_id]['bp_b'] = idx + 1

    context['src'] = src_list
    context['model_lw'] = lw_list
    context['model_fairseq'] = fairseq_list

    max_ratio_a = 0
    for summary in fairseq_list:
        if summary['max_ratio'] > max_ratio_a:
            max_ratio_a = summary['max_ratio']

    max_ratio_b = 0
    for summary in lw_list:
        if summary['max_ratio'] > max_ratio_b:
            max_ratio_b = summary['max_ratio']

    with open("./record.txt", "a") as f:
        f.write(
            str(max_ratio_a) + " " + str(max_ratio_b) + " " +
            str(context['r1fa']) + " " + str(context['r1fb']) + "\n")

    return render(request, 'result.html', context)
