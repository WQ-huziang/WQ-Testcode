#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>
#include <queue>
#include <set>
#include <iterator>
#include <fstream>
using namespace std;

struct Node
{
	int a;

	bool operator < (const Node &n1) const {
		return this->a > n1.a;
	}

	Node(int _a = 0) : a(_a) {}

	Node operator=(const Node &n) {
		a = n.a;
		return *this;
	}
};

struct Compare
{
	bool operator () (const Node *n1, const Node *n2) {
		return n1->a > n2->a;
	}
};

int main() {
	// set<Node*, Compare> myset;
	// Node *temp1 = new Node(0);
	// Node *temp2 = new Node(0);
	// myset.insert(temp1);
	// cout << (myset.find(temp2) != myset.end()) << (temp1 == temp2) << endl;

	string a, b;
	ifstream fin("in");
	fin >> a >> b;
	printf("%s\n%s\n", )

	// string a = "aa";
	// string b = "aa";
	// cout << a.find(b, 0) << endl;
	// int c = a.find(b, 1) ;
	// cout << a.find(b, 1) << ' ' << c << endl;

	// int a, b;
	// string s;
	// ifstream fin("in");
	// fin >> a >> b;
	// fin >> s;
	// cout << "s:" << s << endl;


	// vector<int> vec;
	// vec.push_back(1);

	// vector<int>::iterator it = vec.begin();
	// cout << (it != vec.begin()) << endl;


	// priority_queue<Node*,vector<Node*>, less<Node*>> que;
	// Node *temp1 = new Node(0);
	// Node *temp2 = new Node(1);
	// Node *temp3 = new Node(2);

	// que.push(temp1);
	// que.push(temp2);
	// que.push(temp3);

	// cout << que.top()->a << endl;

	// return 0;

	// Node no[10];
	// for (int i = 0; i < 10; ++i)
	// {
	// 	no[i].a = i;
	// }

	// sort(no, no + 10);

	// for (int i = 0; i < 10; ++i)
	// {
	// 	cout << no[i].a << ' ';
	// }

	// queue<int*> que;
	// vector<int> vec;
	// int a = 1;
	// vec.push_back(a);
	// que.push(&(vec[0]));
	// int *aa = que.front();
	// *aa = 2;
	// cout << vec[0];
}
