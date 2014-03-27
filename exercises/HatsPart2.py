description = r"""
<i>COS 126 Fall 2012 Programming Midterm 1, part 2/2</i><br>
Please see the problem description in <a href="http://www.cs.princeton.edu/courses/archive/fall13/cos126/docs/mid1-f12-prog.pdf">
this PDF link</a>. Please use the alternate URL
<pre>
<a href="http://www.cs.princeton.edu/~cos126/docs/data/Hats/">http://www.cs.princeton.edu/~cos126/docs/data/Hats/</a>
</pre> to access
the sample input files.
<p>
This websheet is intended as a practice exam. However, in a real exam,
<ul>
<li>You'll upload via Dropbox
<li>You'll get limited feedback from Dropbox during the exam, and a different full set of test cases for grading
<li>Real humans will grade your real exams and also mark you on style and apply partial credit where appropriate
<li>Because of Websheet formatting, on this page you have to put your header inside the class. On the exam, put it at the top as usual
<li>We recommend coding in DrJava and/or the command-line and doing basic tests on your own, then copying here for full testing
<li>The exam grader is generally less picky about output whitespace than the Websheet grader.
</ul>
We recommend doing this practice in a timed environment; give yourself 90 minutes.
"""

source_code = r"""
\[
/***********************************************************************
Christopher Moretti
cmoretti
P01A/P06

Read in list side and permutations of that size.
Determine the max cycle length of each permutation.
Compute and print the average max cycle length.

Requires StdIn, StdOut
***************************************************************************/

    // determine longest cycle to get own hat back
    public static int maxCycleLength(int[] arr) {
        int N = arr.length;
        int max = 0;       // max cycle length
        int cycle;         // current cycle length
        
        // for each person
        for (int i = 0; i < N; i++) {
            int j = i;
            cycle = 1; // minimal cycle has 1 person 

            // while person j doesn't have person i's hat
            while (arr[j] != i+1) {
                j = arr[j] - 1;  // new person j to look for
                cycle++;
            }
                        
            if (max < cycle) max = cycle;  // new longest cycle
        }

        // return longest cycle length
        return max;
    }
    
    public static void main(String[] args) {
        // the # of items in the permutation
        int N = StdIn.readInt();
 
        // space to hold permutation
        int[] arr = new int[N];

        // running sum for max cycle lengths
        int sum = 0;

        // how many derangements have we seen?
        int count = 0;
        
        // Read until there are no more permutations left on StdIn.
        while (!StdIn.isEmpty()) {
            // fill array
            for (int i = 0; i < N; i++) {
                arr[i] = StdIn.readInt();
            }

            // count it and find its max cycle length
            count++;
            sum += maxCycleLength(arr);
        }
        
        // compute and print average with the given format
        StdOut.println("Average max cycle length: " + (double) sum / count);
    }
]\
"""

tests = r"""
test("maxCycleLength", (Object)new int[]{3, 4, 1, 5, 2, 6});
test("maxCycleLength", (Object)new int[]{1, 3, 4, 5, 6, 2});
test("maxCycleLength", (Object)new int[]{3, 1, 4, 2, 6, 5});
test("maxCycleLength", (Object)new int[]{1, 2, 3, 4, 5, 6, 7, 8});
test("maxCycleLength", (Object)new int[]{8, 7, 6, 5, 4, 3, 2, 1});
test("maxCycleLength", (Object)new int[]{9, 8, 7, 6, 5, 4, 3, 2, 1});
test("maxCycleLength", (Object)new int[]{2, 3, 4, 5, 1});
test("maxCycleLength", (Object)new int[]{1});
test("maxCycleLength", (Object)new int[]{2, 1});
test("maxCycleLength", (Object)new int[]{1, 2});
testStdin = "9\n9 8 7 6 5 4 3 2 1\n3 7 6 9 8 2 1 5 4";
testMain();
testStdin = "6\n1 2 6 4 3 5\n6 1 5 4 3 2";
testMain();
testStdinURL = "http://www.cs.princeton.edu/~cos126/docs/data/Hats/5perms9.txt";
testMain();
testStdinURL = "http://www.cs.princeton.edu/~cos126/docs/data/Hats/1000perms15.txt";
testMain();
"""
