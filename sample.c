#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main ()
{
		int i=1;
		char str[]="Find me on RAM memory";
		while (i)
		{
			printf("%s \n", str);
			sleep(1);
			i++;
		}
		return (0);
	}

