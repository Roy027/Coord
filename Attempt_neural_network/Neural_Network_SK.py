# https://stackabuse.com/introduction-to-neural-networks-with-scikit-learn/
# https://scikit-learn.org/stable/modules/neural_networks_supervised.html 

from sklearn.neural_network import MLPClassifier
import pandas
import numpy
import os
import sys

# Remove row/column display limit in order to visualise all data
# So that everything can be seen and verified for troubleshooting
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
numpy.set_printoptions(threshold=sys.maxsize)

# Converts the relative directory of training data file into an absolute directory
# An absolute directory is required as an imput in the pandas.read_excel function
directory = os.path.dirname(__file__)
datafile = os.path.join(directory, r'.\trainingdata.xlsx')

# Read excel file and assign the data to a variable
# iloc function numerically locates [rownumbers,columnnumbers], numpy.r_[] concatenates arrays of rows
# x:y , where it is inclusive of x, but exclusive of y
test_sheet = pandas.read_excel (datafile, sheet_name='CN4_table_all_cat_9767')
ideal_sheet = pandas.read_excel (datafile, sheet_name='All-model')

# Depending on how the data is formatted in excel
# The column numbers listed here may be different
# Dimensions are always in no. of rows X no. of columns format
idealset = ideal_sheet.iloc[:,numpy.r_[9:21,22:39]]
idealresult = ideal_sheet.iloc[:,21]
testdata = test_sheet.iloc[:,numpy.r_[9:21,22:39]]
testlabel = test_sheet.iloc[:,[1,3]]

# Convert DataStructure into numpy array for computing purposes
# idealdata dimensions: 3780 x 29
# idealitems dimensions: 3780 rows (x 1 column)
# testset dimensions: 9767 x 29
idealdata = idealset.to_numpy()
idealitems = idealresult.to_numpy()
testset = testdata.to_numpy()
truetestlabel = testlabel.to_numpy()

idealresultdata = numpy.zeros((len(idealitems),4))

for ind, element in enumerate(idealitems):
    if idealitems[ind] == 'T-4':
        idealresultdata[ind, 0] = 1
    if idealitems[ind] == 'SP-4':
        idealresultdata[ind, 1] = 1
    if idealitems[ind] == 'SPY-4':
        idealresultdata[ind, 2] = 1
    if idealitems[ind] == 'SS-4':
        idealresultdata[ind, 3] = 1

# To use idealdata for training, idealresultdata for training targets
# testset for test, so that results will be produced

clf = MLPClassifier(hidden_layer_sizes=(10,10),max_iter=100000,solver='lbfgs',alpha=1e-5,random_state=1)
clf.fit(idealdata, idealresultdata)

prediction = clf.predict(testdata)

# Convert prediction back to string results
dummyarray = []
for i in range(len(prediction)):
    dummyarray.append("          ")

dummyarray2 = numpy.array(dummyarray)
predictedresult = dummyarray2.reshape((-1,1))

for ind, element in enumerate(prediction):
    A = ""
    B = ""
    C = ""
    D = ""
    row = prediction[ind]
    if row[0] == 1:
        A = 'T-4 '
    if row[1] == 1:
        B = 'SP-4 '
    if row[2] == 1:
        C = 'SPY-4 '
    if row[3] == 1:
        D = 'SS-4'
    rowstring = A + B + C + D
    predictedresult[ind] = rowstring

print(numpy.concatenate((truetestlabel,predictedresult),axis=1))
