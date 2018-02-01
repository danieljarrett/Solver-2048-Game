Adversarial Search
====

An AI for the 2048-Game through Minimax with *α*\-*β* Pruning and Gradient Descent for Heuristic Weights.

### Overview

We implement the Player AI using the minimax algorithm with alpha-beta pruning. There are two components to the recursive implementation: the maximizing layer, and the minimizing layer. At a given node, the maximizing layer computes and returns the move and corresponding utility value associated with the successor node with the highest utility value reachable from the current node. Specifically, a move for the maximizer is defined as one of four possible directions: up, down, left, and right. Similarly, the minimizing layer computes and returns the move and corresponding utility value associated with the successor node with the lowest utility value reachable from the given node. Specifically, a move for the minimizer consists of placing a tile of value 2 or 4 in one of the empty spots on the board.

The set of successor states for the maximizer and minimizer, given the current state and the set of legal moves, are computed by permuting the current state with each legal move. This is done, respectively, through the permuteMax() and permuteMin() methods. The maximize() and minimize() methods respectively implement the maximizing and minimizing layers of the minimax recursion. They are almost identical, except for an extra guard clause present in the maximizer to check if the game is over. In each layer, three things are accomplished in each iteration through the successor states: (1) update the move and utility value associated with the optimal successor state, (2) return if the value of the current state is worse than the current  or , and (3) update the value of  or . When all the successor states have been evaluated, the method returns the final values for the move and corresponding utility value.

Searching all the way to terminal states is impractical. Therefore we cut off the search earlier and apply an evaluation function to the search states, which has the effect of turning non-terminal nodes into terminal leaves. Specifically, we make two alterations. First, instead of recursing all the way to terminal leaves, and having utility values propagate upwards from there, we compute the utility value through a heuristic evaluation function Eval.eval(). Second, in addition to the terminal test (i.e. test for whether or not the game is over), we also introduce a cutoff test that determines when to stop recursing and apply the evaluation.

### Results

At various allowances for computation, without printing to screen, our results are as follows:

| Depth  | Trials | 512  | 1024 | 2048 |
|--------|--------:|------:|------:|------:|
| 1-ply  | 1000   | 99%  | 85%  | 39%  |
| 2-ply  | 1000   | 100% | 87%  | 36%  |
| 10ms   | 500    | 100% | 98%  | 75%  |
| 100ms  | 100    | 100% | 100% | 100% |
| 1000ms | 50     | 100% | 100% | 100% |

Especially of note is the fact that even with no searching at all—i.e. the evaluation function is applied immediately on the first search layer—the algorithm still manages to achieve success, on average, almost 40% of the time. As the search depth or time limit increases, the success rate increases as well, give or take a margin allowing for sampling noise. Due to prohibitively long games, the sample sizes are smaller for experiments with longer allowances.

### Solve A Game Board



  To solve a game board, navigate to the code directory, and type:


	"python GameManager.py"


  The time allowance for computation can be changed by modifying the constant
  term in the setTimer() method call within the getMove() method definition
  in PlayerAI.py. For instance, to test the algorithm by only allowing 0.01
  seconds of computation per move, change:


	"setTimer(0.95)"

  to:


	"setTimer(0.01)"



### Bulk Test Statistics



  To run the algorithms on hundreds or thousands of instances to generate
  statistics, the GameManager can simply be copied and altered to repeat
  games with an extra code snippet. The statistics provided in the written
  report were generated with a simple loop and hash object, like so:


	trials = 1000

	results = {64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0, 4096: 0}

	for i in xrange(trials):
		result = main()

		gc.collect()

		while result >= 64:
			results[result] += 1

			result /= 2

	results = {key: value * 1.0 / trials for key, value in results.items()}

	pprint(results, width = 1)


  See above for the output of these experiments.

### Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request