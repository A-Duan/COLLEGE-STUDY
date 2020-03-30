/* 
Problem: turn hex into oct ;
method: first turn hex into binary, and then turn binary into oct, because the test example limits max 100000 digit,
so i decide use string to store. 

Q1:What the relation between hex and oct?
A1:A hex number is made of 4 digit binary numbers, and a oct number is made of 3 digit binary numbers, so that means i 
have to first turn hex into binary, and divide 4 digit binary into 3 digit. Last turn binary into oct.

Q2:How to turn 3 digit binary numbers into oct?
A2:number 7's binary is 111, so i can use & symbol to save last three numbers. The last number i use plus '0' and turn into char, 
the result is oct, and save the result in a string. At last i shift right binary number and do circulation.

*/
 

#include <iostream>
#include <string>
#include <math.h>
using namespace std;

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main(int argc, char *argv[]) {
	int n=0;
	cin>> n;
		
	string* Hex = new string[n];
	string tmpOct;
	string* Oct = new string[n];
	
	for(int i=0;i<n;i++)
	{
		int CurBit = 0;
		cin>>Hex[i];
		
		tmpOct = "";
		Oct[i] = "";
		
		for(int j=Hex[i].size()-3;j>=0;j-=3)
		{
			int d = 0;
			for(int k=0;k<3;k++)//74 DF5 545
			{
				int t = j+k;
				// 16 To 10
				if(Hex[i][t]>='0' && Hex[i][t]<='9')
				{
					CurBit = Hex[i][t]-'0';
				}
				if(Hex[i][t]>='A' && Hex[i][t]<='F')
				{
					CurBit = Hex[i][t]-'A'+10;	
				}
				
				d = d * 16 + CurBit;//5//5*16+15//(5*16+15)*16+4
			}
			
			// 3bit hex to 4bit oct
			int base = 7; // 111B
			for(int k=0;k<4;k++)
			{
				tmpOct += (char)('0' + (d & base));
				d = d >> 3; 
			}
			d = 0;
		} 
		
		// last less three
		int rest = Hex[i].size() % 3;
		if(rest != 0)
		{
			int d = 0;
			for(int k=0;k<rest;k++)
			{
				// 16 To 10
				if(Hex[i][k]>='0' && Hex[i][k]<='9')
				{
					CurBit = Hex[i][k]-'0';
				}
				if(Hex[i][k]>='A' && Hex[i][k]<='F')
				{
					CurBit = Hex[i][k]-'A'+10;	
				}
				
				d = d * 16 + CurBit;
			}
			
			int base = 7; // 111B
			int max = ceil(4.0 / 3.0 * rest);
			// 1bit hex = 4/3 bit oct
			for(int k=0;k<max;k++)
			{
				if(((k==max-1) && (d & base)!=0) || k<max-1)
					tmpOct += char('0' + (d & base));
				d = d >> 3;
			}
		}
		
		int j=tmpOct.size()-1;
		// turn order
		
		bool t = 0;
		 
		for(;j>=0;j--)
		{
			if (t == 0 && tmpOct[j] == '0')		//remove the first '0'
			{
				t++;
				continue;
			}
			Oct[i] += tmpOct[j];
		}
	}
	
	for(int i=0;i<n;i++)
	{
		cout<<Oct[i]<<endl;
	}
	
	return 0;
}

