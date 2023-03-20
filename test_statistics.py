def split_lines(line_list, separator, add_separator_end_line=False, add_separator_new_line=False):
    new_page_list = []
    for i in range(len(line_list)):
        one_line_list = line_list[i].split(separator)
        for one_line in one_line_list:
            if add_separator_end_line:
                new_page_list.append(one_line + separator)
            else:
                new_page_list.append(one_line)
            if add_separator_new_line:
                new_page_list.append(separator)
        if add_separator_new_line:
            new_page_list = new_page_list[:-1]
        if add_separator_end_line:
            new_page_list[-1] = new_page_list[-1][:-(len(separator))]
    return new_page_list


def trim_words(page):
    page.replace("\n\n", "\n")
    page = page.lower()

    page_list = page.split("\n")
    page_list = page_list[5:]
    page_list = page_list[:-5]
    page_list = [" ".join(page_list)]

    new_page_list = split_lines(page_list, ". ")
    new_page_list = split_lines(new_page_list, ", ")
    new_page_list = split_lines(new_page_list, "; ")
    new_page_list = split_lines(new_page_list, ": ")
    new_page_list = split_lines(new_page_list, ",")
    new_page_list = split_lines(new_page_list, ".")
    new_page_list = split_lines(new_page_list, ";")
    new_page_list = split_lines(new_page_list, ":")
    new_page_list = split_lines(new_page_list, " ")

    return new_page_list


def set_from_text(text):
    new_page_list = trim_words(text)
    page_set = set(new_page_list)
    return page_set


def set_words_from_file(filename):
    with open(filename, 'r') as f:
        page = f.read()
    return set_from_text(page)


def stat_dict(base_text, test_text, num_precision=2):
    set_base = set_from_text(base_text)
    set_test = set_from_text(test_text)

    correct_in_test_set = set_test.intersection(set_base)
    num_words_model = len(set_test)
    num_words_base_text = len(set_base)
    num_words_correct_set = len(correct_in_test_set)

    recall = num_words_correct_set / num_words_base_text
    precision = num_words_correct_set / num_words_model
    f1_score = 2 * precision * recall / (precision + recall)

    recall2 = round(recall*100, num_precision)
    precision2 = round(precision*100, num_precision)
    f1_score2 = round(f1_score*100, num_precision)

    d = {
        "f1_score": f1_score2,
        "kompletność": recall2,
        "precyzja": precision2
    }

    return d