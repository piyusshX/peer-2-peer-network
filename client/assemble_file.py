import os
def assemble_file(num_pieces, name, output_path="output", final_output="output file"):
    os.makedirs(f"{final_output}", exist_ok=True)
    output_file = f"{final_output}/{name}"

    with open(output_file, "wb") as out:
        for i in range(num_pieces):
            piece_path = f"{output_path}/{name}/{i}.bin"

            with open(piece_path, "rb") as f:
                out.write(f.read())

            print(f"{i}/{num_pieces-1} pieces assembled", end='\r', flush=True)

    print(f"\nFile assembled: {output_file}")