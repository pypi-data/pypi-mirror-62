csvy
----

Basic context wrappers for stardard library csv.read and csv.write methods.

Writer example:

    import csvy

    with csvy.writer('csvpath.csv') as csvfile:
        csvfile.writerow([1, 2, 3, 4])


Reader example:

    import csvy

    with csvy.reader('csvpath.csv') as csvfile:
        for index, row in csvfile.iter():
            print(f"{index}: {row}")
