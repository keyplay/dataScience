#! python3.6

import pandas as pd    
from bs4 import BeautifulSoup 
import re
from nltk.corpus import stopwords 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def review_to_words(raw_review):
    # Function to convert a raw review to a string of words
    
    review_text = BeautifulSoup(raw_review).get_text()        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    words = letters_only.lower().split()                             
    stops = set(stopwords.words("english"))                  
    meaningful_words = [w for w in words if not w in stops]    # Remove stop words
    
    return(" ".join( meaningful_words )) 

    
train = pd.read_csv("./labeledTrainData.tsv", header=0, delimiter="\t", quoting=3)
                    

print("Cleaning and parsing the training set movie reviews...\n")
num_reviews = len(train["review"])
clean_train_reviews = []
for i in range(num_reviews):
    # If the index is evenly divisible by 1000, print a message
    if((i+1)%1000 == 0):
        print("Review %d of %d\n" % (i+1, num_reviews))                                                                  
    clean_train_reviews.append(review_to_words(train["review"][i]))
    
print("Creating the bag of words...\n")

 
vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000) 
train_data_features = vectorizer.fit_transform(clean_train_reviews)
train_data_features = train_data_features.toarray()

print(train_data_features.shape)
print("Training the random forest...")


# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100) 

# Fit the forest to the training set, using the bag of words as features and the sentiment labels as the response variable
forest = forest.fit(train_data_features, train["sentiment"])


test = pd.read_csv("./testData.tsv", header=0, delimiter="\t", quoting=3)

print(test.shape)

num_reviews = len(test["review"])
clean_test_reviews = [] 

print("Cleaning and parsing the test set movie reviews...\n")
for i in range(num_reviews):
    if((i+1) % 1000 == 0):
        print("Review %d of %d\n" % (i+1, num_reviews))
    clean_review = review_to_words(test["review"][i])
    clean_test_reviews.append(clean_review)
    
# Get a bag of words for the test set, and convert to a numpy array
test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

# Use the random forest to make sentiment label predictions
result = forest.predict(test_data_features)

# Copy the results to a pandas dataframe with an "id" column and a "sentiment" column
output = pd.DataFrame(data={"id":test["id"], "sentiment":result})
output.to_csv("result.csv", index=False, quoting=3)
