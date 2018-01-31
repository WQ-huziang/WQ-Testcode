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

// Node struct
struct Node
{
    u_char index;
    u_char strlistindex;
    short sumvalue;
    string str;
	Node *father;
	
	Node(u_char _index, u_char _strlistindex,
  	 short _sumvalue, string _str, Node *_father = NULL) {
		index = _index;
		strlistindex = _strlistindex;
		sumvalue = _sumvalue;
		str = _str;
		father = _father;
	}

	// deep copy
	Node operator=(const Node &n) {
		index = n.index;
		strlistindex = n.strlistindex;
		sumvalue = n.sumvalue;
		str = n.str;
		father = n.father;
		return *this;
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


int n, k;              // the length of origin string, the size of substring array
string originstr;      // origin string
string ministr[200];   // string's substring
int value[200];        // string's value
Node *null;            // replace NULL
Node *maxnode;         // max sum value node

// get input numbers	
void getInput(FILE *fin) {
	char str[33];
	fscanf(fin, "%d %d\n", &n, &k);
	fscanf(fin, "%s\n", str);
	originstr = str;
	for (int i = 0; i < k; ++i) {
		fscanf(fin, "%s %d\n", str, (value + i));
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
		printf("%d %s\n", temp->index, ministr[temp->strlistindex].c_str());
	}
	printf("%d\n", maxnode->sumvalue);
}

// BFS
void BFS() {
	int nums = 0;
	ofstream fp("err");

	priority_queue<Node*, vector<Node*>, less<Node*> > bfsqueue;
	set<Node*, NodeCompare> store;

	// add the begin node at first
	bfsqueue.push(null);
	cout << "originstr:" << originstr << endl;

	// bfs
	while (!bfsqueue.empty()) {
		Node *temp = bfsqueue.top();
		bfsqueue.pop();
		
		for (int i = 0; i < k; i++) {
			int index = temp->str.find(ministr[i], 0);
			// cout << temp->str << ' ' << ministr[i] << endl;
			// cout << "index:" << index << ' ' << string::npos << endl;
			// cout << (index != int(string::npos)) << endl;

			while (index != int(string::npos)) {
				Node *newnode = new Node(index, i, temp->sumvalue + value[i], temp->str, temp);
				newnode->str.erase(index, ministr[i].length());

				// if the node has appear, jump


				auto it = store.find(newnode);
				fp << "NUMS:" << ++nums << endl;
				fp << "INSET?" << (it != store.end()) << endl;
				if (it != store.end()) {
					if (newnode->sumvalue > (*it)->sumvalue)
						*(*it) = *newnode;
				} else {
					fp << "Values:" << newnode->sumvalue << endl;
					fp << "String:" << newnode->str << endl;
					fp << "Father:" << newnode->father->str << endl;

					// add new appear node
					if (temp->str != "")
						bfsqueue.push(newnode);
				}		

				if (newnode->sumvalue > maxnode->sumvalue)		
					maxnode = newnode;

				// reflesh index
				index = temp->str.find(ministr[i], index + 1);
			}
		}
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
	null = new Node(0, 0, 0, originstr);
	maxnode = null;

	BFS();

	printOutput(fout);

	fclose(fin);
	fclose(fout);

	return 0;
}