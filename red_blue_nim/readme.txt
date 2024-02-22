1) Name and UTA ID: Hyun Ho Kim 1001967176

2) programming language: Python 3.11.4

3) The code's structure.
There are 7 functions and a main.
functions:
    i) cal_points(state): A function that calculates and returns points based on the number of marbles left.
    ii) Minimax_Decision(state,version,alpha,beta): A function that works like an interface. A computer chooses either a max player or a min player depending on the version of the game.
    iii) Max_Value(state,alpha,beta,version): A function that returns an action it takes and the maximum value among the minimum values, which are its successors.
    iv) Min_Value(state,alpha,beta,version): A function that returns an action it takes and the minimum value among the maximum values, which are its successors.
    v) std_successors(state): A function that generates successors. It adds blue marble first, and then red mable.
    vi) mj_successors(state): A function that generates successors. It adds red marble first, and then blue mable.
    vii) whos_winner(point,player,version): A function the receives the final points and prints out the final scores of both, once one of red or blue marbles becomes 0. Depending on the version, it will print out the opposite result of the standard version.
main:
    i) Check the number of arguments is vaild depending on the input.
    ii) Check and store the number of red and blue marbles depending on the input.
    iii) Check and store version depending on the input (Default is standard).
    iv) Check and store first player depending on the input(Default is computer).
    v) Loop until one of the red or blue marbles becomes 0. The computer always uses minimax algorithm to pick a marble and a user type to pick a marble. The initial values of alpha and beta are set to negative infinity and positive infinity, respectively.
    vi) Call the result.

4) Examples of running the code
Format: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>
<version> is optional [standard/misere] (Default is standard)
<first-player> is optional [computer/human](Default is computer)

command line : python3 red_blue_nim.py 2 3
    red: 2, blue: 3
    Version: standard
    first player: computer
command line : python3 red_blue_nim.py 3 3 misere
    red: 3, blue: 3
    Version: misere
    first player: computer
command line : python3 red_blue_nim.py 5 3 misere human
    red: 5, blue: 3
    Version: misere
    first player: human

After entering a valid command line, the program will prompt you to select a marble. For example, you will see 'Your action:', and then you should type 'red' or 'blue' to indicate your choice.
During the computer's turn, it will utilize the Minimax algorithm to select a marble. Then, during the user's turn, if there is at least one marble remaining on both sides, the program will prompt you to choose a marble.