Name and ID: Hyun Ho Kim 1001967176
Version: Python 3.11.4
Structure:
    1) Class Node:
        - For saving selected attributed selected, the threshold, and attribute, child nodes.
    3) verifying argument:
        - Check_arguments.
    2) Calculating functions:
        - Entropy, distribution, information_gain
    3) The function for making trees:
        - DTL
    4) Algorithms how to make tree:
        - optimized_attribute, randomized_attribute
    5) main:
        - To choose right algorithm depending on the option
    6) The function for classifying:
        - single_tree_classify: retrieve the right label.
    7) The function for making output file, counting correct labels, and calculating the accuracy
        - test_decision_tree (for optimized and randomized), test_forest (for forest3 and forest15)
The ways to run the code:
Format: python3 dtree.py *_training.txt *_test.txt option
- Please adjust * with the appropriate filename.
- option: optimized / randomized / forest3 / forest15
The examples of command lines:
 1) python3 dtree.py pendigits_training.txt pendigits_test.txt optimized
 2) python3 dtree.py pendigits_training.txt pendigits_test.txt randomized
 3) python3 dtree.py pendigits_training.txt pendigits_test.txt forest3
 4) python3 dtree.py pendigits_training.txt pendigits_test.txt forest15

When it finishes compiling, it will create a output file (output.txt) for the result!