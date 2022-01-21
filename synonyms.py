
import math
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    top_sum = 0
    bot_vec_1 = 0
    bot_vec_2 = 0
    for key_vec_1 in vec1:
        bot_vec_1 += vec1[key_vec_1] * vec1[key_vec_1]
        if key_vec_1 in vec2:
            top_sum += vec1[key_vec_1] * vec2[key_vec_1]
    for key_vec_2 in vec2:
        bot_vec_2 += vec2[key_vec_2] * vec2[key_vec_2]
    if bot_vec_2 == 0 or bot_vec_1 == 0:
        return 0
    return (top_sum/(math.sqrt((bot_vec_1)*(bot_vec_2))))


def build_semantic_descriptors(sentences):
    dict = {}
    for sen in sentences:
        sent = order_list(sen)
        for word in sent:
            if word not in dict:
                dict[word] = {}
            for word_2 in sent:
                if word_2 in dict[word]:
                    dict[word][word_2] += 1
                else:
                    dict[word][word_2] = 1
            del dict[word][word]
    return dict

def build_semantic_descriptors_from_files(filenames):
    sens = []
    for i in range (len(filenames)):
        file = open(filenames[i], "r", encoding="latin1")
        file = file.read().lower()
        file = file.replace("\n"," ").strip().replace("--"," ").replace("-"," ") .replace(","," ").replace(";"," ").replace(":"," ").replace("!",".").replace("?",".").split(".")
        for i in range (len(file)):
            file[i] = file[i].split()
        sens += file
    return build_semantic_descriptors(sens)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    list_of_results = []
    pos_pt = [0,-100000000]
    if word not in semantic_descriptors:
        return choices[0]
    for i in choices:
        if i in semantic_descriptors:
            list_of_results.append(similarity_fn(semantic_descriptors[word],semantic_descriptors[i]))
        else:
            list_of_results.append(-1)
    for i in range (len(list_of_results)):
        if list_of_results[i] > pos_pt[1]:
            pos_pt = (i,list_of_results[i])
    return choices[pos_pt[0]]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    tests = open(filename,"r",encoding = "latin1")
    tests = tests.read().lower().split("\n")
    new_tests = []
    results_real = []
    results_guess = []
    total_vs_count = [0,0]
    for i in tests:
        if len(i) > 5:
            t = i.split(" ")
            new_tests.append(t)
    for i in new_tests:
        results_real.append(i[1])
        results_guess.append(most_similar_word(i[0], i[2:], semantic_descriptors,similarity_fn))
    for i in range (len(results_real)):
        total_vs_count[0] += 1
        if results_real[i] == results_guess[i]:
            total_vs_count[1] += 1
    percent = (total_vs_count[1]/total_vs_count[0])*100
    percent = round(percent, 1)
    return percent


### Helper Functions

def order_list(list):
    list1 = []
    for i in list:
        if i not in list1:
            list1.append(i)
    return list1

if __name__ == "__main__":
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
