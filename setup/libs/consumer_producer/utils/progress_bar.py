import time


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='', flush=True)


def simulate_work(total_iterations, sleep_time=0.1, callback_function=None):
    for i in range(1, total_iterations + 1):
        time.sleep(sleep_time)
        print_progress_bar(i, total_iterations,
                           prefix='[MIMIR] Progress:', suffix='Complete', length=50)

        if i == total_iterations and callback_function is not None:
            callback_function()
