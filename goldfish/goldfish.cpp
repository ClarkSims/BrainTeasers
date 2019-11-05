// g++ -std=c++14 -g -o stub stub.cpp -l gtest -l pthread
#include <algorithm>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#define WITH_GTEST 1

#if WITH_GTEST
#include <gtest/gtest.h>
#endif

using namespace std;

template <class c> ostream &print_container(ostream &os, const c &cont) {
  for (auto pnt = cont.cbegin(); pnt != cont.cend(); ++pnt) {
    if (pnt != cont.cbegin()) {
      os << ", ";
    }
    os << *pnt;
  }
  return os;
}

template <class c> ostream &print_key_val_container(ostream &os, const c &cont) {
  for (auto pnt = cont.cbegin(); pnt != cont.cend(); ++pnt) {
    if (pnt != cont.cbegin()) {
      os << ", ";
    }
    os << "(" << pnt->first << ", " << pnt->second << ")";
  }
  return os;
}

template <class T> struct goldfish_brain {
  struct size_offset_t {
    int _size;
    int _offset;
    const bool operator<(const size_offset_t &rhs) const {
      if (this == &rhs)
        return false;
      if (_size > rhs._size) return false; // largest sizes are at top
      return -_offset < -rhs._offset;         // smallest offsets are at top
    }
  };

  int _N;
  vector<int> _circular_queue;
  map<int, int> _vals_to_population;
  set<size_offset_t> _increasing_cache;
  unordered_map<int, map<int, int>::iterator> _cache;
  int _off = 0;
  int _not_updated = 0;
  int _max_worm_size = 0;
  T &_data;

  goldfish_brain(T &data, int N)
      : _data(data), _N(N), _circular_queue(N, 0), _not_updated(0) {}

  void brute_force_remember_worm(int worm_size) {
    int dest = _off % _N;
    _circular_queue[dest] = worm_size;
    _off += 1;
    if (_off > _N) {
      _max_worm_size =
          *max_element(_circular_queue.begin(), _circular_queue.end());
    } else {
      _max_worm_size =
          *max_element(&_circular_queue[0], &_circular_queue[_off]);
    }
  }

  bool brute_force_eat_worm() {
    int worm_size;
    if (_data.next(worm_size)) {
      brute_force_remember_worm(worm_size);
      return true;
    }
    return false;
  }

  void order_log_n_remember_worm_increasing_cache(int worm_size) {
    // remove items that are too far back
    int leaving = _off - _N;
    while (!_increasing_cache.empty()) {
      auto point = std::prev(_increasing_cache.end());
      if (point->_offset <= leaving) {
        _increasing_cache.erase(point);
      } else {
        break;
      }
    }

    if (_increasing_cache.empty()) {
      _increasing_cache.insert(size_offset_t{worm_size, _off});
    } else if (worm_size < _increasing_cache.begin()->_size) {
      _increasing_cache.insert(size_offset_t{worm_size, _off});
    } else {
      size_offset_t newpoint{worm_size, _off};
      auto least_upper_bound = _increasing_cache.upper_bound(newpoint);
      _increasing_cache.erase(_increasing_cache.begin(), least_upper_bound);
      _increasing_cache.insert(_increasing_cache.begin(), newpoint);
    }
    _max_worm_size = _increasing_cache.rbegin()->_size;
    ++_off;
  }

  bool order_log_n_eat_worm_increasing_cache() {
    int worm_size;
    if (_data.next(worm_size)) {
      order_log_n_remember_worm_increasing_cache(worm_size);
      return true;
    }
    return false;
  }
};

struct get_next_from_vector {
  size_t _off = 0;
  vector<int> &_data;

  get_next_from_vector(vector<int> &data) : _data(data) {}

  bool next(int &datum) {
    if (_off < _data.size()) {
      datum = _data.at(_off);
      ++_off;
      return true;
    }
    return false;
  }
};

#if WITH_GTEST

struct random_datum {
  bool next (int& x) {
    x = rand();
    return true;
  }
};

TEST(integrity, increasing_cache) {
  int length_memory;
  random_datum input;
  for (int i = 0; i < 10; ++i) {
    for (int j = 0; j < 1000; ++j) {
      length_memory = rand() % 100 + 1;
      goldfish_brain<random_datum> brain(input, length_memory);
      brain.order_log_n_eat_worm_increasing_cache();
      auto pnt = brain._increasing_cache.begin();
      auto next = pnt;
      ++next;
      while (pnt != brain._increasing_cache.end() &&
             next != brain._increasing_cache.end()) {
        ASSERT_LT(pnt->_offset, next->_offset);
        ASSERT_GT(pnt->_size, next->_size);
      }
    }
  }
}

TEST(brute_force, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.brute_force_eat_worm()) {
    //    cout << off << " " << data[off] << " " << expected[off] << " " <<
    //    brain._max_worm_size << endl;
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}

TEST(order_log_n_eat_worm_increasing_cache, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.order_log_n_eat_worm_increasing_cache()) {
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}


TEST(order_log_n_remember_worm_increasing_cache, big_random) {
  for (int i = 0; i < 100; ++i) {
    //cout << "attempt " << i << endl;
    srand(i);
    int L = 2 + rand() % 1000;
    int N = 1 + rand() % (L - 1);
    vector<int> data(L);
    for (size_t j = 0; j < data.size(); ++j) {
      data[j] = rand() % 10;
    }
    get_next_from_vector input1(data), input2(data);
    goldfish_brain<get_next_from_vector> brain1(input1, N), brain2(input2, N);
    size_t off = 0;
    while (brain1.brute_force_eat_worm()) {
      //cout << off << " " << data[off] << " " << brain1._max_worm_size << " " <<
      //     brain2._max_worm_size << endl;
      ++off;
      ASSERT_TRUE(brain2.order_log_n_eat_worm_increasing_cache());
      ASSERT_EQ(brain1._max_worm_size, brain2._max_worm_size);
      //if (off == 63) {
        //cout << "trouble" << endl;
      //}
    }
  }
}

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

#else

struct read_int_stdin {
  int _max;
  int _number = 0;

  read_int_stdin( int amax): _max(amax) {}

  bool next(int & datum) {
    if (_number < _max) {
      scanf("%d", &datum);
      ++_number;
      return true;
    }
    return false;
  }
};

int main() {
  int N, L;
  scanf("%d %d", &L, &N);
  read_int_stdin input(N);
  goldfish_brain<read_int_stdin> brain(input, L);
  while (brain.order_log_N_eat_worm_with_cache()) {
    printf("%d\n", brain._max_worm_size);
  }
}
#endif
