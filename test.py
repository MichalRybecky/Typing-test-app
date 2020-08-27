import linecache

#file = open('words200.txt', 'r')
word = linecache.getline('words200.txt', 10).strip()
print(word)
