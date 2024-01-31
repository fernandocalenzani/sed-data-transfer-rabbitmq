import tracemalloc

from memory_profiler import profile

# Lista global que não será liberada, simulando um vazamento de memória
global_list = []


@profile
def create_data_leak():
    global global_list
    # Adiciona dados à lista global
    global_list.extend(range(100))


@profile
def minha_funcao():
    global global_list
    tracemalloc.start()

    for _ in range(100):
        # Chama a função que adiciona dados à lista global
        create_data_leak()


    snapshot = tracemalloc.take_snapshot()

    for stat in snapshot.statistics("lineno"):
        print(stat)

    tracemalloc.stop()

    stats = tracemalloc.get_tracemalloc_stats()
    for stat in stats:
        print(stat)


print("Fim da função")


minha_funcao()
