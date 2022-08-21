def announce_result(counter, filename):
    cells_cell = 'cell' if counter.checked == 1 else 'cells'
    were_was = 'was' if counter.checked == 1 else 'were'
    print(f"{counter.checked} {cells_cell} {were_was} corrected in {filename}")
