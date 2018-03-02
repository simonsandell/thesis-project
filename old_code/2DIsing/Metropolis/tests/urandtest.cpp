#include <unistd.h>
#include <sys/syscall.h>
#include <linux/random.h>

int main() {
  unsigned long int s;
  syscall(SYS_getrandom, &s, sizeof(unsigned long int), 0);
  std::cout << "The seed is: " << s << "." << std::endl;
}
