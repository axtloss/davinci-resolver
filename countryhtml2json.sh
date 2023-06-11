#!/bin/sh
set -e
# Converts a country.html obtained from the davinci resolve website
# into a json file that can be read by Davinci Resolver
# To obtain a country.html:
# go to https://www.blackmagicdesign.com/products/davinciresolve
# Free Download Now > Linux (version does not matter) > inspect element
# > select the dropdown entry (id is 'country') > right click > Copy > inner html
# Then save the copied string into the root of this project as countries.html

# Seperate each option with a newline
sed 's|</option>|</option>\n|g' countries > countries.tmp

# Remove the placeholder option
sed 's|<option value="" disabled="" class="" selected="selected">Select your country</option>||g' countries.tmp > countries.tmp2

# Remove start of the option value
sed 's|<option label=|\t|g' countries.tmp2 > countries.tmp

# Remove the value for each country shorthand
sed 's| value="string:|: "|g' countries.tmp > countries.tmp2

# Create the json file
echo '{' > countries.json

# Remove the rest of the option syntax
sed 's|">.*|",|g' countries.tmp2 >> countries.json

# Remove the last , in the list
truncate -s -3 countries.json

# close the json object
echo -e '\n}' >> countries.json

# clean up
rm countries.tmp2 countries.tmp
