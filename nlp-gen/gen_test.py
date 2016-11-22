import pickle
from generator import sentGenerator 

if __name__ == '__main__':
    ngrams = pickle.load(open('post_compilation.txt.pickle', 'rb'))
    gen_out = open('generated.out', 'a')
    gen = sentGenerator(ngrams)
    print(gen(), file=gen_out)

