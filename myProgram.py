import os
import re
import random
from owlready2 import *

# This is an example python programme which shows how to use the different stand-alone versions of OWL reasoners and forgetting programme

# Choose the ontology (in the OWL format) for which you want to explain the entailed subsumption relations.
# inputOntology = "datasets/animals.owl"

# 1. PRINT ALL SUBCLASSES (inputOntology):
# print all subClass statements (explicit and inferred) in the inputOntology
# --> uncomment the following line to run this function
#os.system('java -jar kr_functions.jar ' + 'printAllSubClasses' + " " + inputOntology)

# 2. SAVE ALL SUBCLASSES (inputOntology):
# save all subClass statements (explicit and inferred) in the inputOntology to file datasets/subClasses.nt
# --> uncomment the following line to run this function
#os.system('java -jar kr_functions.jar ' + 'saveAllSubClasses' + " " + inputOntology)

# Choose the set of subclass for which you want to find an explanation.
# this file can be generated using the second command (saveAllSubClasses)
# inputSubclassStatements = "datasets/subClasses.nt"

# 3. PRINT ALL EXPLANATIONS (inputOntology, inputSubclassStatements):
# print explanations for each subClass statement in the inputSubclassStatements
# --> uncomment the following line to run this function
#os.system('java -jar kr_functions.jar ' + 'printAllExplanations' + " " + inputOntology + " " + inputSubclassStatements)

# 4. SAVE ALL EXPLANATIONS (inputOntology, inputSubclassStatements):
# save explanations for each subClass statement in the inputSubclassStatements to file datasets/exp-#.owl
# --> uncomment the following line to run this function
#os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + inputOntology + " " + inputSubclassStatements)

###########################FORGETTING############################

# Decide on a method for the forgetter (check the papers of LETHE to understand the different options).
# The default is 1, I believe.
# 1 - ALCHTBoxForgetter
# 2 - SHQTBoxForgetter
# 3 - ALCOntologyForgetter
#method = "2"

# Choose the symbols which you want to forget.
#signature = "datasets/signature.txt"

# Choose the ontology to which you want to apply forgetting. This can be the inputOntology, but in practise
# should be a smaller ontology, e.g. created as a justification for a subsumption
#forgetOntology = "datasets/exp79-1.omn"

# For running LETHE forget command:
# --> uncomment the following line to run this function
#os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' + forgetOntology + ' --method ' + method  + ' --signature ' + signature)

# https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

######################### EXPERIMENT ######################

def save_subsets(inputOntology):
    # first save all subsets
    os.system('java -jar kr_functions.jar ' + 'saveAllSubClasses' + " " + inputOntology)

    # then save all subsets in a separate file called "Subset_{number}"
    subclasses = open("datasets/subClasses.nt")
    lines = subclasses.readlines()
    file_count = 1
    # for every subset
    for line in lines:
        if line.strip():
            # save as individual subset
            with open('datasets/subsets/Subset_{}.nt'.format(file_count), 'w') as outfile:
                outfile.write(line)
        file_count += 1


def save_explanations():
    # for every subset, save all explanations for this subset
    fileList = sorted(os.listdir("datasets/subsets/"),key=natural_keys)
    for file in fileList:

        # save all explanations (to datasets/ by default)
        filePath = "datasets/subsets/" + file
        os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + inputOntology + " " + filePath)

        # for every explanation, rename and add it to justifications folder
        for expFile in os.listdir("datasets"):
            if expFile.startswith("exp"):
                newName = "datasets/justifications/exp" + str(fileList.index(file) + 1) + "-" + str(expFile[5]) + "_gen_0.omn"
                oldName = "datasets/" + str(expFile)
                os.rename(oldName, newName)


def get_signature(inputOntology, inputSubclassStatements):
    signature = "datasets/signature.txt"

    # read inputSubclassStatemnt
    subclassStatements = []
    subClassFile = open(inputSubclassStatements)
    data = subClassFile.read().split(' ')

    for statement in data:
        subclassStatements.append(statement.strip('<>'))

    # Read input ontology
    base_uri = "http://www.co-ode.org/ontologies/pizza/pizza.owl#"
    onto = get_ontology(inputOntology).load()
    ontoClasses = list(onto.classes())

    sigContent = False

    # pick random class that is not an input subclass
    while True:
        item = random.choice(ontoClasses)
        signatureOption = base_uri + str(item).lstrip('pizza.')

        if signatureOption in subclassStatements:
            ontoClasses.remove(item)
            if ontoClasses == []:
                break
        else:
            sigContent = signatureOption
            break

    # Write signature file
    f = open(signature, "a")
    f.truncate(0)
    if sigContent:
        f.write(sigContent)
    f.close()

    return signature


def explain_all_by_forgetting(method):
    # for all files in datasets/justifications
    fileList = sorted(os.listdir("datasets/justifications/"), key=natural_keys)
    for file in fileList:

        # set subset file
        subsetNumber = re.findall(r'\d*(?=-)',file) # 122
        subclassStatement = "datasets/subsets/Subset_" + str(subsetNumber[0]) + ".nt"

        ## Transform .omn file to .owl file using LETHE and emtpy signature
        inputOntology = "datasets/justifications/" + file
        signature = "datasets/empty_signature.txt"
        os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' + inputOntology + ' --method ' + method  + ' --signature ' + signature)

        ## replace .omn by .owl file for first gereration (..._gen_0.owl)
        os.remove(inputOntology) # remove ..._gen_0.owl
        inputOntology = re.sub(r'(.omn)','.owl',inputOntology)
        os.rename("result.owl", inputOntology) # change result.owl to datasets/justifications/exp1-1_gen_0.owl

        i = 1
        while True:

            # Get a new signature
            signature = get_signature(inputOntology, subclassStatement)

            # if signature is emtpy, end function
            if (os.stat("datasets/signature.txt").st_size == 0):
                break # goes to next justification file

            # Forget:
            os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' + inputOntology + ' --method ' + method + ' --signature ' + signature)

            # save the result as expx-y_gen_{i}.owl
            os.rename("result.owl", str(re.sub(r'\d+(?=.owl)', str(i), inputOntology)))

            # set new file as new inputOntology, repeat forgetting
            inputOntology = str(re.sub(r'\d+(?=.owl)', str(i), inputOntology))
            i += 1


################# RUNNING ################

inputOntology = "datasets/pizza_super_simple.owl"

## first save all subsets
# save_subsets(inputOntology)

## save all explanations of this subset
# save_explanations()

## for every explanation, compute all forgetting iterations
explain_all_by_forgetting("2")
