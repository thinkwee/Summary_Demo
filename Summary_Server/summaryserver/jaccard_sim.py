def jacsim(list1, list2):
    unionlength = float(len(set(list1) | set(list2)))
    interlength = float(len(set(list1) & set(list2)))
    return float('%.3f' % (interlength / unionlength))
