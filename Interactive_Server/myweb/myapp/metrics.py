def get_bigram(s):
    bigram_list = []
    str_list = s.split(" ")
    for i in range(len(str_list) - 1):
        bigram_list.append(str_list[i] + '@@' + str_list[i + 1])
    return bigram_list


def calc_novel(src, hypo):

    unigram_novel = 0.0
    bigram_novel = 0.0
    count = 0

    unigram_src = set(src.split(" "))
    unigram_hypo = hypo.split(" ")
    bigram_src = set(get_bigram(src))
    bigram_hypo = get_bigram(hypo)
    l_bi = len(unigram_hypo) - 1
    if l_bi == 0:
        print(hypo)
    l_uni = 0
    count_unigram = 0
    count_bigram = 0
    for unigram in unigram_hypo:
        if unigram not in {".", ",", "?", "!", "\n", "..."}:
            l_uni += 1
            if unigram not in unigram_src:
                count_unigram += 1
    for bigram in bigram_hypo:
        if bigram not in bigram_src:
            count_bigram += 1

    unigram_novel += count_unigram / l_uni
    bigram_novel += count_bigram / l_bi

    return unigram_novel, bigram_novel


def jacsim(str1, str2):
    list1 = str1.split(" ")
    list2 = str2.split(" ")
    unionlength = float(len(set(list1) | set(list2)))
    interlength = float(len(set(list1) & set(list2)))
    return float('%.3f' % (interlength / unionlength))


def find_oracle(article, summary_sentence):
    doc_sentences = article.split(" . ")[:-1]
    jacsim_list = [
        jacsim(sentence, summary_sentence) for sentence in doc_sentences
    ]
    sorted_sentences = [
        item[1]
        for item in sorted(zip(jacsim_list, doc_sentences), reverse=True)
    ]
    if len(sorted_sentences) == 0:
        return "None"
    else:
        return sorted_sentences[0]


def check_jaccard(src, hypo):
    min_js = 1.1
    js = 0.0
    count = 0
    ratio = 0
    max_js = 0.0
    for hypo_i in hypo.split(" . "):
        tmp = jacsim(hypo_i, find_oracle(src, hypo_i))
        min_js = min(tmp, min_js)
        max_js = max(tmp, max_js)
        js += tmp
        count += 1
        covered = 0
    js /= count

    return js, min_js, max_js


def get_all_metrics(src, hypo):
    unigram_novel, bigram_novel = calc_novel(src, hypo)
    js, min_js, max_js = check_jaccard(src, hypo)
    # return [unigram_novel, bigram_novel, js, covered]
    return [unigram_novel, bigram_novel, 1 - js, 1 - min_js, 1 - max_js]
