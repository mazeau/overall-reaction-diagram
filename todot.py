"""
Script to take the overall integration_flux_data.txt and create a dot file.

After running this, run 'dot -Tpdf integration_flux_data.dot -ooverallpathway.pdf'
to get the pathway in pdf
"""

f = open("integration_flux_data.txt", "r")

list_of_strings = ['digraph reaction_paths {','center=1;']

data = []
species_dict = {}
for line in f:
    s1, s2, net = line.split()
    # n = '{:.20f}'.format(float(net))  # surpressing scientific notation

    if float(net) < 0.:  # if net is negative, switch s1 and s2 so it is positive
        data.append([s2, s1, float(net) * -1])
    else:
        data.append([s1, s2, float(net)])

    # renaming species to dot compatible names
    if s1 not in list(species_dict.keys()):
        species_dict[s1] = 's' + str(len(species_dict) + 1)
    if s2 not in list(species_dict.keys()):
        species_dict[s2] = 's' + str(len(species_dict) + 1)

# getting the arrow widths
largest_rate = max([row[2] for row in data])
smallest_rate = min([row[2] for row in data])

# setting the threshold
threshold = 1e-9

added_species = {}  # dictionary of species that show up on the diagram
for x in data:  # writing the node connections
    s1, s2, net = x
    if net < threshold:  # don't include the paths that are below the threshold
        continue
    label = net / largest_rate
    rounded_label = '{:0.3e}'.format(label)

    pen_width = ((net - smallest_rate) / (largest_rate - smallest_rate)) * 4 + 2
    str_to_add = species_dict[s1] + ' -> ' + species_dict[s2] + '[fontname="Helvetica", penwidth=' + str(pen_width) + ', arrowsize=' + str(pen_width / 2) + ', label=" ' + str(rounded_label) + '"];'
    list_of_strings.append(str(str_to_add))

    if s1 not in list(added_species.keys()):
        added_species[s1] = species_dict[s1]
    if s2 not in list(added_species.keys()):
        added_species[s2] = species_dict[s2]

for species in added_species:  # writing the species translations
    str_to_add = added_species[species] + ' [ fontname="Helvetica", label="' + species + '"];'
    list_of_strings.append(str_to_add)

list_of_strings.append(' label = "Scale = ' + str(largest_rate) + '";')
list_of_strings.append(' fontname = "Helvetica";')
list_of_strings.append('}')

with open("integration_flux_data.dot",'w') as f:
    for x in list_of_strings:
        f.write('{}\n'.format(x))
