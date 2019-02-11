g++ -g -I. -std=c++11 -c -o n_by_m_longest_path.o n_by_m_longest_path.cpp || exit 1
g++ -g -I. -std=c++11 -c -o test_n_by_m_longest_path.o test_n_by_m_longest_path.cpp || exit 1
g++ -g -o test_n_by_m_longest_path n_by_m_longest_path.o test_n_by_m_longest_path.o    /usr/lib/libgtest.a  -lpthread
