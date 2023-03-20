from jiwer import wer, mer, wip, wil, cer


def call_func(func, basetext_text, test_text, num_precision):
    result = func(basetext_text, test_text)
    return round(result, num_precision)


def jiwer_dict(basetext_text, test_text, num_precision):
    result = dict()
    result["wer"] = call_func(wer, basetext_text, test_text, num_precision)
    result["mer"] = call_func(mer, basetext_text, test_text, num_precision)
    result["wip"] = call_func(wip, basetext_text, test_text, num_precision)
    result["wil"] = call_func(wil, basetext_text, test_text, num_precision)
    result["cer"] = call_func(cer, basetext_text, test_text, num_precision)
    return result