file_size = 800
threads_count = 8
used_fragments = 0
fragment_size = file_size // threads_count
for i in range(threads_count):
    # threading.Thread(target=download_file, args=(json_data, size, used+fragments, used_fragments+fragment_size)).start()
    if used_fragments + fragment_size * 2 > file_size:
        print(f'{used_fragments} {file_size}')
        break
    else:
        print(f'{used_fragments} {used_fragments + fragment_size - 1}')
    used_fragments += fragment_size
