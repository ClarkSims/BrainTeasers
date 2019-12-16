// g++ -std=c++14 -O4 -o time_slots time_slots.cpp
#define UNITTEST 0

#if UNITTEST
#include <gtest/gtest.h>
#endif

#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>

using namespace std;

struct counter {
  int _bin_number;
  int _in_bin;
  int _updated;
  int _cumulative_count_lt;
};

struct update {
  int _bin_number;
  int _count;
};

struct time_slots {
  int _num_bin;
  std::vector<update> _updates;
  std::vector<counter> _counters;
  std::map<int, int> _binary_key_to_counter_offset;
  std::unordered_map<int, int> _key_to_counter_offset;
  int _sum_count = 0;
  int _min_bin_number = 0;
  int _max_bin_number = 0;

  time_slots(int num_bin) : _num_bin(num_bin) {}

  pair<int, int> initialize_from_neighbor(int bin_number) {
    if (_binary_key_to_counter_offset.empty()) {
      return pair<int, int>(0, 0);
    }
    auto poff = _binary_key_to_counter_offset.lower_bound(bin_number);
    if (poff == _binary_key_to_counter_offset.end()) {
      // finish this
    } else {
      // and this
    }
    return pair<int, int>(0, 0);
  }

  void add_update(int bin_number, int count) {
    if (_updates.empty()) {
      _min_bin_number = _max_bin_number = bin_number;
    } else {
      if (bin_number < _min_bin_number) {
        _min_bin_number = bin_number;
      } else if (bin_number > _max_bin_number) {
        _max_bin_number = bin_number;
      }
    }
    _updates.push_back(update{bin_number, count});
    int updated, cumulative_count_lt;
    tie(updated, cumulative_count_lt) = initialize_from_neighbor(bin_number);
    auto pnt = _key_to_counter_offset.find(bin_number);
    if (pnt == _key_to_counter_offset.end()) {
      int updated, cumulative_count_lt;
      tie(updated, cumulative_count_lt) = initialize_from_neighbor(bin_number);
      _counters.push_back(
          counter{bin_number, count, updated, cumulative_count_lt});
      int off = _counters.size() - 1;
      auto element = pair<int, int>(bin_number, off);
      _binary_key_to_counter_offset.insert(element);
      _key_to_counter_offset.insert(element);
    } else {
      int off = pnt->second;
      _counters[off]._in_bin += count;
    }
    _sum_count += count;
  }

  int brute_force_query(int lhs, int rhs) {
    int count = 0;
    for (size_t off = 0; off < _updates.size(); ++off) {
      if (_updates[off]._bin_number >= lhs &&
          _updates[off]._bin_number <= rhs) {
        count += _updates[off]._count;
      }
    }
    return count;
  }

  void update_counter_at_offset(int off) {
    int bin_number = _counters[off]._bin_number;
    int last_update = _counters[off]._updated;
    for (size_t i = last_update; i < _updates.size(); ++i) {
      if (_updates[i]._bin_number < bin_number) {
        _counters[off]._cumulative_count_lt += _updates[i]._count;
      }
    }
    _counters[off]._updated = _updates.size();
  }

  int total_less_than_bin_key(int bin_number) {
    if (bin_number < _min_bin_number) {
      return 0;
    }
    if (bin_number > _max_bin_number) {
      return _sum_count;
    }
    auto pnt_hash = _key_to_counter_offset.find(bin_number);
    if (pnt_hash != _key_to_counter_offset.end()) {
      update_counter_at_offset(pnt_hash->second);
      return _counters[pnt_hash->second]._cumulative_count_lt;
    }
    auto pnt_binary = _binary_key_to_counter_offset.upper_bound(bin_number);
    update_counter_at_offset(pnt_binary->second);
    return _counters[pnt_binary->second]._cumulative_count_lt;
  }

  int total_including_bin_key(int bin_number) {
    if (bin_number < _min_bin_number) {
      return 0;
    }
    if (bin_number >= _max_bin_number) {
      return _sum_count;
    }
    auto pnt_hash = _key_to_counter_offset.find(bin_number);
    if (pnt_hash != _key_to_counter_offset.end()) {
      update_counter_at_offset(pnt_hash->second);
      return _counters[pnt_hash->second]._cumulative_count_lt +
             _counters[pnt_hash->second]._in_bin;
    }
    auto pnt_binary = _binary_key_to_counter_offset.upper_bound(bin_number);
    update_counter_at_offset(pnt_binary->second);
    return _counters[pnt_binary->second]._cumulative_count_lt;
  }

  int query(int lhs, int rhs) {
    if (_counters.empty()) {
      return 0;
    }
    return total_including_bin_key(rhs) - total_less_than_bin_key(lhs);
  }
};

#if UNITTEST

TEST(simple_test, first) {
  time_slots ts(4);
  ts.add_update(0, 1);
  ts.add_update(1, 1);
  ts.add_update(2, 1);
  int output;
  output = ts.brute_force_query(1, 2);
  EXPECT_EQ(2, output);
  output = ts.query(1, 2);
  EXPECT_EQ(2, output);
  ts.add_update(1, 1);
  output = ts.brute_force_query(1, 3);
  EXPECT_EQ(3, output);
  output = ts.query(1, 3);
  EXPECT_EQ(3, output);
}

TEST(stress_test, second) {
  int num_test = 100;
  for (int i = 0; i < num_test; ++i) {
    // for (int i = 36; i < 37; ++i) {
    srand(i);
    int num_bins = rand() % 100 + 1;
    time_slots ts(num_bins);
    int num_inserts = rand() % 1000 + 1;
    for (int j = 0; j < num_inserts; ++j) {
      int bin_number = rand() % num_bins;
      int increment = rand() % 10 + 1;
      ts.add_update(bin_number, increment);
    }
    int lhs = rand() % num_bins;
    int rhs = rand() % num_bins;
    if (lhs > rhs) {
      std::swap(lhs, rhs);
    }
    int expected = ts.brute_force_query(lhs, rhs);
    int output = ts.query(lhs, rhs);
    if (expected != output) {
      cerr << "problem at i = " << i << endl;
    }
    ASSERT_EQ(expected, output);
  }
}

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

#else

int main() {
  int num_slots;
  scanf("%d", &num_slots);
  time_slots ts(num_slots);
  char command;
  int i1, i2, count;
  while (scanf("%c %d %d", &command, &i1, &i2)) {
    if (command == 'd') {
      ts.add_update(i1, i2);
      printf("-\n");
    } else if (command == 'q') {
      count = ts.query(i1, i2);
      printf("%d\n", count);
    }
  }
}

#endif
