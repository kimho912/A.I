import sys
import math
import random

class Node:
    def __init__(self, attribute, threshold):
        self.attribute = attribute
        self.threshold = threshold
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

def check_arguments():
    if len(sys.argv) != 4:
        print("Format: dtree.py training_file.txt test_file.txt option")
        sys.exit("Incorrect number of arguments")
    
    training_file = str(sys.argv[1])
    test_file = str(sys.argv[2])
    option = str(sys.argv[3])
    
    if option not in ["optimized", "randomized", "forest3", "forest15"]:
        sys.exit("Please type a valid option [optimized / randomized / forest3 / forest15]")
    
    return training_file, test_file, option

def single_tree_classify(sample, node):
    # Check if node is an instance of Node. If not, it's a leaf node.
    if not isinstance(node, Node):
        return node  # node is actually a class label at a leaf

    # Continue traversing the tree if it's not a leaf node
    if sample[node.attribute] < node.threshold:
        return single_tree_classify(sample, node.left)
    else:
        return single_tree_classify(sample, node.right)


def test_decision_tree(tree, test_file):
    test_samples = []
    with open(test_file) as f:
        for line in f:
            sample = [float(x) for x in line.strip().split()]
            label = int(sample[-1])
            test_samples.append((sample[:-1], label))

    correct_predictions = 0
    with open("output.txt", "w") as output_file:
        for i, (features, true_label) in enumerate(test_samples):
            predicted_label = single_tree_classify(features, tree)
            
            # Assuming no ties in this implementation
            if predicted_label == true_label:
                accuracy = 1
                correct_predictions += accuracy
            else:
                accuracy = 0
            

            output_file.write(f"Object Index = {i}, Result = {predicted_label}, True Class = {true_label}, Accuracy = {accuracy}\n")

        # Calculate overall classification accuracy
        overall_accuracy = correct_predictions / len(test_samples)
        output_file.write(f"Classification Accuracy = {overall_accuracy}\n")
    return overall_accuracy
def test_forest(forest, test_file):
    test_samples = []
    with open(test_file) as f:
        for line in f:
            sample = [float(x) for x in line.strip().split()]
            label = int(sample[-1])
            test_samples.append((sample[:-1], label))

    correct_predictions = 0
    with open("output.txt", "w") as output_file:
        for i, (features, true_label) in enumerate(test_samples):
            predicted_labels = []
            for tree in forest:
                predicted_label = single_tree_classify(features, tree)
                predicted_labels.append(predicted_label)
            choiced_label = random.choice(predicted_labels)
            # Calculate accuracy
            if choiced_label == true_label:
                accuracy = 1
                correct_predictions += accuracy
            else:
                accuracy = 0

            output_file.write(f"Object Index = {i}, Result = {predicted_label}, True Class = {true_label}, Accuracy = {accuracy}\n")

        # Calculate overall classification accuracy
        overall_accuracy = correct_predictions / len(test_samples)
        output_file.write(f"Classification Accuracy = {overall_accuracy}\n")

def distribution(samples):
    label_counts = {}
    for sample in samples:
        label = sample[-1]
        label_counts[label] = label_counts.get(label, 0) + 1

    total_samples = len(samples)
    num_classes = len(label_counts)
    probabilities = [label_counts.get(i, 0) / total_samples for i in range(num_classes)]

    return probabilities


def entropy(samples):
    label_counts = {}
    for sample in samples:
        label_counts[sample[1]] = label_counts.get(sample[1], 0) + 1

    total_samples = len(samples)
    entropy_value = 0
    for label in label_counts:
        probability = label_counts[label] / total_samples
        entropy_value -= probability * math.log2(probability)
    return entropy_value

def information_gain(samples, attribute, threshold):
    # Divide samples into two groups based on the threshold
    left_split = []
    right_split = []
    for s in samples:
        if s[0][attribute] < threshold:
            left_split.append(s)
        elif s[0][attribute] >= threshold:
            right_split.append(s)
    
    # Calculate entropy before the split
    initial_entropy = entropy(samples)
    
    # Calculate weighted entropy after the split
    total_samples = len(samples)
    entropy_left = entropy(left_split)
    entropy_right = entropy(right_split)
    weighted_entropy = (len(left_split) / total_samples) * entropy_left + (len(right_split) / total_samples) * entropy_right
    
    # Information gain is the difference in entropy
    return initial_entropy - weighted_entropy

def optimized_attribute(samples, attributes):
    best_gain = best_attribute = best_threshold = -1

    for attribute in attributes:
        # Find the minimum (L) and maximum (M) values for the attribute
        attribute_values = []
        for sample in samples:
            value = sample[0][attribute]
            attribute_values.append(value)
        L = min(attribute_values)
        M = max(attribute_values)

        # Generate 50 thresholds
        for K in range(1, 51):
            threshold = L + K * (M - L) / 51
            gain = information_gain(samples, attribute, threshold)
            if gain > best_gain:
                best_gain = gain
                best_attribute = attribute
                best_threshold = threshold

    return best_attribute, best_threshold
def randomized_attribute(samples, attributes):
    best_gain = best_threshold = -1

    random_attribute = random.choice(attributes)

    attribute_values = []
    for sample in samples:
        value = sample[0][random_attribute]
        attribute_values.append(value)
    
    L = min(attribute_values)
    M = max(attribute_values)

    for K in range(1, 51):
        threshold = L + K * (M - L) / 51
        gain = information_gain(samples, random_attribute, threshold)
        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold
    
    return random_attribute,best_threshold

def DTL(samples, attributes, default, option):
    if not samples:
        return default
    
    # Flag set to check if all of them are the same class
    all_same_class = True
    for sample in samples:
        if sample[1] != samples[0][1]:
            all_same_class = False
            break
    if all_same_class == True:
        return samples[0][1]

    # Best attribute and threshold for the split
    if option == "optimized":
        best_attribute, best_threshold = optimized_attribute(samples, attributes)
    elif option == "randomized":
        best_attribute, best_threshold = randomized_attribute(samples, attributes)

    # Create a new decision tree
    tree = Node(best_attribute, best_threshold)

    examples_left = []
    examples_right = []
    for s in samples:
        if s[0][best_attribute] < best_threshold:
            examples_left.append(s)
        elif s[0][best_attribute] >= best_threshold:
            examples_right.append(s)
    
    tree.left = DTL(examples_left, attributes, distribution(examples_left), option)
    tree.right = DTL(examples_right, attributes, distribution(examples_right), option)

    return tree

# def build_forest(samples, attributes, default, option, num_trees):
#     forest = []
#     for _ in range(num_trees):
#         tree = DTL(samples, attributes, default, option)
#         forest.append(tree)
#     return forest

# Constants
training_file, test_file, option = check_arguments()

# Code
samples = []
with open(training_file) as f:
    for line in f:
        sample = [float(x) for x in line.strip().split()]
        label = int(sample[-1])
        samples.append((sample[:-1], label))

# The number of attributes
num_features = len(samples[0][0])
# Create a list of attribute indices
attributes = list(range(num_features))


forest = []
if option == "forest3":
    for _ in range(3):
        tree = DTL(samples, attributes, distribution(samples), "randomized")
        forest.append(tree)
    # Test the trained model
    test_forest(forest, test_file)
elif option == "forest15":
    for _ in range(15):
        tree = DTL(samples, attributes, distribution(samples), "randomized")
        forest.append(tree)
    # Test the trained mode
    test_forest(forest, test_file)
elif option in ["optimized", "randomized"]:
    tree = DTL(samples, attributes, distribution(samples),option)
    # Test the trained mode
    test_decision_tree(tree, test_file)

