import unittest
import generator
import string
import random
import sys

class GeneratorTest(unittest.TestCase):
    '''Test case for generator.py'''
    def setUp(self):
        self.bases = ['A', 'T', 'C', 'G']
        self.invalid_bases = [chr(x) for x in range(0,255 + 1) if string.upper(chr(x)) not in self.bases]
        self.haplotype_length = 100

    def test_generate_haplotype_zero_size(self):
        haplotype = generator.generate_haplotype(0, generator.ModificationType.NONE)
        self.assertIsNone(haplotype)

    def test_generate_haplotype_negative_size(self):
        negative_sizes = [random.randint(-(sys.maxint) - 1,0) for x in range(0,1000)]
        for negative_size in negative_sizes:
            haplotype = generator.generate_haplotype(negative_size, generator.ModificationType.NONE)
            self.assertIsNone(haplotype)

    def test_generate_haplotype_inexistent_modification_kind(self):
        haplotype = generator.generate_haplotype(self.haplotype_length, "XPTO")
        self.assertIsNone(haplotype)
        haplotype = generator.generate_haplotype(self.haplotype_length, -1)
        self.assertIsNone(haplotype)
        haplotype = generator.generate_haplotype(self.haplotype_length, None)
        self.assertIsNone(haplotype)
        haplotype = generator.generate_haplotype(self.haplotype_length, True)
        self.assertIsNone(haplotype)

    def test_generate_haplotype_normal(self):
        haplotype = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        self.assertIsNotNone(haplotype)
        for character in self.invalid_bases:
            self.assertNotIn(character, haplotype)
        for base in haplotype:
            self.assertIn(base, self.bases)

    def test_generate_haplotype_mutation(self):
        haplotype_original = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        haplotype = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.MUTATION, haplotype_original)
        self.assertIsNotNone(haplotype)
        self.assertNotEqual(haplotype, haplotype_original)
        for character in self.invalid_bases:
            self.assertNotIn(character, haplotype)
        for base in haplotype:
            self.assertIn(base, self.bases)

    def test_generate_haplotype_mutation_incomplete(self):
        haplotype_original = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        haplotype = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.MUTATION)
        self.assertIsNone(haplotype)

    def test_generate_haplotype_mutation_excedent(self):
        haplotype_original = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        haplotype = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.MUTATION, haplotype_original, haplotype_original)
        self.assertIsNone(haplotype)

    def test_generate_haplotype_recombination(self):
        haplotype_original_one = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        haplotype_original_other = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        while haplotype_original_one == haplotype_original_other:
            haplotype_original_other = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.NONE)
        haplotype = generator.generate_haplotype(self.haplotype_length, generator.ModificationType.RECOMBINATION, haplotype_original_one, haplotype_original_other)
        self.assertIsNotNone(haplotype)
        self.assertNotEqual(haplotype, haplotype_original_one)
        self.assertNotEqual(haplotype, haplotype_original_other)
        for character in self.invalid_bases:
            self.assertNotIn(character, haplotype)
        for base in haplotype:
            self.assertIn(base, self.bases)

    def test_generate_haplotypes(self):
        haplotype_length = random.randint(1,500)
        total_length = random.randint(1,1000)
        mutation_rate = random.random()
        recombination_rate = 1.0 - mutation_rate
        original, mutated_list, recombinant_list = generator.generate_haplotypes(haplotype_length, total_length, mutation_rate, recombination_rate)
        self.assertIsNotNone(original)
        self.assertIsNotNone(mutated_list)
        self.assertIsNotNone(recombinant_list)


if __name__ == '__main__':
    unittest.main()
