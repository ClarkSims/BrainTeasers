// g++ -std=c++14 -g -o stub stub.cpp -l gtest -l pthread
#include <algorithm>
#include <iostream>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#define WITH_GTEST 0

#if WITH_GTEST
#include <gtest/gtest.h>
#endif

using namespace std;

template <class T> struct goldfish_brain {
  int _N;
  vector<int> _circular_queue;
  map<int, int> _vals_to_population;
  unordered_map<int, map<int, int>::iterator> _cache;
  int _off = 0;
  int _not_updated = 0;
  int _max_worm_size = 0;
  T &_data;

  goldfish_brain(T &data, int N) : _data(data), _N(N), _circular_queue(N, 0),
  _not_updated(0) {}

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

  void optimized_order_N_remember_worm(int worm_size) {
    int dest = _off % _N;
    if (_off >= _N) {
      int dest = _off % _N;
      ++_off;
      int leaving = _circular_queue[dest];
      _circular_queue[dest] = worm_size;
      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      } else if (leaving == _max_worm_size) {
        _max_worm_size =
            *max_element(&_circular_queue[0], &_circular_queue[_N]);
      }
    } else {
      _circular_queue[_off] = worm_size;
      ++_off;
      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      }
    }
  }

  bool optimized_order_N_eat_worm() {
    int worm_size;
    if (_data.next(worm_size)) {
      optimized_order_N_remember_worm(worm_size);
      return true;
    }
    return false;
  }

  void add_val_to_population(int worm_size) {
    auto pnt = _vals_to_population.find(worm_size);
    if (pnt != _vals_to_population.end()) {
      ++pnt->second;
    } else {
      _vals_to_population.insert(pair<int, int>(worm_size, 1));
    }
  }

  void decrement_val_in_population(int leaving) {
    auto pnt = _vals_to_population.find(leaving);
    if (pnt == _vals_to_population.end()) {
      throw runtime_error("map out of sync");
    }
    if (pnt->second == 1) {
      _vals_to_population.erase(pnt);
    } else {
      --pnt->second;
    }
  }

  void order_log_N_remember_worm(int worm_size) {
    if (_off >= _N) {
      int dest = _off % _N;
      ++_off;
      int leaving = _circular_queue[dest];
      _circular_queue[dest] = worm_size;
      decrement_val_in_population(leaving);
      add_val_to_population(worm_size);

      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      } else if (leaving == _max_worm_size) {
        _max_worm_size = _vals_to_population.rbegin()->first;
      }
    } else {
      _circular_queue[_off] = worm_size;
      ++_off;
      add_val_to_population(worm_size);
      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      }
    }
  }

  bool order_log_N_eat_worm() {
    int worm_size;
    if (_data.next(worm_size)) {
      order_log_N_remember_worm(worm_size);
      return true;
    }
    return false;
  }

  void lazy_update_order_log_N_remember_worm(int worm_size) {
    if (_off >= _N) {
      int dest = _off % _N;
      ++_off;
      int leaving = _circular_queue[dest];
      //if (leaving == worm_size) {
        //return;
      //}
      if (!_vals_to_population.empty()) {
        decrement_val_in_population(leaving);
      }
      _circular_queue[dest] = worm_size;

      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      } else if (leaving == _max_worm_size) {

        // add all the values we skipped
        if (_not_updated < (_off - _N)) {
          _not_updated = (_off - _N);
        }
        for (; _not_updated < _off; ++_not_updated) {
          dest = _not_updated % _N;
          add_val_to_population(_circular_queue[dest]);
        }
        _max_worm_size = _vals_to_population.rbegin()->first;
      }
    } else {
      _circular_queue[_off] = worm_size;
      ++_off;
      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      }
    }
  }

  bool lazy_update_order_log_N_eat_worm() {
    int worm_size;
    if (_data.next(worm_size)) {
      lazy_update_order_log_N_remember_worm(worm_size);
      return true;
    }
    return false;
  }


  void add_val_to_population_with_cache(int worm_size) {
    unordered_map<int, map<int, int>::iterator>::iterator pcache;
    map<int, int>::iterator pnt;

    pcache = _cache.find(worm_size);
    if (pcache == _cache.end()) {
      pnt = _vals_to_population.insert(pair<int, int>(worm_size, 1)).first;
      _cache[worm_size] = pnt;
    } else {
      pnt = pcache->second;
      ++pnt->second;
    }
  }

  void decrement_val_in_population_with_cache(int leaving) {
    unordered_map<int, map<int, int>::iterator>::iterator pcache;
    map<int, int>::iterator pnt;

    pcache = _cache.find(leaving);
    pnt = pcache->second;

    if (pnt->second == 1) {
      _vals_to_population.erase(pnt);
      _cache.erase(pcache);
    } else {
      --pnt->second;
    }
  }

  void order_log_N_remember_worm_with_cache(int worm_size) {
    if (_off >= _N) {
      int dest = _off % _N;
      ++_off;
      int leaving = _circular_queue[dest];
      _circular_queue[dest] = worm_size;
      decrement_val_in_population_with_cache(leaving);
      add_val_to_population_with_cache(worm_size);

      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      } else if (leaving == _max_worm_size) {
        _max_worm_size = _vals_to_population.rbegin()->first;
      }
    } else {
      _circular_queue[_off] = worm_size;
      ++_off;
      add_val_to_population_with_cache(worm_size);
      if (worm_size > _max_worm_size) {
        _max_worm_size = worm_size;
      }
    }
  }

  bool order_log_N_eat_worm_with_cache() {
    int worm_size;
    if (_data.next(worm_size)) {
      order_log_N_remember_worm_with_cache(worm_size);
      return true;
    }
    return false;
  }
};

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

TEST(optimized_order_N, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.optimized_order_N_eat_worm()) {
    //    cout << off << " " << data[off] << " " << expected[off] << " " <<
    //    brain._max_worm_size << endl;
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}

TEST(order_log_n, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.order_log_N_eat_worm()) {
    // cout << off << " " << data[off] << " " << expected[off] << " " <<
    // brain._max_worm_size << endl;
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}

TEST(lazy_update_order_log_N, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.lazy_update_order_log_N_eat_worm()) {
    // cout << off << " " << data[off] << " " << expected[off] << " " <<
    // brain._max_worm_size << endl;
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}


TEST(order_log_N_eat_worm_with_cache, denis) {
  vector<int> data{1, 2, 4, 3, 2, 1, 1};
  vector<int> expected{1, 2, 4, 4, 4, 4, 3};
  get_next_from_vector input(data);
  int length_memory = 4;
  goldfish_brain<get_next_from_vector> brain(input, length_memory);

  int off = 0;
  while (brain.order_log_N_eat_worm_with_cache()) {
    // cout << off << " " << data[off] << " " << expected[off] << " " <<
    // brain._max_worm_size << endl;
    ASSERT_EQ(expected[off], brain._max_worm_size);
    off += 1;
  }
}

TEST(optimized_order_N, big_random) {
  for (int i = 0; i < 100; ++i) {
    srand(i);
    int L = 2 + rand() % 1000;
    int N = 1 + rand() % (L - 1);
    vector<int> data(L);
    for (size_t j = 0; j < data.size(); ++j) {
      data[j] = rand() % 10;
    }
    get_next_from_vector input1(data), input2(data);
    goldfish_brain<get_next_from_vector> brain1(input1, N), brain2(input2, N);
    while (brain1.brute_force_eat_worm()) {
      ASSERT_TRUE(brain2.optimized_order_N_eat_worm());
      ASSERT_EQ(brain1._max_worm_size, brain2._max_worm_size);
    }
  }
}

TEST(order_log_n, big_random) {
  for (int i = 0; i < 100; ++i) {
    srand(i);
    int L = 2 + rand() % 1000;
    int N = 1 + rand() % (L - 1);
    vector<int> data(L);
    for (size_t j = 0; j < data.size(); ++j) {
      data[j] = rand() % 10;
    }
    get_next_from_vector input1(data), input2(data);
    goldfish_brain<get_next_from_vector> brain1(input1, N), brain2(input2, N);
    while (brain1.brute_force_eat_worm()) {
      ASSERT_TRUE(brain2.order_log_N_eat_worm());
      ASSERT_EQ(brain1._max_worm_size, brain2._max_worm_size);
    }
  }
}

TEST(lazy_update_order_log_N, big_random) {
  for (int i = 0; i < 100; ++i) {
    srand(i);
    //cerr << "test number " << i << endl;
    int L = 2 + rand() % 1000;
    int N = 1 + rand() % (L - 1);
    vector<int> data(L);
    for (size_t j = 0; j < data.size(); ++j) {
      data[j] = rand() % 10;
    }
    get_next_from_vector input1(data), input2(data);
    goldfish_brain<get_next_from_vector> brain1(input1, N), brain2(input2, N);
    while (brain1.brute_force_eat_worm()) {
      //cerr << "brain1_off = " << brain1._off << endl;
      //print_container(std::cerr, brain1._circular_queue) << endl;
      //if (brain1._off==1) {
        //cerr << "trouble" << endl;
      //}
      ASSERT_TRUE(brain2.lazy_update_order_log_N_eat_worm());
      //print_container(std::cerr, brain2._circular_queue) << endl;
      //print_key_val_container(std::cerr, brain2._vals_to_population) << endl;
#if 0
      int pop = 0;
      for (auto pnt = brain2._vals_to_population.begin();
        pnt != brain2._vals_to_population.end() ; ++pnt)
      {
        pop += pnt->second;
      }
      ASSERT_LE(pop, N);
      //cerr << "brain2._not_updated" << brain2._not_updated << endl;
      int begin = brain2._off - N;
      if (begin < 0) {
        begin = 0;
      }
      int dupe_pop = brain2._not_updated - begin;
      if (dupe_pop < 0) {
        dupe_pop = 0;
      }
      //cerr << "pop = " << pop << "" << "dupe_pop = " << dupe_pop << endl;
      ASSERT_EQ(pop, dupe_pop);
#endif
      ASSERT_EQ(brain1._max_worm_size, brain2._max_worm_size);
    }
  }
}


TEST(order_log_N_eat_worm_with_cache, big_random) {
  for (int i = 0; i < 100; ++i) {
    srand(i);
    int L = 2 + rand() % 1000;
    int N = 1 + rand() % (L - 1);
    vector<int> data(L);
    for (size_t j = 0; j < data.size(); ++j) {
      data[j] = rand() % 10;
    }
    get_next_from_vector input1(data), input2(data);
    goldfish_brain<get_next_from_vector> brain1(input1, N), brain2(input2, N);
    while (brain1.brute_force_eat_worm()) {
      ASSERT_TRUE(brain2.order_log_N_eat_worm_with_cache());
      ASSERT_EQ(brain1._max_worm_size, brain2._max_worm_size);
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