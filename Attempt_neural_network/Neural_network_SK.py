# https://stackabuse.com/introduction-to-neural-networks-with-scikit-learn/
# https://scikit-learn.org/stable/modules/neural_networks_supervised.html 

# Import main neural network module
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn import preprocessing
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
test_sheet = pandas.read_excel (datafile, sheet_name='testset_easy')
ideal_sheet = pandas.read_excel (datafile, sheet_name='trainingset')

# Extract cif filename and site names
rawtestlabel = test_sheet.iloc[:,[0,1]]
testlabel = rawtestlabel.to_numpy()
rawideallabel = ideal_sheet.iloc[:,[0,1]]
ideallabel = rawideallabel.to_numpy()

# Depending on how the data is formatted in excel
# The column numbers listed here may be different
# Dimensions are always in no. of rows X no. of columns format
idealset = ideal_sheet.iloc[:,numpy.r_[8:30]]
idealresult = ideal_sheet.iloc[:,6]
testset = test_sheet.iloc[:,numpy.r_[8:30]]
testresultanswer = test_sheet.iloc[:,6]

# Convert DataStructure into numpy array for computing purposes
# Total number of labelled data: 8104, 304, 163, 218 = 8789
# idealdata dimensions: 6184, 304, 163, 218 = 6869( x 22C)
# idealresult dimensions: 6869 rows (x 1 column)
# testset dimensions: 
# - easy: 50, 99, 34, 31
# - medium: 1903, 189, 163, 126
# - hard: 4773, 155, 163, 218
# ( x 22C)
idealdata = idealset.to_numpy()
idealitems = idealresult.to_numpy()
testdata = testset.to_numpy()
testresultanswers = testresultanswer.to_numpy()

idealdata = numpy.zeros((len(idealitems),4))

for ind, element in enumerate(idealitems):
    if idealitems[ind] == 'T-4':
        idealdata[ind, 0] = 1
    if idealitems[ind] == 'SP-4':
        idealdata[ind, 1] = 1
    if idealitems[ind] == 'SPY-4':
        idealdata[ind, 2] = 1
    if idealitems[ind] == 'SS-4':
        idealdata[ind, 3] = 1

idealtestdata = numpy.zeros((len(testresultanswers),4))

for ind, element in enumerate(testresultanswers):
    if testresultanswers[ind] == 'T-4':
        idealtestdata[ind, 0] = 1
    if testresultanswers[ind] == 'SP-4':
        idealtestdata[ind, 1] = 1
    if testresultanswers[ind] == 'SPY-4':
        idealtestdata[ind, 2] = 1
    if testresultanswers[ind] == 'SS-4':
        idealtestdata[ind, 3] = 1

# To use idealdata for training, idealresultdata for training targets
# testset for test, so that results will be produced
###########################################################################################
# Allocation of variables here so that there's only one area to be changed
# predictee = testset
# predictee_label = testlabel
# predictee_results = idealtestdata
predictee = idealset
predictee_label = ideallabel
predictee_results = idealdata
###########################################################################################

# Scaling of data to range [0,1]
# Otherwise one descriptor might overshadow other descriptors
min_max_scaler = preprocessing.MinMaxScaler()
scaled_data = min_max_scaler.fit_transform(predictee)

# Count total number of sites belonging to a structure
# Stored in an array. [n_T-4, n_SP-4, n_SPY-4, n_SS-4]
each_struc_ideal_count = numpy.zeros(len(predictee_results[0]))
for row in predictee_results:
    each_struc_ideal_count = each_struc_ideal_count + row

clf = MLPClassifier(hidden_layer_sizes=(22),max_iter=10000,solver='lbfgs',alpha=0.1,random_state=1,activation='relu')
clf.fit(idealset, idealdata)

# To test prediction within ideal data
# prediction = clf.predict(idealdata)
# To test prediction within test data
prediction = clf.predict(scaled_data)


# Accuracy algorithm
# "Normal" accuracy is when for each entry, at least one value is correct
# "Strict" accuracy is when for each entry, ALL values are correct
NumCorrect_arr = numpy.zeros(len(predictee_results[0]))
NumStrictCorrect_arr = numpy.zeros(len(predictee_results[0]))
MaxCorrect = len(predictee_results)
for ind, element in enumerate(prediction):
    if numpy.all(prediction[ind] == predictee_results[ind]):
        NumStrictCorrect_arr = NumStrictCorrect_arr + predictee_results[ind]
    for i, struct_type in enumerate(prediction[ind]):
        if prediction[ind][i] == predictee_results[ind][i] and prediction[ind][i] != 0:
            NumCorrect_arr = NumCorrect_arr + predictee_results[ind]
            continue

indiv_perC = numpy.around(100*NumCorrect_arr/each_struc_ideal_count, 5)
strict_indiv_perC = numpy.around(100*NumStrictCorrect_arr/each_struc_ideal_count, 5)

global_correct = 0
strict_global_correct = 0
for i in NumCorrect_arr:
    global_correct = global_correct + i
for i in NumStrictCorrect_arr:
    strict_global_correct = strict_global_correct + i
global_perC = str(round(global_correct*100/MaxCorrect,5))
strict_global_perC = str(round(strict_global_correct*100/MaxCorrect,5))

print("~~~~~~~~~~~~~~~~~ SUMMARY ~~~~~~~~~~~~~~~~~")
print("Global percentage accuracy is: " + global_perC + "%.")
print("Strictly, global percentage accuracy is: " + strict_global_perC + "%.")
print("Accuracy for T-4 is " + str(indiv_perC[0]) + "% (" + str(strict_indiv_perC[0]) + "%)")
print("Accuracy for SP-4 is " + str(indiv_perC[1]) + "% (" + str(strict_indiv_perC[1]) + "%)")
print("Accuracy for SPY-4 is " + str(indiv_perC[2]) + "% (" + str(strict_indiv_perC[2]) + "%)")
print("Accuracy for SS-4 is " + str(indiv_perC[3]) + "% (" + str(strict_indiv_perC[3]) + "%)")


########### Scrapped content #1 #############################################################################

# # Convert prediction back to string results
# dummyarray = []
# for i in range(len(prediction)):
#     dummyarray.append("          ")

# dummyarray2 = numpy.array(dummyarray)
# predictedresult = dummyarray2.reshape((-1,1))

# for ind, element in enumerate(prediction):
#     A = []
#     B = []
#     C = []
#     D = []
#     rowstring = []
#     row = prediction[ind]
#     if row[0] == 1:
#         A.append('T-4 ')
#     if row[1] == 1:
#         B.append('SP-4 ')
#     if row[2] == 1:
#         C.append('SPY-4 ')
#     if row[3] == 1:
#         D.append('SS-4 ')
#     rowstring.extend(A)
#     rowstring.extend(B)
#     rowstring.extend(C)
#     rowstring.extend(D)
#     predictedresult[ind] = str(rowstring)

# # Depending on data used, concatenate different sets of labels.
# #displaytext = numpy.concatenate((ideallabels,predictedresult),axis=1)
# # displaytext = numpy.concatenate((predictee_label,predictedresult),axis=1)
# # print(displaytext)

########### Scrapped content #2 ################################################################################
# ideal_proba = numpy.zeros(len(predictee_results[0]))
# for row in predictee_results:
#     ideal_proba = ideal_proba + row

# ideal_proba = ideal_proba/len(predictee_results)


# print("####### SUMMARY #######")
# probabilities = clf.predict_proba(scaled_data)
# net_proba = numpy.zeros(len(probabilities[0]))

# for row in probabilities:
#     net_proba = net_proba + row

# net_proba = net_proba/len(probabilities)
# print("                          " + str(["T-4","SP-4","SPY-4","SS-4"]))
# print("The predicted results are " + str(net_proba))
# print("Ideally it should be      " + str(ideal_proba))
# print("The ratio is              " + str(net_proba/ideal_proba))

# net_diff = numpy.zeros(len(predictee_results[0]))
# for ind, element in enumerate(predictee_results):
#    net_diff = net_diff + predictee_results[ind] - probabilities[ind]
# net_diff = net_diff/len(predictee_results)
# # For average difference, positive values means underprediction, negative values means overprediction
# print("Average difference is     " + str(net_diff))