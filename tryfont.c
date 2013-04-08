// Quick C program to test out generated font.
//
// echo 'The lazy developer something something...' | tryfont > test.pbm

#include <stdio.h>

#include "newfont.h"

// Gets the location of a character in |font| using a step size of 5.
int get_char_start(unsigned char c) {
  return c * 5 + offset[c];
}

// Each column is printed as a row of 0s and 1s, plus a trailing 0.
// This converts neatly to a Portable Bit Map. Simply add:
// P1
// 9 N
// to the start of the file, where N is the number of rows.
void print(int start, int width) {
  for (int i = start; i < start + width; ++i) {
    unsigned char c = font[i];
    for (int b = 7; b >= 0; --b) {
      putchar(c & (1 << b) ? '1' : '0');
      putchar(' ');
    }
    printf("0\n");
  }
}

void print_gap() {
  printf("0 0 0 0 0 0 0 0 0\n");
}

void print_char(unsigned char c) {
  int start = get_char_start(c);
  int width = get_char_start(c+1) - start;
  print(start, width);
}

void print_input() {
  int c;
  print_gap();
  while((c = getchar()) != EOF) {
    print_char((unsigned char) c);
    print_gap();
  }
}

void print_all() {
  print_gap();
  for (int c = 0; c < 256; ++c) {
    print_char((unsigned char) c);
    print_gap();
  }
}

int main(int argc, char *argv[]) {

  print_input();

  //print_all();

  return 0;
}
