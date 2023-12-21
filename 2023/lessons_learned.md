# Consider these options if you are stuck

1. Memoization
    - If you have to compute the same values over and over, store them in a dict and look for
      solutions there before computing them.
2. Recursion
    - Will you exceed the recursion depth of 1000 in Python? Is that OK for this task? Can be
      increased but not indefinitely.
3. Pathfinding:
    - BFS: Breadth First Search
        - Do not maintain distance travelled in each state. Evaluate points in the order that they
          were added to the list.
    - Dijkstra's
        - Maintain an ordered list, ordered by the distance travelled to get to each node.
        - The same as BFD if the distances between points in the graph are always equal.
    - A star
        - If there is a way of estimating distance left to target *without* overestimating that
          distance, you can use A star.
        - Maintain an ordered list of states, ordered by distance travelled + estimated distance
          remaining. Always evaluate the one with minimum f = g + h. As soon as you pick a state
          that is the end-point, that is the optimal solution.

# Day 1

Could have used string.startswith() instead of string[i:i+2], since I had to check that i+3 was
within the string first (and made OBOE:s of course).

# Day 10

I started working on a recursive solution that didn't even have a chance to work in the end. There
were way too many edge cases that I realistically could not hope to cover. I also struck the
recursive limit pretty quickly, which made it _impossible_ to debug.

I wanted to do a flood-fill and try to keep track of on which side I had a pipe, to try and thread
the cracks between pipes. That did not work..

Lessons:
- Do not just run with the first solution that comes to mind, if it seems like it doesn't fit the
  problem. If you can't convince yourself on pen and paper that it will work, think harder until you
  find something that feels convincing.
- Do not do a recursive solution if you suspect that it will require more than 1000 levels in
  Python. It gets IMPOSSIBLE to debug what the problem is and if your program would finish if it
  could only recurse further.

# Day 12

I should definitely have a list of things that I must consider when being stuck on a huge problem.
For day 12, I spent a looot of time thinking about how the hell to compute all of the different
combinations when the solution is simply 'memoization'. It was super fast to implement and runs
fast.

Adding that list to the top of this document.

# Day 15

Using 'myList = [[]] * 10' in Python will create 10 copies of the same list, and they can not be
modified independently, since they are the same list.

# Day 18

Shoelace Formula would have been handy to learn on day 10, since it came to use once again.

# Day 21

PRINT WHAT YOU'RE WORKING ON if you are fumbling in the dark. You almost always can, and it helps
tremendously. I wasted hours on today's question because I never printed and did not see that my
plan was never going to work.
