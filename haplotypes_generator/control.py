import generator
import nexus
import random
import os
import logging

logging.basicConfig()

original_haplotype = None
mutated_haplotypes = None
recombinated_haplotypes = None

def generate_sequence(haplotype_length, total_number, mutation_rate, recombination_rate):
    global original_haplotype
    global mutated_haplotypes
    global recombinated_haplotypes
    logger = logging.getLogger('control.generate_sequence')
    logger.setLevel(logging.INFO)
    logger.debug("generator.generate_haplotype(%d, %d, %f, %f)" % (haplotype_length, total_number, float(mutation_rate)/100, float(recombination_rate)/100))
    original_haplotype, mutated_haplotypes, recombinated_haplotypes = generator.generate_haplotypes(haplotype_length, total_number, float(mutation_rate)/100, float(recombination_rate)/100)

def generate_multiple_sequences(number_simulations, number_haplotypes_minimum, number_haplotypes_maximum, haplotype_length_minimum, haplotype_length_maximum, percentage_rate_minimum, percentage_rate_maximum, directory_to_save_simulations):
    logger = logging.getLogger('control.generate_multiple_sequences')
    logger.setLevel(logging.INFO)
    number_haplotypes = [random.randint(number_haplotypes_minimum, number_haplotypes_maximum) for x in range(0,number_simulations)]
    haplotypes_lengths = [random.randint(haplotype_length_minimum, haplotype_length_maximum) for x in range(0,number_simulations)]
    mutation_rates  = [random.randint(percentage_rate_minimum, percentage_rate_maximum) for x in range(0,number_simulations)]
    for simulation_number in range(0,number_simulations):
        generate_sequence(haplotypes_lengths[simulation_number], number_haplotypes[simulation_number], mutation_rates[simulation_number], 100-mutation_rates[simulation_number])
        logger.info("Creating file #" + str(simulation_number + 1) + ": " + directory_to_save_simulations + os.sep + "simulation_h" + str(number_haplotypes[simulation_number]) + "_m" + str(mutation_rates[simulation_number]) + "_r" + str(100-mutation_rates[simulation_number]) + ".nex")
        save_file(directory_to_save_simulations + os.sep + "simulation_h" + str(number_haplotypes[simulation_number]) + "_m" + str(mutation_rates[simulation_number]) + "_r" + str(100-mutation_rates[simulation_number]) + ".nex")

def save_file(file_path):
    nexus_file = nexus.NexusWriter()
    nexus_file.add_comment("File made with Ricardo Henrique Gracini Guiraldelli's <rguira@acm.org> simulator.")
    # adding the original haplotype
    for i in range(0,len(original_haplotype)):
        nexus_file.add("original", i, original_haplotype[i])
    # adding the mutated haplotypes
    for i in range(0,len(mutated_haplotypes)):
        if mutated_haplotypes[i] != None:
            for j in range(0,len(mutated_haplotypes[i])):
                nexus_file.add("mutated" + str(i), j, mutated_haplotypes[i][j])
    # adding the recombinated haplotypes
    for i in range(0,len(recombinated_haplotypes)):
        if recombinated_haplotypes[i] != None:
            for j in range(0,len(recombinated_haplotypes[i])):
                nexus_file.add("recombinated" + str(i), j, recombinated_haplotypes[i][j])
    # saving file
    nexus_file.write_to_file(filename=file_path, charblock=True)
    # print nexus_file.make_nexus(charblock=True)
