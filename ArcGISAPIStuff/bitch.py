import re

# get the values
vals = 'Test2 "USEPA HQ 1 RSL IND - SOIL" Test1 test3'

# set a regex to find any values surrounded by double quotes
regx = re.compile(r'(?:(?<=.)|^)(\".*?\")(?=.*?)')
match = regx.findall(vals)

# remove the double quoted strings from the vals variable
for m in match:
    vals = re.sub(m, '', vals)

# split the modified vals at each space
vals = vals.split()

# remove the double quotes from the matched occurences
match = list(map(lambda i : i.strip('"'), match))

# concatenate the list of double quote matches and the list of vals
conc = match + vals

# now map the concatenated list into a valid right hand SQL string
result = ""
for i in conc:
    result += f"'{i}', "

result[:-2]
