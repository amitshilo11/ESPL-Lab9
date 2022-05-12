# grades format: 
# student \tab error_code1:1|error_code2:1|error_code3:0.5 ...

# list of all students
echo list of all students:

awk -F '\t' '{print "\t", $1}' grades 


# the number of students
echo -en '\n'
echo number of students:

awk -F '\t' '{print $1}' grades |
wc -l


# A list of all error-codes mentioned in the file together 
#   with how many times each error-code was mentioned
echo -en '\n'
echo list of all error-codes:

awk -F '\t' '{print $2}' grades |
awk -F '|' '{out=""; for(i=2;i<=NF;i++){out=out"\n"$i}; print out}' |
grep -v "^\s*$" |
awk -F ':' '{print $1}' |
sort |
uniq -c


#  The number of unique error-codes found in the file
echo -en '\n'
echo number of unique error-codes:

awk -F '\t' '{print $2}' grades |
awk -F '|' '{out=""; for(i=2;i<=NF;i++){out=out"\n"$i}; print out}' |
grep -v "^\s*$" |
awk -F ':' '{if($2 < 1) print $1}' |
sort |
uniq -c