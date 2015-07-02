description = r"""
<b>You have to solve the <a href='javascript:websheets.load("java/11-classes/Clicker")'>Clicker</a> websheet before this one will work.</b> 
<p>
Write a program <tt>CountingSort</tt>, a client of <tt><a href="javascript:websheets.load('java/11-classes/Clicker')">Clicker</a></tt>, 
that sorts a list of single-digit numbers.
On standard input, you will get a list of numbers like
<pre>
0 2 4 3 2 2 9 8 1 0
</pre>
Your program should use an array of ten <tt>Clicker</tt> objects to keep track of how many of each digit you saw. At the end, print out each number the number of times it was seen, in this case it would be
<pre>
0 0 1 2 2 2 3 4 8 9
</pre>
Remember that <tt>Clicker</tt> has the following API:
<ul>
<li><tt>public Clicker()&nbsp; // constructor, make new clicker with value 0</tt>
<li><tt>public void inc() // add one to the current value</tt>
<li><tt>public void dec() // subtract one from the current value</tt>
<li><tt>public int curr() // return the current value</tt>
</ul>
"""

source_code = r"""
public static void main(String[] args) {
   Clicker[] counts = \[new Clicker[10];]\ // array of Clickers

   // initialize them all
\[
   for (int i=0; i<10; i++) {
      counts[i] = new Clicker(); // initialize one
   }
]\

   // read each digit
   while (!StdIn.isEmpty()) {
      int digit = StdIn.readInt();
      // increment the right clicker
\[
      counts[digit].inc();
]\
   }

   // print out each number once for each time it was seen
   for (int i=0; i<10; i++) {
      while (counts[i].curr() > 0) {
         StdOut.print(i+" ");
         counts[i].dec();
      }
   }
   StdOut.println();
}
"""

dependencies = ["java/11-classes/Clicker"]

tests = r"""
stdin = "0 2 4 3 2 2 9 8 1 0";
testMain();
stdin = "6";
testMain();
stdin = "3 4 5 5 5 4 3 4 4 5 3 4 3 5 4";
testMain();
stdin = "0 1 3 6 0 0 7 4 3 5 6 7 8 7 4 3 2 2 3 4 5 6 8 9 8 5 1 1 1 1 2 2 3 6 8 7 9 0 0 5";
testMain();
"""
