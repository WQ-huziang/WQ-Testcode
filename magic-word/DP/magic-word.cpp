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

// dp[i, j] means the substr(i, j)'s value
// F(x, y) = 0, x == y
//         = max (for k:1->n) 
//          (if (ministr[k] conpare [x, i), [j, y):
//               if (F(i, j) == -1)  return -1
//               else  return F(i, j) + value[k])
short dpfull[33][33];   

// dp[i, j] means the index (
)
int dpnotfull[33][33];

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
	// stack<Node*> outsta;
	// Node *temp = maxnode;
	// while (temp != null) {
	// 	outsta.push(temp);
	// 	temp = temp->father;
	// }
	// while (!outsta.empty()) {
	// 	temp = outsta.top();
	// 	outsta.pop();
	// 	fprintf(fout, "%d %s\n", temp->index, ministr[temp->strlistindex].c_str());
	// }
	// fprintf(fout, "%d\n", maxnode->calculateSumValue());
}

// judge whether is suitable
bool isHalfSubstr(int x, int y, int index, int split) {
	int rightlength = ministr[index].length() - split;
	return originstr.substr(x, split) == ministr[index].substr(0, split)
		&& originstr.substr(y - rightlength, rightlength) ==
		ministr[index].substr(split, rightlength);
}

// DPfull, calculate the value dpfull
void DPfull() {
	// get the ministring length
	int minstrlength = 32;
	for (int i = 0; i < k; ++i)
		if (minstrlength < ministr[i].length())  minstrlength = ministr[i].length();

	// reset
	for (int i = 0; i < n; i++)
		for (int j = 0; j < n; j++)  dpfull[i][j] = -1;

	// if (i == j): F(i, j) = 0
	for (int i = 0; i < n; ++i)
		dpfull[i][i] = 0;
	
	// if originstr[i, j) is ministr[k]: F(i, j) = value[k]
	for (int i = 0; i < k; ++i) {
		int index = originstr.find(ministr[i], 0);
		while (index != int(string::npos)) {
			dpfull[index][index + ministr[i].length()] = value[i];
			index = originstr.find(ministr[i], index + 1);
		}
	}

	// F (i, j) = max (for i : 1 -> k)
	//           (if (ministr[k] fit [x, i), [j, y):
	//                if (F(i, j) == -1)  return -1
	//                else  return F(i, j) + value[k])
	for (int x = 0; x < n; ++x) {
		for (int l = minstrlength; l < n - x; ++l) {
			int y = x + l;
			
			for (int i = 0; i < k; ++i) {
				// if remain string's length is less than ministr, continue
				if (ministr[i].length() > l)  continue;
				for (int s = 0; s <= ministr[i].length(); ++s) {
					int r = ministr[i].length() - s;
					
					// if fit [x, x + s), [y - r, y)
					// if [x + s, r - y) has string
					// if dpfull[x + s][y - r] + value[i] > dpfull[]
					if (isHalfSubstr(x, y, i, s)
						&& dpfull[x + s][y - r] != -1)
						dpfull[x][y] = max(dpfull[x + s][y - r] + value[i], dpfull[x][y]); 
					else  continue;
				}
			}
		}
	}

	return;
}

// DPnotfull, calculater the value dpnotfull
void DPnotFull() {

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
	//null = new Node(0, 0, originstr);
	//maxnode = null;



	DPfull();

	printOutput(fout);

	fclose(fin);
	//fclose(fout);

	return 0;
}