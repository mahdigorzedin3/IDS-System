import sys
memory_hog = []
try:
    while True:
        memory_hog.append(bytearray(100 * 1024 * 1024))  
        print(f"Memory usage: {sys.getsizeof(memory_hog)} bytes")
except MemoryError:
    print("Out of memory! System is running low on RAM.")
