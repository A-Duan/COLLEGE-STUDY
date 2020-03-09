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
I cube an integer, and I get a floating-point number after cube root extraction, then I coerce the floating-point number to an integer.
Why I haven't get the original integer (the second and third lines of output)? Do you know how to answer it? Thank you!
*/


/*
answer:
The result come from cube root extraction is not exactly the actual value. For example, 125 cubic root extract into 5, but the floating-point
number in computer is not exactly 5, it's always have some error and it's mabey turn out to be 4.999999992432423225667 at last. So when we do
coerce turning the result will become 4.
*/
