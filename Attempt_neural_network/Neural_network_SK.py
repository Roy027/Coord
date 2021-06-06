# https://stackabuse.com/introduction-to-neural-networks-with-scikit-learn/
# https://scikit-learn.org/stable/modules/neural_networks_supervised.html 

# Import main neural network module
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import pandas
import numpy
import os
import sys
import csv

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
test_sheet = pandas.read_excel (datafile, sheet_name='testset_general')
ideal_sheet = pandas.read_excel (datafile, sheet_name='trainingset')

# Extract cif filename and site names
rawtestlabel = test_sheet.iloc[:,[0,1]]
testlabel = rawtestlabel.to_numpy()
rawideallabel = ideal_sheet.iloc[:,[0,1]]
ideallabel = rawideallabel.to_numpy()

# Depending on how the data is formatted in excel
# The column numbers listed here may be different
# Dimensions are always in no. of rows X no. of columns format
# [8:26] if include dot products, [14:26] if exclude dot products
idealset = ideal_sheet.iloc[:,numpy.r_[8:26]]
idealresult = ideal_sheet.iloc[:,6]
testset = test_sheet.iloc[:,numpy.r_[8:26]]
testresultanswer = test_sheet.iloc[:,6]

# Convert DataStructure into numpy array for computing purposes
# Total number of labelled data: 
# idealdata dimensions: 
# idealresult dimensions:  rows (x 1 column)
# testset dimensions: 
# - testset_general: 
# - easy: 
# - medium: 
# - hard: 
# - controversial:
# ( x 18C if include dot products, or X 12C if exclude dot products)
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
# Have to scale the model data too
min_max_scaler = preprocessing.MinMaxScaler()
scaled_data = min_max_scaler.fit_transform(predictee)
scaled_ideal_data = min_max_scaler.fit_transform(idealset)

# Count total number of sites belonging to a structure
# Stored in an array. [n_T-4, n_SP-4, n_SPY-4, n_SS-4]
each_struc_ideal_count = numpy.zeros(len(predictee_results[0]))
for row in predictee_results:
    each_struc_ideal_count = each_struc_ideal_count + row

errors = []

with open(r'.\NNdata.csv', mode='w') as dotfile:
    file_writer = csv.writer(dotfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for nomo in range(3,18):
        clf = MLPClassifier(hidden_layer_sizes=(nomo+1),max_iter=10000,solver='lbfgs',alpha=0.01,random_state=1,activation="logistic")
        clf.fit(scaled_ideal_data, idealdata)
        probabilities = clf.predict_proba(scaled_data)

        prediction = numpy.zeros((len(scaled_data),len(probabilities[0])))
        # Convert probabilities into binary values
        # By selecting the highest value among the array and converting it to 1
        # While converting other probabilities to zero.
        for ind, element in enumerate(probabilities):
            # prediction[ind] = numpy.zeros(len(probabilities[0]))
            # Find the highest probability
            checking_value = 0
            checking_value_position = 0
            highest_value = 0
            highest_value_position = 0
            for i, prob in enumerate(element):
                checking_value = element[i]
                checking_value_position = i
                if checking_value > highest_value:
                    highest_value = checking_value
                    highest_value_position = i
            # Assign prediction results based on probability
            prediction[ind][highest_value_position] = 1


        # Accuracy algorithm
        # "Strict" accuracy is when for each entry, ALL values are correct
        NumStrictCorrect_arr = numpy.zeros(len(predictee_results[0]))
        MaxCorrect = len(predictee_results)
        for ind, element in enumerate(prediction):
            if numpy.all(prediction[ind] == predictee_results[ind]):
                NumStrictCorrect_arr = NumStrictCorrect_arr + predictee_results[ind]
            elif nomo > 9:
                errors.append([str(predictee_label[ind]),str(probabilities[ind])])

        strict_indiv_perC = numpy.around(100*NumStrictCorrect_arr/each_struc_ideal_count, 5)

        # Count number of correct answers
        strict_global_correct = 0
        for i in NumStrictCorrect_arr:
            strict_global_correct = strict_global_correct + i
        strict_global_perC = str(round(strict_global_correct*100/MaxCorrect,5))

        print("~~~~~~~~~~~~~~~~~ SUMMARY ~~~~~~~~~~~~~~~~~")
        print("Strictly, global percentage accuracy is: " + strict_global_perC + "%.")
        print("Accuracy for T-4 is " + str(strict_indiv_perC[0]) + "%")
        print("Accuracy for SP-4 is " + str(strict_indiv_perC[1]) + "%")
        print("Accuracy for SPY-4 is " + str(strict_indiv_perC[2]) + "%")
        print("Accuracy for SS-4 is " + str(strict_indiv_perC[3]) + "%")

        file_writer.writerow([str(strict_indiv_perC[0]),str(strict_indiv_perC[1]),str(strict_indiv_perC[2]),str(strict_indiv_perC[3])])

# Print list of wrongly-predicted sites
print(errors)

### To compare .cif file with predicted results
# Convert prediction back to string results
# Comment out exit() if there is a need to compare results.
exit()
dummyarray = []
for i in range(len(prediction)):
    dummyarray.append("          ")

dummyarray2 = numpy.array(dummyarray)
predictedresult = dummyarray2.reshape((-1,1))

for ind, element in enumerate(prediction):
    A = []
    B = []
    C = []
    D = []
    rowstring = []
    row = prediction[ind]
    if row[0] == 1:
        A.append('T-4 ')
    if row[1] == 1:
        B.append('SP-4 ')
    if row[2] == 1:
        C.append('SPY-4 ')
    if row[3] == 1:
        D.append('SS-4 ')
    rowstring.extend(A)
    rowstring.extend(B)
    rowstring.extend(C)
    rowstring.extend(D)
    predictedresult[ind] = str(rowstring)

# displaytext = numpy.concatenate((predictee_label,predictedresult),axis=1)
displaytext = numpy.concatenate((predictee_label,probabilities),axis=1)
print(displaytext)



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
