import os
import re
import sys
import random
import shutil
import collections
from owlready2 import *

Strategy = sys.argv[1]

# strategy, random on default 
strategy1 = False
strategy2 = False
strategy3 = False

if Strategy == "-S1": #less frequent classes first
    strategy1 = True
elif Strategy == "-S2": #most frequent classes first
    strategy2 = True
else:
    strategy3= True #random
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
    subclasses.close()
    # for every subset
    for line in lines:
        if line.strip():
            if file_count<11:
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
                #number sub
                x = expFile.find("-")
                y = expFile.find(".")
                t=expFile[(x+1):y]
                
                newName = "datasets/justifications/exp" + str(fileList.index(file) + 1) + "-" + str(t) + "_gen_0.omn"
                oldName = "datasets/" + str(expFile)
                os.rename(oldName, newName)

                #opening new file
                counter = 0
                with open(newName) as checkFile:
                    content = checkFile.read()
                    lines = content.split("\n")
                    #counting amount of lines
                    for i in lines:
                        if i:
                            counter+=1 
                #delete small justifications
                if counter<5:
                    os.remove(newName)

def get_signature_minmax(inputOntology, inputSubclassStatements):
    signature = "datasets/signature.txt"
    text = open(inputOntology)
    subclass = open(inputSubclassStatements, 'r')
    print(text)
    print(subclass)

    list_axioms = []
    list_subclasses = []

    base_uri = "http://www.co-ode.org/ontologies/pizza/pizza.owl#"
    full_classes = []
    onto = get_ontology(inputOntology).load()
    ontoClasses = list(onto.classes())
    print(ontoClasses)

    # read inputSubclassStatemnt
    for line in text:
        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, line)
        for lnk in links:
            if lnk[0] == "http://www.w3.org/2002/07/owl#" or lnk[0] == "http://www.w3.org/2002/07/owl" or lnk[
                0] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#" or lnk[0] == "http://www.w3.org/2002/07/owl#" or \
                            lnk[0] == "http://www.w3.org/2001/XMLSchema#" or lnk[
                0] == "http://www.w3.org/2000/01/rdf-schema#" or lnk[0] == "http://owlapi.sourceforge.net":
                pass
            else:
                axiom = lnk[0]
                for item in ontoClasses:
                    signatureOption = base_uri + str(item).lstrip('pizza.')
                    full_classes.append(signatureOption)
                if axiom in full_classes:
                    list_axioms.append(axiom)

    url_counts = collections.Counter(list_axioms)

    for line in subclass:
        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, line)
        for lnk in links:
            list_subclasses.append(lnk[0])

    subclass_count = collections.Counter(list_subclasses)
    print('sub', subclass_count)

    for url in list(url_counts.keys()):
        if url in subclass_count:
            del url_counts[url]

    print('url', url_counts)

    if url_counts != {}:
        if (strategy2):
            newSignature = max(url_counts, key=url_counts.get)
        else:
            newSignature = min(url_counts, key=url_counts.get)
        sigContent = newSignature
    else:
        print('sigcontent is leeg')
        sigContent = False

    print('sigContent:', sigContent)

    # Write signature file
    f = open(signature, "w")
    if sigContent:
        f.write(sigContent)
    f.close()
    text.close()
    subclass.close()

    return signature

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
    f = open(signature, "w")
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
        os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' 
                  + inputOntology + ' --method ' + method  + ' --signature ' + signature)

        # # replace .omn by .owl file for first gereration (..._gen_0.owl)
        os.remove(inputOntology) # remove ..._gen_0.owl
        inputOntology = re.sub(r'(.omn)','.owl',inputOntology)
        os.rename("result.owl", inputOntology) # change result.owl to datasets/justifications/exp1-1_gen_0.owl

        i = 1
        while (True):

            # Get a new signature
            if (strategy3):
                signature = get_signature(inputOntology, subclassStatement)
            else:
                signature = get_signature_minmax(inputOntology, subclassStatement)

            # if signature is emtpy, end function
            if (os.stat("datasets/signature.txt").st_size == 0):
                break # goes to next justification file

            # Forget:
            os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' 
                      + inputOntology + ' --method ' + method + ' --signature ' + signature)

            # save the result as expx-y_gen_{i}.owl
            newGeneration = str(re.sub(r'\d+(?=.owl)', str(i), inputOntology))
            os.rename("result.owl", newGeneration)

            # set new file as new inputOntology, repeat forgetting
            inputOntology = newGeneration
            i += 1

def owl_len(fname):
    onto = get_ontology(fname).load()
    axiomList = list(onto.general_axioms())
    return len(axiomList)

def analyse():
    fileList = sorted(os.listdir("datasets/justifications/"), key=natural_keys)
    currentExp = 'exp1-1'
    expList = []
    expSumList = []
    sum = 0
    for file in fileList:
        newExp = re.search('(.+)(?=_gen)', file).group(1)
        if newExp != currentExp:
            expList.append(currentExp)
            expSumList.append(sum)
            sum = 0
            currentExp = newExp
        # calculate sum
        sumFile = owl_len('datasets/justifications/' + file)
        sum += sumFile
    return expList,expSumList

################# RUNNING ################

inputOntology = "datasets/pizza_super_simple.owl"

#deleting files in directory
shutil.rmtree("datasets/justifications")
shutil.rmtree("datasets/subsets")
#making dir again
os.mkdir("datasets/justifications")
os.mkdir("datasets/subsets")

## first save all subsets
save_subsets(inputOntology)

## save all explanations of this subset
save_explanations()

## for every explanation, compute all forgetting iterations
explain_all_by_forgetting("2")

## analyse the results
# expList, expSumList = analyse()
# print(expList)
# print(expSumList)