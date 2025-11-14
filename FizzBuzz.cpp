/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>

int main()
{
    for (int i = 1; i <= 100; i++){
        if (i % 15 == 0) {
            printf("FizzBuzz");
            printf("\n");
        }
        else if (i % 3 == 0){
            printf("Fizz");
            printf("\n");
        }
        else if (i % 5 == 0){
            printf("Buzz");
            printf("\n"); 
        }
        else{
            printf("%d", i);
            printf("\n");
        }
    }

    return 0;
}