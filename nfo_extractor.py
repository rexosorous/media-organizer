import os

tags = set()

for dirs, subdir, file in os.walk('D:\\password\\JAV'):
    for item in file:
        if item.endswith('nfo'):
            with open(os.path.join(dirs, item), 'r') as nfo:
                try:
                    for line in nfo:
                        if '<name>' in line:
                            tags.add(line[line.find('>')+1:line.find('</')])
                except:
                    pass

with open('actors.txt', 'w+') as file:
    for tag in tags:
        file.write(tag + '\n')