#include <stdio.h>

const char* fizz = "Fizz";
const char* buzz = "Buzz";
const char* fizzbuzz = "FizzBuzz";

int main() {
int i = 1;

LOOP:
if (i % 15 == 0)
goto FIZZBUZZ;
if (i % 3 == 0)
goto FIZZ;
if (i % 5 == 0)
goto BUZZ;
printf("%d", i);
printf("\n");
goto STEP;

FIZZBUZZ:
printf(fizzbuzz);
printf("\n");
goto STEP;

FIZZ:
printf(fizz);
printf("\n");
goto STEP;

BUZZ:
printf(buzz);
printf("\n");

STEP:
i = i + 1;
if (i > 100) goto END;
goto LOOP;

END:
return 0;
}
