import time, json
from generator import sentGenerator 

if __name__ == '__main__':

    start_time = time.time()
    print ('LOADING JSON...')
    with open('post_compilation.json', 'r') as post_comp:
	    ngrams = json.load(post_comp)
    print ('LOADED ' + str(time.time()-start_time) + ' sec')    
    with open('generated.out', 'a') as gen_out:
	    gen = sentGenerator(ngrams)
	    gen_out.write(gen().encode('utf-8')+'\n')
	    print ('finish gen at ' + str(time.time()-start_time))

