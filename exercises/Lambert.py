source_code = r"""

// evaluate Lambert's W function at x. Assumes x >= 0.
public static double W(double x) {
   // we know that W(x) >= 0 and W(x) <= max(1, ln(x))
   double lo = 0;
  \[double hi = Math.max(1, Math.log(x));]\

   // continue until search endpoints differ by 1E-8 or less
   while (\[hi - lo >= 1E-8]\) {
      // evaluate midpoint times e^midpoint
\[
      double mid = (lo + hi) / 2;
      double midval = mid * Math.exp(mid);
]\

      // if this value is smaller than x, search above, else search below
\[
      if (midval < x)
         lo = mid;
      else
         hi = mid;
]\
   }
   return lo; // return some point in final range
}

public static void main(String[] args) {
   double x = Double.parseDouble(args[0]);
   StdOut.println(W(x));
}
"""

description = r"""
<i>Lambert's W function</i> is a mathematical function
with a <a href="https://cs.uwaterloo.ca/research/tr/1993/03/W.pdf">diverse
range of applications in math and science</a>. It is an inverse function
to $x = w \times \mathrm{e}^w$. In other words, for a given $x$, the value
of the Lambert function $W(x)$ is defined as the real number satisfying
$$x = W(x) \times \mathrm{e}^{W(x)}.$$

<p>
For example, <i>W</i>(126) is approximately 3.5651 since 126 = 3.5651 &times; e<sup>3.5651</sup>.

<p>
Use binary search to define a static method <tt>W(double x)</tt> that 
evaluates the Lambert function at <i>x</i>. You may assume $x \ge 0$. 
To help get the binary search
started, you may use the fact that $0 \le W(x) \le \max(1, \ln(x))$.
Terminate the binary search when 
the search endpoints differ by 10<sup>-8</sup> or less.
"""

tests = r"""
testMain(126);
testMain(2.718281828459045);
testMain(23423.348);
testMain("1E25");
testMain("1E-5");
"""
