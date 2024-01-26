import tracemalloc
import numpy as np

tracemalloc.start(25)

l1 = [i for i in range(10000)]
l2 = [i*i for i in range(10000)]
l3 = [i*i*i for i in range(10000)]
l4 = np.random.randint(1, 100, (1000,))

snapshot = tracemalloc.take_snapshot()

print("========== SNAPSHOT =============")
for stat in snapshot.statistics("lineno"):
    print(stat)
    print(stat.traceback.format())

print("\n=========== USEFUL METHODS ===========")
print("\nTraceback Limit : ", tracemalloc.get_traceback_limit(), " Frames")

print("\nAllocation Location for List l4 : ",
      tracemalloc.get_object_traceback(l4))

print("\nTraced Memory (Current, Peak): ", tracemalloc.get_traced_memory())

# tracemalloc.reset_peak()

# print("\nTraced Memory : ", tracemalloc.get_traced_memory())

print("\nMemory Usage by tracemalloc Module : ",
      tracemalloc.get_tracemalloc_memory(), " bytes")

print("\nTracing Status : ", tracemalloc.is_tracing())

tracemalloc.stop()
