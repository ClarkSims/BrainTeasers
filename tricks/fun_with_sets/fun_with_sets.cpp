//g++ -std=c++14 -g -o fun_with_sets fun_with_sets.cpp
#include <stdio.h>
#include <string.h>

using namespace std;

#include <cmath>

struct datum {
  const char *key;
  unsigned offset;
  unsigned count;
  datum *next;
};

#define LARGE_PRIME 48779
#define MAX_OFFSET 1048576
static_assert(MAX_OFFSET % LARGE_PRIME != 0);

unsigned calc_hash(const char* str) {
  unsigned rv = 0;
  while (*str) {
    rv *=  LARGE_PRIME;
    rv += *str;
    ++str;
  }
  rv %= MAX_OFFSET;
  return rv;
}

datum data[MAX_OFFSET];
datum* bins[MAX_OFFSET];
int num_data = 0;

datum* add_word(const char ** argv, unsigned off) {
  unsigned hash = calc_hash(argv[off]);
  datum* pnode = bins[hash], *prev_pnode = nullptr;

  // search through bin for new key
  while (pnode != nullptr) {
    if (strcmp(pnode->key, argv[off]) == 0) {
      // key found, so return node
      ++pnode->count;
      return pnode;
    }
    prev_pnode = pnode;
    pnode = pnode->next;
  }

  // key not found, create node
  pnode = &data[num_data];
  ++num_data;
  pnode->key = argv[off];
  pnode->count = 1;
  pnode->offset = off;

  // add node to end of list, or make head if list empty
  if (prev_pnode == nullptr) {
    bins[hash] = pnode;
  } else {
    prev_pnode->next = pnode;
  }
  return pnode;
}

void set_diff(int argc, const char **argv) {
  datum *pdata;
  for (int rgc = 1; rgc < argc; ++rgc) {
    if (argv[rgc][0] == '-' && strcmp(argv[rgc], "--") == 0) {
      argv[rgc] = nullptr;
    } else {
      pdata = add_word(argv, rgc);
      if (pdata->count > 1) {
        argv[pdata->offset] = nullptr;
        argv[rgc] = nullptr;
      }
    }
  }
}

int print_set_diff(int argc, const char*argv[]) {
  set_diff(argc, argv);
  bool first = true;
  for (int off=1; off<argc; ++off) {
    if (argv[off] != nullptr) {
      if (first) {
        first = false;
      } else {
        printf(" ");
      }
      printf("%s", argv[off]);
    }
  }
  printf("\n");
}

#if 0
int main() {
  const char *argv[5] = {"", "1", "2", "3", "2"};
  print_set_diff(5, argv);
}
#else

int main(int argc, const char*argv[]) {
  print_set_diff(argc, argv);
}
#endif
