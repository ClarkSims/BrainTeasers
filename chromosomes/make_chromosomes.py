#!/usr/bin/env python3
import unittest
import bisect
import sys
import heapq
import math
import string
import random
from typing import List


class string_key:
    hash_alpha = [hash(c) for c in string.ascii_uppercase]
    off_a = ord('A')

    def __init__(self, key_string, N=-1):
        if N == -1:
            N = len(key_string)
        elif N > len(key_string):
            s.checksum = 0
            return

        self.key_string = key_string
        self.checksum = 0
        for i in range(N):
            c = key_string[i]
            offset = ord(c) - self.off_a
            self.checksum += self.hash_alpha[offset]

    def recalc(self, newchar, oldchar):
        offset = ord(oldchar) - self.off_a
        self.checksum -= self.hash_alpha[offset]
        offset = ord(newchar) - self.off_a
        self.checksum += self.hash_alpha[offset]

    def __eq__(self, other):
        if self is other:
            return True
        return self.checksum == other.checksum
        # if self.checksum != other.checksum:
        #    return False
        # return self.fingerprint == other.fingerprint


class Solution:
    def findAnagrams(self, chromosome: str, gene: str) -> List[int]:
        len_gene = len(gene)
        len_chromosome = len(chromosome)
        if len_chromosome < len_gene:
            return []
        if len_chromosome == len_gene:
            if chromosome == gene:
                return [0]
            else:
                return []
        gene_string_key = string_key(gene)
        chromosome_string_key = string_key(chromosome, len_gene)
        if chromosome_string_key == gene_string_key:
            rv = [0]
        else:
            rv = []
        for newoff in range(len_gene, len_chromosome):
            oldoff = newoff - len_gene
            newchar = chromosome[newoff]
            oldchar = chromosome[oldoff]
            chromosome_string_key.recalc(newchar, oldchar)
            if chromosome_string_key == gene_string_key:
                rv.append(oldoff + 1)
        return rv

    def findAnagramsNoOverlap(self, chromosome: str, gene: str) -> List[int]:
        with_overlap = self.findAnagrams(chromosome, gene)
        if len(with_overlap) == 0:
            return []
        len_gene = len(gene)
        without_overlap = [with_overlap[0]]
        iprev = 0
        for i in range(1, len(with_overlap)):
            dist = with_overlap[i] - iprev
            if dist >= len_gene:
                without_overlap.append(with_overlap[i])
                iprev = i
        return without_overlap

    def findNumAnagramsNoOverlap(self, chromosome: str, gene: str) -> int:
        without_overlap = self.findAnagramsNoOverlap(chromosome, gene)
        return len(without_overlap)

    def findNumAnagrams(self, chromosome: str, gene: str) -> int:
        len_gene = len(gene)
        len_chromosome = len(chromosome)
        if len_chromosome < len_gene:
            return 0
        if len_chromosome == len_gene:
            if chromosome == gene:
                return 1
            else:
                return 0
        gene_string_key = string_key(gene)
        chromosome_string_key = string_key(chromosome, len_gene)
        if chromosome_string_key == gene_string_key:
            rv = 1
        else:
            rv = 0
        for newoff in range(len_gene, len_chromosome):
            oldoff = newoff - len_gene
            newchar = chromosome[newoff]
            oldchar = chromosome[oldoff]
            chromosome_string_key.recalc(newchar, oldchar)
            if chromosome_string_key == gene_string_key:
                rv += 1
        return rv

        return 0


class TestAllAnagrams(unittest.TestCase):
    def test1(self):
        sol = Solution()
        s = "CBAEBABACD"
        p = "ABC"
        output = sol.findAnagrams(s, p)
        expected = [0, 6]
        self.assertEqual(expected, output)
        output = sol.findNumAnagrams(s, p)
        expected = 2
        self.assertEqual(expected, output)

    def test2(self):
        sol = Solution()
        s = "AGAG"
        p = "AG"
        output = sol.findAnagrams(s, p)
        expected = [0, 1, 2]
        self.assertEqual(expected, output)

        output = sol.findAnagramsNoOverlap(s, p)
        expected = [0, 2]
        self.assertEqual(expected, output)

        output = sol.findNumAnagrams(s, p)
        expected = 3
        self.assertEqual(expected, output)

        output = sol.findNumAnagramsNoOverlap(s, p)
        expected = 2
        self.assertEqual(expected, output)

    def test3(self):
        sol = Solution()
        s = "AB"
        p = "AB"
        output = sol.findAnagrams(s, p)
        expected = [0]
        self.assertEqual(expected, output)
        output = sol.findNumAnagrams(s, p)
        expected = 1
        self.assertEqual(expected, output)

    def test4(self):
        sol = Solution()
        s = "A"
        p = "AB"
        output = sol.findAnagrams(s, p)
        expected = []
        self.assertEqual(expected, output)
        output = sol.findNumAnagrams(s, p)
        expected = 0
        self.assertEqual(expected, output)


NUCLEOTIDES = 'AGCTU'


def random_string(gene_length: int) -> str:
    return "".join(random.choice(NUCLEOTIDES) for _ in range(gene_length))


def mutate_gene(gene: str) -> str:
    return "".join(random.sample(gene, len(gene)))


def random_chromosome(gene: str, min_num_occur: int, max_space: int) -> str:
    rng = range(max_space // 2, max_space)
    chromosome = random_string(random.choice(rng))
    for _ in range(min_num_occur):
        chromosome += mutate_gene(gene)
        chromosome += random_string(random.choice(rng))
    return chromosome


if __name__ == '__main__':
    #unittest.main()
    sol = Solution()
    gene = 'AG'
    print(gene)
    fcount = open('short_count.txt', 'w')
    foffset = open('short_offset.txt', 'w')
    command = ['./find_gene', gene]
    for j in range(5):
        chromosome = random_chromosome(gene, j + 2, 10)
        numoccur = sol.findNumAnagrams(chromosome, gene)
        offsets = sol.findAnagrams(chromosome, gene)
        print("    {} {}".format(chromosome, numoccur))
        print("       {}".format(offsets))
        fname_chromosome = 'short_chromosome_{}.txt'.format(j)
        command.append(fname_chromosome)
        fchromo = open(fname_chromosome, 'w')
        fchromo.write(chromosome)
        fchromo.close()
        print(numoccur, file=fcount)
        stroffsets = [str(off) for off in offsets]
        print(", ".join(stroffsets), file=foffset)
    fcount.close()
    foffset.close()
    print(" ".join(command))

    gene = random_string(8)
    print(gene)
    fcount = open('medium_count.txt', 'w')
    foffset = open('medium_offset.txt', 'w')
    command = ['./find_gene', gene]
    for j in range(5):
        chromosome = random_chromosome(gene, j + 2, 10)
        numoccur = sol.findNumAnagrams(chromosome, gene)
        offsets = sol.findAnagrams(chromosome, gene)
        print("    {} {}".format(chromosome, numoccur))
        print("       {}".format(offsets))
        fname_chromosome = 'medium_chromosome_{}.txt'.format(j)
        command.append(fname_chromosome)
        fchromo = open(fname_chromosome, 'w')
        fchromo.write(chromosome)
        fchromo.close()
        print(numoccur, file=fcount)
        stroffsets = [str(off) for off in offsets]
        print(", ".join(stroffsets), file=foffset)
    fcount.close()
    foffset.close()
    print(" ".join(command))
