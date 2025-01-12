with open('NewRMAZ.txt', 'r') as file:
    lines = file.readlines()
entries = []
seen_words = set()
for line in lines:
    split_line = line.strip().split("▶")
    if len(split_line) == 2:
        parts = split_line[1].split()
        if len(parts) > 1:
            word = split_line[1]
            if word not in seen_words:
                rf1=split_line[1].rfind('\t')
                rf2=split_line[1].rfind(' ')
                rf3=split_line[1].rfind('	')
                index=max(rf1,rf2,rf3)
                split_line[1]=split_line[1][:index-1]+"\t"+split_line[1][index+1:]
                entries.append(split_line)
                seen_words.add(word)

sorted_entries = sorted(entries, key=lambda x: x[0].split()[1].lower())
#Sort alphabetically

sorted_lines = [' ▶'.join(entry) for entry in sorted_entries]
with open('RM-AZ.txt', 'w') as file:
    file.write('\n'.join(sorted_lines))