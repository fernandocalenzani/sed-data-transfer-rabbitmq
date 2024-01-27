from tqdm import tqdm


def progress_bar(progress, bar_name):
    with tqdm(total=100, desc=bar_name, unit="%", unit_scale=True) as barra:
        for _ in range(progress):
            barra.update(1)
