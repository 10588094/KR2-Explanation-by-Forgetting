import os

# This is an example python programme which shows how to use the different stand-alone versions of OWL reasoners and forgetting programme

# Choose the ontology (in the OWL format) for which you want to explain the entailed subsumption relations.
#inputOntology = "datasets/pizza.owl"

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
#inputSubclassStatements = "datasets/subClasses.nt"

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

######################### EXPERIMENT ######################

def get_signature(inputOntology, inputSubclassStatements):
    # return the best option
    return "datasets/signature.txt"


# inputOntology = total ontology, like 'exp10-1.omn'
# inputSubclassStatements = subclass statement(s) for which you want an explanation, often just one.
def explain_by_forgetting(inputOntology, inputSubclassStatements, method):

    # Transform .omn file to .owl file using LETHE and emtpy signature
    signature = "datasets/empty_signature.txt"
    os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' + inputOntology + ' --method ' + method  + ' --signature ' + signature)
    inputOntology = "result.owl"

    i = 1
    while True:
        # Get a signature
        signature = get_signature(inputOntology, inputSubclassStatements)
        if (1 < 0): # if signature is emtpy
            break
        # Forget:
        os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile ' + inputOntology + ' --method ' + method + ' --signature ' + signature)
        # set the resulting ontology as the new ontology
        inputOntology = "result.owl"
        # and save the result as forget_gen_i.owl
        os.rename("result.owl","forget_gen_" + str(i) + ".owl")
        i+= 1
        break


ont = "datasets/exp1.omn"
subset = "datasets/subclass1.nt"
explain_by_forgetting(ont, subset, "2")