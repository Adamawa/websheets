attempts_until_ref = 0

description = r"""
Create a member function <tt>string delEnd()</tt>
that deletes the last item in the list, and returns the
<tt>string</tt> it contained (its <tt>name</tt>).
<p>If the list is empty, return an empty string (<tt>""</tt>).
<p>Remember to deallocate the item removed from the list!
"""

lang = "C++"

source_code = r"""
\hide[
#include <iostream>
#include <string>
using namespace std;

// structure of items in list
struct Node {
   Node* next;  // each node knows "next" node
   string name; // and stores a value
   Node(string initialName);  // constructor for nodes
};

Node::Node(string initialName) {name = initialName; next = NULL;}

class MonkeyChain {
   public:
      MonkeyChain();
      void threeKongs();
      void printAll();
      void addStart(string newName);
      bool isEmpty();
      int size();
      string delEnd();
   private: 
      Node* first;
};

MonkeyChain::MonkeyChain() {first = NULL;}

// a demo to create a length-3 list
void MonkeyChain::threeKongs() {
   first = new Node("DK Sr.");
   first->next = new Node("DK");
   first->next->next = new Node("DK Jr.");
}

// we'll provide a working copy of printAll for you 
void MonkeyChain::printAll() {
   // one possible approach: use a while loop
   Node* current = first; // start at beginning

   // if current isn't past the last node,
   while (current != NULL) {
      // print current node's name; then repeat loop w/next one
      cout << current->name << endl;
      current = current->next;
   }
}

// add a new node, containing this name, at the start of the list
void MonkeyChain::addStart(string newName) {
   Node* newFirst = new Node(newName);
   Node* oldFirst = first;
   first = newFirst;
   first->next = oldFirst;
   // there's also a slightly trickier 2-line solution
}

// add a new node, containing this name, at the start of the list
bool MonkeyChain::isEmpty() {
   return first == NULL;
}


int MonkeyChain::size() {
   int count = 0;
   Node* loc = first;
   while (loc != NULL) {
      count++;
      loc = loc->next;
   }
   return count;
}
]\

string MonkeyChain::delEnd() {
\[
   if (first == NULL) 
      return "";
   else if (first->next == NULL) {
      string result = first->name;
      delete first;
      first = NULL;
      return result;
   }
   else {
      Node* curr = first;
      // find node holding the last node
      while (curr->next->next != NULL)
         curr = curr->next;
      string result = curr->next->name;
      delete curr->next;
      curr->next = NULL;
      return result;
   }   
]\
}

int main() {
   MonkeyChain mc;
   mc.threeKongs();
   mc.addStart("Bubbles");
   cout << "Deleted: " << mc.delEnd() << endl;
   mc.printAll(); cout << endl;
   cout << "Deleted: " << mc.delEnd() << endl;
   mc.printAll(); cout << endl;
   cout << "Deleted: " << mc.delEnd() << endl;
   cout << boolalpha << mc.isEmpty() << endl;
   mc.printAll(); cout << endl;
   cout << "Deleted: " << mc.delEnd() << endl;
   cout << boolalpha << mc.isEmpty() << endl;

   // deleting from empty should do nothing:
   cout << "Deleted: " << mc.delEnd() << endl;
   cout << boolalpha << mc.isEmpty() << endl;

   // test your deallocation
   for (int i=0; i<1000000; i++) {
      mc.addStart("A");
      mc.addStart("B");
      mc.delEnd();
      mc.delEnd();
   }
}

"""

tests = [["", []]]

