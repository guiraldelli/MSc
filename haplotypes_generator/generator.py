import random
import math
import copy
import logging

logging.basicConfig()

bases = ['A', 'T', 'C', 'G']

class ModificationType:
    NONE = 0
    MUTATION = 1
    RECOMBINATION = 2


# TODO: should use the numpy.random.poisson() or numpy.random.binomial() for random numbers in mutation step.
def generate_haplotype(haplotype_length, modification_type, one_haplotype=None, other_haplotype=None):
    logger = logging.getLogger('generate.generate_haplotype')
    logger.setLevel(logging.INFO)
    # logger.debug('haplotype_length = %d; modification_type = %s', haplotype_length, modification_type)
    if haplotype_length > 0:
        if modification_type == ModificationType.NONE:
            return [random.sample(bases,1).pop() for base in range(0,haplotype_length)]
        elif modification_type == ModificationType.MUTATION:
            if one_haplotype != None and other_haplotype == None:
                haplotype_mutation = copy.deepcopy(one_haplotype)
                number_mutations = 0
                while number_mutations == 0:
                    number_mutations = int(math.ceil(random.expovariate(1)))
                while number_mutations > 0:
                    index_to_change = random.randint(0,len(haplotype_mutation) - 1)
                    haplotype_mutation[index_to_change] = random.sample(bases,1).pop()
                    while haplotype_mutation == one_haplotype:
                        haplotype_mutation[index_to_change] = random.sample(bases,1).pop()
                    number_mutations = number_mutations - 1
                return haplotype_mutation
            else:
                return None
        elif modification_type == ModificationType.RECOMBINATION:
            # logger.debug('modification_type == ModificationType.RECOMBINATION')
            if one_haplotype == None or other_haplotype == None:
                return None
            if len(one_haplotype) != len(other_haplotype):
                return None
            indexes = sorted([random.randint(0,len(one_haplotype) - 1) for i in range(0,2)])
            while indexes[1] - indexes[0] >= len(one_haplotype) or indexes[1] - indexes[0] <= 0:
                indexes = sorted([random.randint(0,len(one_haplotype) - 1) for i in range(0,2)])
            haplotype = None
            haplotype = copy.deepcopy(random.choice([one_haplotype, other_haplotype]))
            cutted_string = None
            cutted_string = [x for x in [one_haplotype, other_haplotype] if x != haplotype].pop()
            index = indexes[0]
            while index <= indexes[1]:
                haplotype[index] = cutted_string[index]
                index = index + 1
            # TODO: solve the code below without getting in infinite loop or returning None
            # if haplotype == one_haplotype or haplotype == other_haplotype:
            #     return None
                # haplotype = generate_haplotype(haplotype_length, modification_type, one_haplotype, other_haplotype)
            return haplotype
    else:
        return None

def generate_haplotypes(haplotype_length, total_number, mutation_rate=None, recombination_rate=None):
    logger = logging.getLogger('generate.generate_haplotypes')
    logger.setLevel(logging.INFO)
    logger.debug("haplotype_length = %d; total_number = %d; mutation_rate = %s; recombination_rate = %s", haplotype_length, total_number, mutation_rate, recombination_rate)
    original_haplotype = generate_haplotype(haplotype_length, ModificationType.NONE)
    mutated_haplotypes = list()
    recombinated_haplotypes = list()
    if mutation_rate == None:
        mutation_rate = 0.5
    else:
        pass
    if recombination_rate == None:
        recombination_rate = 0.5
    else:
        pass
    assert mutation_rate <= 1.0
    assert recombination_rate <= 1.0
    assert mutation_rate + recombination_rate <= 1.0
    mutation_quantity = int(round(mutation_rate * (total_number - 1)))
    recombination_quantity = int(round(recombination_rate * (total_number - 1)))
    if mutation_quantity + recombination_quantity + 1 != total_number:
        logger.warn("Number of haplotypes (mutated + recombinated + original) != total expected ---> " + str(mutation_quantity + recombination_quantity + 1) + " != " + str(total_number) + ".")
    assert mutation_quantity + recombination_quantity + 1 >= total_number + 1 or mutation_quantity + recombination_quantity + 1 <= total_number + 1, "%d != %d" % (mutation_quantity + recombination_quantity + 1, total_number)
    for i in range(0, mutation_quantity + recombination_quantity):
        logger.debug("Interaction #%d of %d", i, mutation_quantity + recombination_quantity - 1)
        mutated_haplotype = None
        recombinated_haplotype = None
        # generating a mutated haplotype
        logger.debug('generating a mutated haplotype')
        if len(mutated_haplotypes) <= mutation_quantity:
            while mutated_haplotype == None:
                mutated_haplotype = generate_haplotype(haplotype_length, ModificationType.MUTATION, random.choice(mutated_haplotypes + recombinated_haplotypes + [original_haplotype]))
        else:
            pass
        # adding mutated haplotype in the list of mutated haplotypes
        mutated_haplotypes.append(mutated_haplotype)
        # generating a recombinated haplotype
        logger.debug('generating a recombinated haplotype')
        if len(recombinated_haplotypes) <= recombination_quantity:
            assert len(mutated_haplotypes + recombinated_haplotypes + [original_haplotype]) > 1
            assert recombinated_haplotype == None
            while recombinated_haplotype == None:
                one_haplotype = random.choice([item for item in (mutated_haplotypes + recombinated_haplotypes + [original_haplotype]) if item != None])
                other_haplotype = random.choice([item for item in (mutated_haplotypes + recombinated_haplotypes + [original_haplotype]) if item != one_haplotype and item != None])
                assert one_haplotype != None
                assert other_haplotype != None
                assert one_haplotype != other_haplotype
                recombinated_haplotype = generate_haplotype(haplotype_length, ModificationType.RECOMBINATION, one_haplotype, other_haplotype)
                logger.debug('recombinated_haplotype = %s', recombinated_haplotype)
        else:
            pass
        # adding recombinated haplotype to the list of recombinated haplotypes
        recombinated_haplotypes.append(recombinated_haplotype)
    return (original_haplotype, mutated_haplotypes, recombinated_haplotypes)
