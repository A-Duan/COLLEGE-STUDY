/*
Problem Description: Given a string s, find the longest palindrome substring in s. 
You can assume that the longest length of s is 1000.
*/
#include<iostream>
#include<vector>
#include<string>
using namespace std;
int expendaroundcenter(string &s,int left,int right)
{
	int L = left;
	int R = right;
	while(L>=0 && R<=s.length() && s[R] == s[L])
	{
		--L;
		++R;
	}
	return R-L-1;
}

string SearchSubstr(string s)
{
	int len = s.size();
	if(len == 0)
		return s;
	int start = 0;//record the initial position of the substring
	int end = 0;//record the end position of the substring
	int mlen = 0;//recond the max length of the substring
	for(int i = 0;i < len;++i)
	{
		int len1 = expendaroundcenter(s,i,i);	//deal with the string with length is odd number
		int len2 = expendaroundcenter(s,i,i+1);	//deal with the string with length is even number
		mlen = max(max(len1,len2),mlen);
		if(mlen > end - start +1)
		{
			start = i - (mlen - 1)/2;
			end = i + mlen/2;
		}
	}
	return s.substr(start,mlen);
}

int main()
{
	string s,substr;
	cin>>s;
	substr = SearchSubstr(s);
	cout<<substr<<endl;
	return 0;
		
 } 
