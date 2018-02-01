#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <bitset>
#include <queue>
#include <set>
#include <stack>
using namespace std;

int n, k;              // the length of origin string, the size of substring array
string originstr;      // origin string
string ministr[200];   // string's substring
short value[200];      // string's value

// Node struct
struct Node
{
    u_char index;
    u_char strlistindex;
    string str;
	Node *father;
	
	Node(u_char _index, u_char _strlistindex,
  	 string _str, Node *_father = NULL) {
		index = _index;
		strlistindex = _strlistindex;
		str = _str;
		father = _father;
	}

	// deep copy
	Node operator=(const Node &n) {
		index = n.index;
		strlistindex = n.strlistindex;
		str = n.str;
		father = n.father;
		return *this;
	}

	short calculateSumValue() {
		short sumvalue = 0;
		Node *temp = this;
		while (temp->father != NULL) {
			sumvalue += value[temp->strlistindex];
			temp = temp->father;
		}
		return sumvalue;
	}

	// compare function, in order to use priority_queue
	bool operator < (const Node &n1) {
		return this->str < n1.str;
	}
};

// node compare class
struct NodeCompare {
	bool operator () (const Node *n1, const Node *n2) {
		return n1->str < n2->str;
	}
};

Node *null;            // replace NULL
Node *maxnode;         // max sum value node

// get input numbers	
void getInput(FILE *fin) {
	char str[33];
	fscanf(fin, "%d %d\n", &n, &k);
	fscanf(fin, "%s\n", str);
	originstr = str;
	for (int i = 0; i < k; ++i) {
		fscanf(fin, "%s %hd\n", str, value + i);
		ministr[i] = str;
	}
}

// output answer
void printOutput(FILE *fout) {
	// output
	stack<Node*> outsta;
	Node *temp = maxnode;
	while (temp != null) {
		outsta.push(temp);
		temp = temp->father;
	}
	while (!outsta.empty()) {
		temp = outsta.top();
		outsta.pop();
		fprintf(fout, "%d %s\n", temp->index, ministr[temp->strlistindex].c_str());
	}
	fprintf(fout, "%d\n", maxnode->calculateSumValue());
}

// BFS
void BFS() {
	queue<Node*> bfsqueue;
	set<Node*, NodeCompare> store;

	// add the begin node at first
	bfsqueue.push(null);
	store.insert(null);

	// bfs
	while (!bfsqueue.empty()) {
		Node *temp = bfsqueue.front();
		bfsqueue.pop();
		
		for (int i = 0; i < k; i++) {
			int index = temp->str.find(ministr[i], 0);

			while (index != int(string::npos)) {
				Node *newnode = new Node(index, i, temp->str, temp);
				newnode->str.erase(index, ministr[i].length());
				
				// if the node has appear, jump
				auto it = store.find(newnode);
				if (it != store.end()) {
					if (newnode->calculateSumValue() > (*it)->calculateSumValue())
						*(*it) = *newnode;
				} else {
					// add new appear node
					store.insert(newnode);
					bfsqueue.push(newnode);
				}
					
				// reflesh index
				index = temp->str.find(ministr[i], index + 1);
			}
		}
	}

	// find max value
	for (Node* i : store) {
		if (i->calculateSumValue() > maxnode->calculateSumValue())
			maxnode = i;
	}
}

int main(int argc, char const *argv[])
{
	// check arg number
	if (argc != 3) {
		printf("The input arguments need to be 2!\n");
		exit(0);
	}

	FILE *fin = fopen(argv[1], "r");
	FILE *fout = fopen(argv[2], "w");
	
	getInput(fin);

	// replace NULL
	null = new Node(0, 0, originstr);
	maxnode = null;

	BFS();

	printOutput(fout);

	fclose(fin);
	fclose(fout);

	return 0;
}