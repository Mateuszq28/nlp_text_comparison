import os
from test_statistics import stat_dict
from test_jiwer import jiwer_dict
import shutil
import preprocess_catalog


def result_table_string(result_table, testname, sortkey, col_space):
    text = "TEST: " + testname + "\n"
    newlist = sorted(result_table, key=lambda d: d[sortkey])

    # first line
    line = newlist[0]
    col_num = len(line)
    block = "{:<" + str(col_space) + "}"
    line_text = ""

    for i in range(col_num):
        element = list(line.keys())[i]
        line_text += block.format(element) + " "
    line_text = line_text[:-1]
    text += line_text + "\n"


    for line in newlist:
        col_num = len(line)
        block = "{:<" + str(col_space) + "}"
        line_text = ""

        for i in range(col_num):
            element = list(line.values())[i]
            line_text += block.format(element) + " "
        line_text = line_text[:-1]
        text += line_text + "\n"
    return text


def preprocess_from_testname(testname):
    d = {
        "test_1_eng_whisper_greed_transcript_vs_basetext": preprocess_catalog.preprocess1,
        "test_2_eng_whisper_beam_transcript_vs_basetext": preprocess_catalog.preprocess2,
        "test_3_eng_vosk_transcript_vs_basetext": preprocess_catalog.preprocess3,
        "test_4_eng_ginger_on_vosk_vs_basetext": preprocess_catalog.preprocess4,
        "test_5_eng_ginger_on_basetext_vs_basetext": preprocess_catalog.preprocess5,
        "test_6_eng_ginger_on_whisper_base_greedy_vs_basetext": preprocess_catalog.preprocess6,
        "test_7_eng_vosk_text2punc_raw_vs_basetext": preprocess_catalog.preprocess7,
        "test_8_eng_vosk_text2punc_vs_basetext": preprocess_catalog.preprocess8,
        "test_9_grammar_check_vs_basetext": preprocess_catalog.preprocess9
    }
    return d[testname]
    

def prepare_test_texts(tests_to_prepare_dir, test_dir, basetext_filename):
    test_listdir = os.listdir(test_dir)
    test_to_prepare_listdir = os.listdir(tests_to_prepare_dir)

    for t in test_to_prepare_listdir:
        if t not in test_listdir:
            os.mkdir(os.path.join(test_dir, t))

        file_list = os.listdir(os.path.join(tests_to_prepare_dir, t))
        preprocess_filename = "preprocess.py"
        if preprocess_filename in file_list:
            file_list.remove(preprocess_filename)
        if basetext_filename in file_list:
            file_list.remove(basetext_filename)

        # copy base text
        shutil.copyfile(os.path.join(tests_to_prepare_dir,t,basetext_filename), os.path.join(test_dir,t,basetext_filename))

        preprocess = preprocess_from_testname(t)

        for f in file_list:
            path = os.path.join(tests_to_prepare_dir,t,f)
            with open(path, "r") as file:
                text2correct = file.read()
            corrected = preprocess(text2correct)

            path = os.path.join(test_dir,t,f)
            with open(path, "w") as file:
                file.write(corrected)
     

def do_tests():
    test_dir = "tests"
    tests_to_prepare_dir = "tests_not_prepared"
    basetext_filename = "tekst_odniesienia-10min.txt"

    prepare_test_texts(tests_to_prepare_dir, test_dir, basetext_filename)

    test_listdir = os.listdir(test_dir)


    # don't do old tests
    drop_tests = []
    for d in drop_tests:
            if d in test_listdir:
                test_listdir.remove(d)
                

    all_tests_table = []
    common_result_text = ""
    for test in test_listdir:
        tests_file_path = os.path.join(test_dir, test)
        basetext_file_path = os.path.join(test_dir, test, basetext_filename)
        with open(basetext_file_path, "r") as f:
                basetext_text = f.read()

        num_precision = 2
        result_table = []

        file_list_to_process = os.listdir(tests_file_path)
        dropname = "0_test_result.txt"
        if dropname in file_list_to_process:
            file_list_to_process.remove(dropname)
        for file in file_list_to_process:
            t_file_path = os.path.join(tests_file_path, file)
            with open(t_file_path, "r") as f:
                test_text = f.read()

            test_result_jiwer = jiwer_dict(basetext_text, test_text, num_precision)
            test_result_stat = stat_dict(basetext_text, test_text, num_precision)

            test_results_dict = test_result_jiwer
            test_results_dict |= test_result_stat
            test_results_dict |= {"filename": file}

            result_table.append(test_results_dict)
            all_tests_table.append(test_results_dict)

        # one test result
        # colspace = num_precision*2+2
        colspace = 10
        result_string = result_table_string(result_table, testname=test, sortkey="wil", col_space=colspace)
        print(result_string)
        print()
        result_filename = os.path.join(test_dir, test, "0_test_result.txt")
        with open(result_filename, "w") as f:
            f.write(result_string)
        common_result_text += result_string + "\n\n"
        result_table.clear()
    
    # all tests results
    result_string = result_table_string(all_tests_table, testname="ALL TESTS TOGETHER", sortkey="wil", col_space=colspace)
    print(result_string)
    print()
    result_filename = "0_all_test_result.txt"
    common_result_text += result_string + "\n\n"
    with open(result_filename, "w") as f:
        f.write(common_result_text)

    
do_tests()