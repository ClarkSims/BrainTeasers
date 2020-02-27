#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <unordered_map>
#include <stdexcept>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

#define NDEBUG

struct my_list_node {
    int key;
    int val;
    my_list_node* next = nullptr;
    my_list_node* prev = nullptr;
};

class LRUCache {
    int _capacity;
    int _size = 0;
    unordered_map<int,my_list_node*> _kv_store;
    my_list_node* _head = nullptr;
    my_list_node* _tail = nullptr;
    my_list_node* _free_head = nullptr;
    vector<my_list_node> _pool;

public:
    LRUCache(int capacity) :
        _capacity( capacity),
        _pool( capacity)
    {
        if (_capacity) {
            _free_head = &_pool[0];
            _free_head->prev = nullptr;
            for (int i=0; i<_capacity-1; ++i) {
                _pool[i].next = &_pool[i+1];
                _pool[i+1].prev = &_pool[i];
            }
            _pool[_capacity-1].next = nullptr;
        }
    }

    void put(int key, int val) {
        my_list_node* nd = _find_node(key);

        if (nd) { // node in cache
            nd->val = val;
            if (nd != _head) {
                _unlink_node(nd);
                _link_as_head(nd);
            }
        } else { // not in cache
            if (_size == _capacity) {
                _kv_store.erase(_tail->key);
                _remove_tail();
            }
            _push(key, val);
        }
    }

    // return val if in cache, else -1
    int get(int key) {
        my_list_node* nd = _find_node(key);
        if (nd == nullptr) {
            return -1;
        } else {
            if (nd != _head) {
                _unlink_node(nd);
                _link_as_head(nd);
            }
        }
        return nd->val;
    }

    my_list_node* _find_node(int key) {
        auto p_kv = _kv_store.find(key);
        if (p_kv != _kv_store.end()) {
            return p_kv->second;
        } else {
            return nullptr;
        }
    }

    void _link_as_head(my_list_node *nd) {
        if (_head) {
            _head->prev = nd;
        }
        // remove nd from free list
        if (nd->prev) {
            nd->prev = nd->next;
        }
        if (nd->next) {
            nd->next = nd->prev;
        }
        nd->next = _head;
        _head = nd;
    }

    void _make_head(my_list_node *nd) {
        _link_as_head(nd);
        ++_size;
        if (_size == _capacity) {
            _free_head = nullptr;
        }
    }

    void _unlink_internal_node(my_list_node *nd) {
        nd->prev->next = nd->next;
        nd->next->prev = nd->prev;
    }

#ifndef NDEBUG
#define CHECK(EX) if (!(EX)) { cerr << "!"#EX << " at " << line << endl; throw std::logic_error("!"#EX);};
#else
#define CHECK(EX)
#endif

    int length_of_list(my_list_node* hd) {
        int ln=0;
        while (hd) {
            ++ln;
            hd = hd->next;
        }
        return ln;
    }

    const char * check_list_integrity(my_list_node* hd) {
#define chk(EX) if (!(EX)) { return "!"#EX; }
        chk (hd->prev == nullptr);
        my_list_node* prev = nullptr;
        while (hd != nullptr && hd->next != nullptr) {
            chk(hd->prev == prev);
            prev = hd;
            hd = hd->next;
            if (hd==nullptr) break;
        }
        return nullptr;
#undef chk
    }

    void check(int line) {
        int free_size = _capacity - _size;
        const char* err;
        int ln;
        if (free_size) {
            CHECK(_free_head != nullptr);
            ln = length_of_list(_free_head);
            CHECK( free_size == ln);
            err = check_list_integrity(_free_head);
            if (err) {
                cerr << err << " at " << line << endl;
                throw std::logic_error(err);
            }
        } else {
            CHECK(_free_head == nullptr);
        }
        ln = length_of_list(_head);
        CHECK(ln == _size);
        if (_size > 0) {
            err = check_list_integrity(_head);
            my_list_node *actual_tail = _head;
            while (actual_tail != nullptr && actual_tail->next != nullptr) {
                actual_tail = actual_tail->next;
            }
            CHECK(_tail == actual_tail);
        } else {
            CHECK(_head == nullptr);
            CHECK(_tail == nullptr);
        }
        if (_size != _kv_store.size()) {
            cerr << "_size = "<< _size << endl;
            cerr << "_kv_store.size() = " << _kv_store.size() << endl;
        }
        CHECK(_size == _kv_store.size());
    }

    void _unlink_node(my_list_node *nd) {
        if (nd == _tail) {
            _unlink_tail();
        } else {
            _unlink_internal_node(nd);
        }
    }

    void _remove_node(my_list_node *nd) {
        assert(nd != _head);
        _kv_store.erase(nd->val);
    }

    void _unlink_tail() {
        if (_tail->prev) {
            _tail->prev->next = nullptr;
            _tail = _tail->prev;
        }
    }

    void _remove_tail() {
        assert(_tail != nullptr);
        assert(_size > 0);
        assert(_free_head == nullptr || _size < _capacity);
        --_size;
        if (_head == _tail) _head = nullptr;
        if (_free_head) {
            _free_head->next = _free_head;
        }
        _free_head = _tail;
        if (_tail->prev) {
            _tail->prev->next = nullptr;
            _tail = _tail->prev;
        }
        _free_head->next = _free_head->prev = nullptr;
    }

    // push to beginning of cache
    void _push(int key, int val) {
        assert(_size < _capacity);  // must have room for one more
        my_list_node* new_node = _free_head;
        _free_head = _free_head->next;
        if (_free_head) {
            _free_head->prev = nullptr;
        }
        if (_head) {
            new_node->next = _head;
            _head->prev = new_node;
            _head = new_node;
        } else {
            new_node->prev = new_node->next = nullptr;
            _head = _tail = new_node;
        }
        _kv_store[key] = new_node;
        new_node->key = key;
        new_node->val = val;
        ++_size;
    }
};



//https://github.com/google/googletest/blob/master/googletest/docs/primer.md
TEST(LRUCache, test_empty) {
    ASSERT_NO_THROW( LRUCache c(0) );
}

TEST(LRUCache, test_push1) {
    LRUCache c5(5);
    c5.check(__LINE__);
    c5.put(1, 1);
    c5.check(__LINE__);
    ASSERT_EQ(1, c5.get(1));
    c5.check(__LINE__);

    LRUCache c1(1);
    c1.check(__LINE__);
    c1.put(1, 1);
    c1.check(__LINE__);
    ASSERT_EQ(1, c1.get(1));
    c1.check(__LINE__);
    c1.put(2, 2);
    c1.check(__LINE__);
    ASSERT_EQ(2, c1.get(2));
    c1.check(__LINE__);
    ASSERT_EQ(-1, c1.get(1));
    c1.check(__LINE__);
    ASSERT_EQ(2, c1.get(2));
    c1.check(__LINE__);
}

TEST(LRUCache, test_push2) {
    LRUCache c5(5);
    c5.check(__LINE__);
    c5.put(1, 1);
    c5.check(__LINE__);
    c5.put(2, 2);
    c5.check(__LINE__);
    ASSERT_EQ(1, c5.get(1));
    c5.check(__LINE__);
    ASSERT_EQ(2, c5.get(2));
    c5.check(__LINE__);

    LRUCache c2(2);
    c2.check(__LINE__);
    c2.put(1, 1);
    c2.check(__LINE__);
    c2.put(2, 2);
    c2.check(__LINE__);
    ASSERT_EQ(1, c2.get(1));
    c2.check(__LINE__);
    ASSERT_EQ(2, c2.get(2));
    c2.check(__LINE__);
}

TEST(LRUCache, test_push3) {
    LRUCache c5(5);
    c5.check(__LINE__);
    c5.put(1, 1);
    c5.check(__LINE__);
    c5.put(2, 2);
    c5.check(__LINE__);
    c5.put(3, 3);
    c5.check(__LINE__);
    ASSERT_EQ(1, c5.get(1));
    c5.check(__LINE__);
    ASSERT_EQ(2, c5.get(2));
    c5.check(__LINE__);
    ASSERT_EQ(3, c5.get(3));
    c5.check(__LINE__);

    LRUCache c3(3);
    c3.check(__LINE__);
    c3.put(1, 1);
    c3.check(__LINE__);
    c3.put(2, 2);
    c3.check(__LINE__);
    ASSERT_EQ(1, c3.get(1));
    c3.check(__LINE__);
    ASSERT_EQ(2, c3.get(2));
    c3.check(__LINE__);
}

TEST(LRUCache, leetcode) {
    LRUCache c2(2);
    c2.check(__LINE__);
    c2.put(1, 1);
    c2.check(__LINE__);
    c2.put(2, 2);
    c2.check(__LINE__);

    c2.put(1, 1);
    c2.check(__LINE__);
    c2.put(2, 2);
    c2.check(__LINE__);
    ASSERT_EQ(1, c2.get(1));       // returns 1
    c2.check(__LINE__);
    c2.put(3, 3);    // evicts key 2
    c2.check(__LINE__);
    ASSERT_EQ(-1, c2.get(2));       // returns -1 (not found)
    c2.check(__LINE__);
    c2.put(4, 4);    // evicts key 1
    c2.check(__LINE__);
    ASSERT_EQ(-1, c2.get(1));       // returns -1 (not found)
    c2.check(__LINE__);
    ASSERT_EQ(3, c2.get(3));       // returns 3
    c2.check(__LINE__);
    ASSERT_EQ(4, c2.get(4));       // returns 4
    c2.check(__LINE__);
}

int track;

TEST(LRUCache, random_shuffle) {
    int i, j, k, test;
    srand(0);

    for (i=1; i<100; ++i) {
        LRUCache c(i);
        for (j=0; j<i; ++j) {
            c.put(j, j);
            c.check(__LINE__);
        }
        for (k=0; k<100; ++k) {
            j = rand() % i;
            ++track;
            test = c.get(j);
            if (j != test) {
                cerr << "failure at track = " << track << endl;
            }
            ASSERT_EQ(j, c.get(j));
            c.check(__LINE__);
        }
    }
}

TEST(LRUCache, random_shuffle_and_rewrite) {
    static int track = 0;
    int i, j, k, test;
    srand(0);

    for (i=1; i<100; ++i) {
        LRUCache c(i);
        for (j=0; j<i; ++j) {
            c.put(j, j);
            c.check(__LINE__);
        }
        for (k=0; k<100; ++k) {
            j = rand() % i;
            c.put(j, j*j);
            ++track;
        }

         for (j=0; j<i; ++j) {
            c.put(j, j*j*j);
            c.check(__LINE__);
        }

        for (k=0; k<100; ++k) {
            j = rand() % i;
            test = c.get(j);
            ++track;
            if (j*j*j != test) {
                cerr << "failure at track = " << track << endl;
            }
            ASSERT_EQ(j*j*j, c.get(j));
            c.check(__LINE__);
        }
    }
}

void execute_cache_algo(FILE *infile, FILE *outfile) {
    bool first = true;
    string line;
    int cache_size, key, value;
    Cache *cache = NULL;
    while (getline(infile, line)) {
        if (first) {
            first = false;
            cache_size = atoi(line.c_str());
            cache = new Cache()
        } else {
            if (memcmp(line.c_str(), 'get', 3) == 0) {
                key = atoi(line.c_str() + 3);
            } else if (memcmp(line.c_str(), 'put', 3) == 0) {
                key = atoi(line.c_str() + 3);
                const char *pvalue = line.c_str() + line.size()
                while (*pvalue < 0 || *pvalue > 9) {
                    --pvalue;
                }
                while (*pvalue != ' ') {
                    --pvalue;
                }
                value = atoi(pvalue);
            }
        }
    }
}

void usage() {

}

int main(int argc, char **argv) {
    if (argc == 1) {
        execute_cache_algo(stdin, stdout);
    } else if (argc == 2) {
        if (strcmp(argv[1], 'test') == 0) {
            testing::InitGoogleTest(&argc, argv);
            return RUN_ALL_TESTS();
        }
    } else if (argc == 3) {
        input_fl = fopen(argv[1], 'r');
        output_fl = fopen(argv[2], 'w');
        execute_cache_algo(input_fl, output_fl);
    }

}
