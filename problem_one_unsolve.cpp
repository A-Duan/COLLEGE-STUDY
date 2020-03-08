#include<iostream>
#include<math.h>
int main()
{
	int sum = 0;
	for(int j = 3;j < 6;++j)
	{
		sum = pow(j,3);
		double temp = pow(sum,1.0/3);
		printf("sum = %d,temp = %f,temp = %d\n",sum,temp,(int)temp); 
	}
}
/*
Problem Description:
I cube an integer, and I get a floating-point number after cubic expansion, then I coerce the floating-point number to an integer.
Why I haven't get the original integer (the second and third lines of output)? Do you know how to answer it? Thank you!
*/
