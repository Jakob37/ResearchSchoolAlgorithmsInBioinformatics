# Models of computation

Questions:

### Describe the RAM model. What assumptions are made and how well does it match an actual computer?
 
Similar to 'counter machine', with ability of indirect addressing of registers.

Counter machine: Can hold single non-negative integer and list of
arithmetic and control instructions for machine to follow.

Under RAM model each simple operation takes 1 step. Loops and subroutines
are considered many single-step operations. Each memory access takes a single
step. It takes no notice of cached data.

It simplifies the computer - for instance multiplication takes more time
than addition on most processors. Memory access differ greatly with caching
or if on disk. But is still useful tool for understanding behaviour of
computers.

So - true results can differ a bit, but generally not much.

### Name and describe two other important models of computation

Turing machine: 

* Operates on infinite memory tape with discrete cells.
* It positions head over cell and scans symbol there. 
* Then, it writes symbol in the cell. 
* Then either moves tape 1 step right/left, then proceeds to next instruction or halts.

Finite-state machine:

* Can exist in one of a finite number of states at a time
* It can change state in response to external inputs - transition
* Defined by initial states, list of states and conditions for transitions

Limited in power compared to turing machine. Limited in memory through
number of states.

# Complexity analysis

How many steps are needed for calculation? How does it scale with input size?

Here, we use asymptotic analysis to estimate rate of scaling.

*Time complexity* is the asymptotic estimate of number of needed steps.

*Space complexity* is the amount of memory, asymptotically as function of
input size an algorithm would need.

Questions:

* What does the Big-Oh notation mean? For a programmer? For a mathematician?

For mathematician: How function behaves when moving either towards particular
value, or towards infinity.

For programmer: Analyzing algorithms for efficiency. The trend of the number
of steps for a particular algorithm. Checking what part of it dominates,
and then describe that.

* What following statements are true?
    * 2n + 17 is in O(n) - True
    * 10n is in O(n*2) - False
    * n^2 + log n is in O(n^2) - True
    
* Why do we talk about "time complexity" but report asymptotic number of steps?

Because processing time is directly related to the number of operations needed.
The processor works in clock cycles. The time it takes to process scales with
the number of cycles needed for the calculation.

* Consider problem of multiplying two n-digit integers. What is the time
    complexity if we take single-digit multiplication and addition as the
    elementary operations?

Start values: nnnnn * mmmmmm

Using basic 'manual' calculation, we can calculate this by comparing first
the lowest digit, multiply, add rest and then compare first. We would iteratively
wander through all the combinations of digits, generating m n-length numbers
which we then would add up.

If multiplying with itself, this would scale quadratically with the length:

2 would mean 4 operations
3 would mean 9 operations

So, we end up with O(n^2)