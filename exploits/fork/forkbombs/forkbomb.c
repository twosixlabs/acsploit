#include <unistd.h>

int main(void)
{
    while(1) {
      fork(); /* malloc can be used in order to increase the data usage */
    }
}
