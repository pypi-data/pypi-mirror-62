# Get the required resources
<code> scp -r webis@webislab40.medien.uni-weimar.de:/home/weci2587/projects/args-topic-modeling/resources . </code>

# To run the ESA-script with all terms run:
## For normal ESA:
    
    ./esa-all-terms.py  --similarity cos
                        --matrix-path <path_to_resources>/resources/esa-plain/<debatepedia|strategic-intelligence|wikipedia>.mat
                        --model-path <path_to_resources>/resources/esa-w2v/GoogleNews-vectors-negative300.bin
                        --model-vocab <path_to_resources>/resources/esa-w2v/w2v-vocab.p
                        --input-path <path_to_input_file>
                        --output-path <path_to_output_file>
        
## For word2vec-ESA:
    
    ./esa-all-terms.py  --similarity max
                        --matrix-path <path_to_resources>/resources/esa-w2v/<debatepedia|strategic-intelligence|wikipedia>.mat
                        --model-path <path_to_resources>/resources/esa-w2v/GoogleNews-vectors-negative300.bin
                        --model-vocab <path_to_resources>/resources/esa-w2v/w2v-vocab.p
                        --input-path <path_to_input_file>
                        --output-path <path_to_output_file>
    
# To run the word2vec-ESA with reduced terms run:

    ./esa-top-n-terms.py    -n <number_of_terms> 
                            --corpus-path <path_to_resources>/resources/corpora/<debatepedia|strategic-intelligence|wikipedia>.csv
                            --model-path <path_to_resources>/resources/esa-w2v/GoogleNews-vectors-negative300.bin
                            --model-vocab <path_to_resources>/resources/esa-w2v/w2v-vocab.p
                            --input-path <path_to_input_file>
                            --output-path <path_to_output_file>
                            
The input document must be a csv file with "|" as the separator and must contain the column "document", which is used as the input text for the ESA.