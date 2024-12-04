# importing the module
import tracemalloc
import prtpy
import random

def greedy(input_set):
    prtpy.partition(algorithm=prtpy.partitioning.greedy, numbins=2, items=input_set)

def ckk(input_set):
    prtpy.partition(algorithm=prtpy.partitioning.complete_karmarkar_karp, numbins=2, items=input_set)

#saveF = open("output", 'w')
saveF = None
step = 1
while step <= 20:
    testset = [random.randint(0, step) for _ in range(0, step)]
    print(f"Step number {step}", file=saveF)

    tracemalloc.start()
    tracemalloc.reset_peak()
    greedy(testset)
    greedyPeek = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f"G: {greedyPeek}", file=saveF)

    tracemalloc.start()
    tracemalloc.reset_peak()
    ckk(testset)
    ckkPeak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f"C: {ckkPeak}", file=saveF)

    print(file=saveF)
    step += 1