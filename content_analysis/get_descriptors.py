import pickle
import spacy
from nltk.tokenize import sent_tokenize

nlp = spacy.load('en_core_web_sm')



def check_policy_names(sent, policy):
    present = False
    for pol in policy:
        if pol in sent:
            present = True
    return present

def update_descriptor(sentences, common_nouns_policy, policy):
    res = []
    j = 0
    present = False
    for sentence in sentences:
        doc = nlp(sentence)
        present = check_policy_names(sentence, policy)
        for token in doc:
            j += 1
            word = token.text.lower()
            target = token.head.text.lower()
            if token.pos_ != 'PROPN' and \
                    token.pos_ != 'NOUN' and token.pos_ != 'PRON': continue
            if present or (target in common_nouns_policy):
                if token.dep_ == 'nsubj' and (token.head.pos_ == 'VERB' or token.head.pos_ == 'ADJ'): 
                    res.append((str(j), word, present, target, token.head.pos_, token.dep_))
                if token.dep_ == 'nsubjpass' and token.head.pos_ == 'VERB': 
                    res.append((str(j), word, present, target, token.head.pos_, token.dep_))
                if (token.dep_ == 'obj' or token.dep_ == 'dobj') and token.head.pos_ == 'VERB': 
                    res.append((str(j), word, present, target, token.head.pos_, token.dep_))
    return res

def main():
    f = open('data/CommonNounPol.pickle', 'rb')
    common_nouns_policy = pickle.load(f)
    f.close()

    f = open('data/PolicySchemes.pickle', 'rb')
    policy = pickle.load(f)
    f.close()

    f = open("data/UpdNewsText", "rb")
    articles = pickle.load(f)
    f.close()
    descriptor_words = {}
    for key, val in articles.items():
        text = val['Text']
        descriptor_words[key] = []
        sentences = sent_tokenize(text)
        desc = update_descriptor(sentences, common_nouns_policy, policy)
        descriptor_words[key].append(desc)
    
    f = open('output/Descriptors.pickle', 'wb')
    pickle.dump(descriptor_words, f)
    f.close()

if __name__ == '__main__':
    main()