Name: Hyun Ho Kim
UTA ID: 1001967176
programming language used: Python 3.11.4
Code structure: There are four big sections: 
    1. Classes - For creating and updating a node, and track the statistics.
    2. Functions - Calculate values, print a result, or assign a value.
    3. Methods - Breadth First Search / Uniform Cost Search / Greedy Seach / A* Search / Depth First Search / Depth Limited Search / Iterative Deepening Search
    4. Main - Read files, print result, check if the arguments valid, and pass initial variables to be filled up
How to run code:
    format: python3 expense_8_puzzle.py <start-file> <goal-file> [<method>] [<dump-flag>]
    <method>: bfs / ucs / greedy / a\* / dfs / dls / ids ; default: a\* ;
    <dump-flag>: true/false ; default: false ; if true, it creates a trace<date><time>.txt file;

    Examples:
        To run the code with default A* search and without dump:
            python3 expense_8_puzzle.py start.txt goal.txt

        To run the code with A* search and create a dump file:
            python3 expense_8_puzzle.py start.txt goal.txt a* true

        To run the code with Greedy search:
            python3 expense_8_puzzle.py start.txt goal.txt greedy

        To run the code with BFS and create a dump file:
            python3 expense_8_puzzle.py start.txt goal.txt bfs true

        To run the code with UCS:
            python3 expense_8_puzzle.py start.txt goal.txt ucs

	To run the code with IBS:
	    python3 expense_8_puzzle.py start.txt goal.txt ids
	
	To run the code with DLS:
 	    python3 expense_8_puzzle.py start.txt goal.txt ids
	    
	    when you see "Enter the depth limit: ", you should type the depth limit.
	    *you might type more than 17 to see the solution.

