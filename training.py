import csv
import pickle

result_template = {"alert": 0, "not-alert": 0}
likelihood_table = {"*": {"alert": 0, "not-alert": 0}} # initialize with 'all'
data_count = 0

with open('trained_model/trained_model.pk1', 'rb') as f:
    likelihood_table = pickle.load(f)
with open('trained_model/data_count.pk1', 'rb') as f:
    data_count = pickle.load(f)

def train():
    global data_count
    global likelihood_table

    likelihood_table = {"*": {"alert": 0, "not-alert": 0}} # initialize with 'all'
    data_count = 0
    with open('training_data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)

        for row in list(reader):
            title = row[0]
            result = row[-1]

            stripped_title = "".join([c if (c.isalnum() or c==" ") else "" for c in title]).lower().split()
            for word in stripped_title:
                if word not in likelihood_table:
                    likelihood_table[word] = {"alert": 0, "not-alert": 0}

                likelihood_table[word][result] += 1
                likelihood_table["*"][result] += 1
                data_count += 1
    with open('trained_model/trained_model.pk1', 'wb') as f:
        pickle.dump(likelihood_table, f, pickle.HIGHEST_PROTOCOL)
    with open('trained_model/data_count.pk1', 'wb') as f:
        pickle.dump(data_count, f, pickle.HIGHEST_PROTOCOL)
    print("Finished training!")

def get_score(sentence):
    global data_count
    global likelihood_table
    score_alert = 1
    score_not = 1
    stripped_sentence = stripped_title = "".join([c if (c.isalnum() or c==" ") else "" for c in sentence]).lower().split()

    for word in stripped_sentence:
        if word in likelihood_table:
            p_alert_word = likelihood_table[word]["alert"]/float(likelihood_table["*"]["alert"])
            p_word = (likelihood_table[word]["alert"]+likelihood_table[word]["not-alert"])/float(data_count)
            p_alert = likelihood_table["*"]["alert"]/float(data_count)

            p_not_word = likelihood_table[word]["not-alert"]/float(likelihood_table["*"]["not-alert"])
            p_not = likelihood_table["*"]["not-alert"]/float(data_count)

            p_word_alert = p_alert_word * p_word/p_alert if p_alert != 0 else 9000000

            p_word_not = p_not_word * p_word/p_not if p_not != 0 else 9000000

            score_alert *= p_word_alert
            score_not *= p_word_not
    if score_alert > score_not:
        return 3.5
    else:
        return -2

if __name__ == "__main__":
    train()
