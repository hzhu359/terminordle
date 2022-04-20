from timeit import default_timer as timer

start = timer()

with open('./dictionaries/valid_guesses.txt', 'r') as file:
    print('reuse' in file.read())

end = timer()

print(f'that took {end - start}.')
