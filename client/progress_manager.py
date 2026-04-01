import os

def save_progress(name, total_pieces, downloaded_set):
    os.makedirs(f"output/{name}", exist_ok=True)
    filename = f"output/{name}/_progress"
    temp = filename + ".tmp"

    with open(temp, "w") as f:
        f.write(f"TOTAL={total_pieces}\n")
        f.write("DOWNLOADED=" + ",".join(map(str, sorted(downloaded_set))))

    os.replace(temp, filename)

def load_progress(name):
    filename = f"output/{name}/_progress"
    downloaded = set()
    total = 0

    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("TOTAL="):
                total = int(line.strip().split("=")[1])

            elif line.startswith("DOWNLOADED="):
                data = line.strip().split("=")[1]
                if data:
                    downloaded = set(map(int, data.split(",")))

    except FileNotFoundError:
        pass

    return total, downloaded

def show_progress(downloaded, total):
    percent = (len(downloaded) / total) * 100
    print(f"\rProgress: {len(downloaded)}/{total} ({percent:.2f}%)", end='')