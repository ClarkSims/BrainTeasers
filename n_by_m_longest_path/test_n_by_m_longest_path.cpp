#include <gtest/gtest.h>
#include "n_by_m_longest_path.h"
#include <csignal>


TEST(n_by_m_longest_path, test_creator) {
    double data[1] = { 1 };
    Matrix m( data, 1, 1);
    NbyMLongestPathSolver nlps;
    nlps._matrix = &m;
    Line answer;
    nlps.solveLongestColumn(answer);
}


TEST(n_by_m_longest_path, test_one) {
    double data[1] = { 1 };
    NbyMLongestPathSolver nlps( data, 1, 1);
    Line answer;
    nlps.solveLongestColumn(answer);
    EXPECT_EQ(1,answer._length);
}


TEST(n_by_m_longest_path, test_one_column_several_lengths) {
#define NROWS 10
    double data[NROWS];
    int i;
    for (i = 0; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        NbyMLongestPathSolver nlps( data, i, 1);
        Line answer;
        nlps.solveLongestColumn(answer);
        EXPECT_EQ(i,answer._length);
    }
#undef NROWS
}


TEST(n_by_m_longest_path, test_one_column_several_lengths_leading_zero) {
#define NROWS 10
    double data[NROWS];
    int i;
    data[0] = 0;
    for (i = 1; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        NbyMLongestPathSolver nlps( data, i, 1);
        Line answer;
        int expected_answer = (i > 0)? (i-1):0;
        nlps.solveLongestColumn(answer);
        EXPECT_EQ(expected_answer, answer._length);
    }
#undef NROWS
}

TEST(n_by_m_longest_path, test_one_column_several_lengths_trailing_zero) {
#define NROWS 10
    double data[NROWS];
    int i, j;
    for (i = 0; i < NROWS; ++i) {
        for (j = 0; j < NROWS; ++j) {
            data[j] = 1;
        }
        if (i>0) {
            data[i-1] = 0;
        }
        NbyMLongestPathSolver nlps( data, i, 1);
        Line answer;
        int expected_answer = (i > 0)? (i-1):0;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(expected_answer, answer._length);
    }
#undef NROWS
}


TEST(n_by_m_longest_path, test_one_row_several_lengths) {
#define NROWS 10
    double data[NROWS];
    int i;
    for (i = 0; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        NbyMLongestPathSolver nlps( data, 1, i);
        Line answer;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(i,answer._length);
    }
#undef NROWS
}

TEST(n_by_m_longest_path, test_one_row_several_lengths_leading_0) {
#define NROWS 10
    double data[NROWS];
    int i;
    data[0] = 0;
    for (i = 1; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        NbyMLongestPathSolver nlps( data, 1, i);
        Line answer;
        int expected_answer = (i > 0)? (i-1):0;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(expected_answer,answer._length);
    }
#undef NROWS
}

TEST(n_by_m_longest_path, test_one_row_several_lengths_trailing_zero) {
#define NROWS 10
    double data[NROWS];
    int i, j;
    for (i = 0; i < NROWS; ++i) {
        for (j = 0; j < NROWS; ++j) {
            data[j] = 1;
        }
        if (i>0) {
            data[i-1] = 0;
        }
        NbyMLongestPathSolver nlps( data, 1, i);
        Line answer;
        int expected_answer = (i > 0)? (i-1):0;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(expected_answer, answer._length);
    }
#undef NROWS
}
//        if (expected_answer == 1) raise(SIGINT);

TEST(n_by_m_longest_path, test_one_diagonal_positive_slope_several_lengths) {
#define NROWS 10
    double data[NROWS*NROWS];
    int i, stride;
    for (i = 0; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        memset( reinterpret_cast<void*>(data), 0, sizeof(data));
        for (stride=0; stride<i; ++stride) {
            data[stride + stride*i] = 1;
        }
        NbyMLongestPathSolver nlps( data, i, i);
        Line answer;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(i,answer._length);
    }
#undef NROWS
}

TEST(n_by_m_longest_path, test_one_diagonal_positive_slope_several_lengths_leading_0) {
#define NROWS 10
    double data[NROWS*NROWS];
    int i, stride;
    for (i = 0; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        memset( reinterpret_cast<void*>(data), 0, sizeof(data));
        for (stride=1; stride<i; ++stride) {
            data[stride + stride*i] = 1;
        }
        int expected_answer = (i > 0)? (i-1):0;
        NbyMLongestPathSolver nlps( data, i, i);
        Line answer;
        nlps.solveLongestRun(answer);
        EXPECT_EQ(expected_answer, answer._length);
    }
#undef NROWS
}

TEST(n_by_m_longest_path, test_off_center_diagonals_positive) {
    static int track = 0;
#define NROWS 10
    double data[NROWS*NROWS];
    int i, stride, offset;
    for (i = 0; i < NROWS; ++i) {
        data[i] = 1;
    }
    for (i = 0; i < NROWS; ++i) {
        for (offset=0; offset<i; ++offset) {
            memset( reinterpret_cast<void*>(data), 0, sizeof(data));
	    int expected_answer = 0;
            for (stride=offset; stride<i-offset; ++stride) {
                data[stride+offset + stride*i] = 1;
		++expected_answer;
            }
            NbyMLongestPathSolver nlps( data, i, i);
            Line answer;
            nlps.solveLongestRun(answer);
            EXPECT_EQ(expected_answer, answer._length);
            ++track;
        }
    }
    for (i = 0; i < NROWS; ++i) {
        for (offset=0; offset<i; ++offset) {
            memset( reinterpret_cast<void*>(data), 0, sizeof(data));
	    int expected_answer = 0;
            for (stride=0; stride<i-offset; ++stride) {
                data[stride + (stride + offset) *i] = 1;
		++expected_answer;
            }
            NbyMLongestPathSolver nlps( data, i, i);
            Line answer;
            if (track == 49) {
                int row, col;
                for (row=0; row<i; ++row) {
                    for (col=0; col<i; ++col) {
                        printf( "%lf ", data[row+col*i]);
                    }
                    printf( "\n");
                }
                printf( "trouble\n");
            }
            nlps.solveLongestRun(answer);
            if (expected_answer != answer._length) {
                printf( "fail at track=%d expected=%d answer=%d\n", track, expected_answer, answer._length);
                return;
            }
            EXPECT_EQ(expected_answer, answer._length);
            ++track;
        }
    }
#undef NROWS
}
int main(int argc, char **argv) {
	testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}

