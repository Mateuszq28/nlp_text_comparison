def empty_preprocess(text):
    return text

def double_empty_lines(text):
    split = text.split("\n")
    text = "\n\n".join(split)
    return text

def preprocess1(text):
    return preprocess2(text)

def preprocess2(text):
    split = text.split("\n")
    split = split[:-5]
    split = split[5:]
    new_text = "\n\n".join(split)
    return new_text

def preprocess3(text):
    split = text.split("\n")
    split = split[:-2]
    split = split[1:]
    text = " ".join(split)

    text = text.replace("\t", "")
    text = text.replace("    ", "")
    text = text.replace("\",", "")
    text = text.replace("\"", "")

    return text

def preprocess4(text):
    text = text.replace(". ", ".\n\n")
    return text

def preprocess5(text):
    return text

def preprocess6(text):
    return double_empty_lines(text)

def preprocess7(text):
    # text = text.replace("\"", "\n")
    text = text.replace(" \" ].", "")
    text = text.replace("[ \" ", "")
    text = text.replace(" \" ", " ")
    text = text.replace(". ", ".\n\n")
    text = text.replace("\"", "")
    text = text.replace("\n,\n", "")
    text = text.replace("\n\n\n", "\n\n")

    return text

def preprocess8(text):
    text = text.replace(". ", ".\n\n")
    return text

def preprocess9(text):
    return empty_preprocess(text)