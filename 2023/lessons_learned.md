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
