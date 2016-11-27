#! python2.7
# DigitRecog.py

import csv
from sklearn.neural_network import MLPClassifier

def div255(x):
    return x/255.

# create a NN
mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                    solver='sgd', verbose=10, tol=1e-4, random_state=1,
                    learning_rate_init=.1)

# open the csv file to read and write
with open('train.csv') as datasetFile, \
    open('test.csv') as testFile, open('sample_submission.csv', 'r') as outFile, \
    open('out_submission.csv', 'w') as realoutFile:
    dataset = csv.reader(datasetFile)
    y = []    # label set
    x = []    # training set
    
    # read train data from train.csv
    for row in dataset:
        if dataset.line_num == 1:
            continue

        y.append(int(row[0]))
        x.append(map(div255, map(int, row[1:])))

    print 'start training'
    mlp.fit(x, y)       # train the model
    print 'end training'
    
    realout = csv.writer(realoutFile, lineterminator='\n')
    out = csv.reader(outFile)
    test = csv.reader(testFile)
    testx = []
    for row in test:
        if test.line_num == 1:
            continue    
        testx.append(map(int, row))        
    # test the model
    testy = mlp.predict(testx)
    
    # output the result to out_submission.csv
    for row in out:
        if out.line_num == 1:
            realout.writerow(row)
            continue
        row[1] = testy[out.line_num-2]
        realout.writerow(row)
