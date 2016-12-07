# S E N T I E N C E

Original content generator


Webpage code in /web2py/ subdirectory.
[View live webpage here](https://DED8IRD.pythonanywhere.com/)


To try out NLP gen and image gen modules my or your own test data:


For NLP:

Generate an n-gram model

Requires: post_compilation (text of corpus you want to build model from) in same directory

Out: post_compilation.json (n-gram model)
```
python ngram_generator.py 
```
Generates single sentence to generate.out

Out: generated.out
```
python gen_test.py
```

For image generation:

Requires: /src/ subdirectory containing source images, /src/bkgd/ for background images, and /src/overlays/ and /src/backoverlays/ source image layers

Out: generated image (autoincremented int titles in the current directory
```
python image_generator.py
```

