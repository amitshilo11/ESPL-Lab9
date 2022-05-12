import sys
from plumbum import local
import numpy as np
import matplotlib.pyplot as plt

DELMITER = '|'

# IMDB.csv format: imdb_title_id,original_title,year,genre,duration,country
ALL = '$0'
FIRST = '$1'
SECCOND = '$2'

ID = '$1'
TITLE = '$2'
YEAR = '$3'
GENRE = '$4'
DURATION = '$5'
COUNTRY = '$6'

def init():
    # convert input:
    # csvtool -u \| -t , cat IMDB.csv > IMDB_n.csv
    (local.cmd.csvtool["-u", DELMITER, "-t", ",", "cat", "IMDB.csv"] > "IMDB_n.csv")()

def done():
    # delete convertion
    local.cmd.rm["IMDB_n.csv"]()

def clean():
    #local.cmd.rm["IMDB_n.csv"]()
    local.cmd.rm["movies.stats"]()
    local.cmd.rm["movies.histogram"]()


clean_blanc_rows = local.cmd.grep["-v", '^\s*$']
flat_col = r'{out = ""; for(i=1; i<=NF; i++){ out = out"\n"$i };  print out}'
to_output_format = r'{out = ""; i = 1; for(i; i<=NF; i++) {if(i==NF) {j = i-1; out = out$i"|"$j} }; print out}'
to_output_format2 = r'{out = ""; i = 1; for(i; i<=NF; i++) {if(i==NF) {j = i-1; out = out$i" "$j} }; print out}'
col_to_row = r'{out = ""; for(i=1; i<=NF; i++){ out = out","$i };  print out}'

def replace_delmiter(new_del):
    return (r'{out = ""; for(i=1; i<=NF; i++){ out = out"%s"$i };  print out}'%(new_del))

def awk_after_date_by_country(date, country):
    return (r'{out = ""; if((%s > %d) && (%s == "%s")) out = out"\n"$0; print out}'%(YEAR, date, COUNTRY, country))

def awk_get_col(col):
    return (r'{print %s}'%(col))

def make_plot(x, y):
    plt.plot(x, y, 'o--', color='blue')
    plt.title('Histogram Of The Number Of Movies Presented Each Year:')
    plt.xlabel('Year')
    plt.ylabel('Times Presented')

    plt.show()

def make_plot2(x, y, data):
    # Fixing random state for reproducibility
    #np.random.seed(19680801)

    #mu, sigma = 100, 15
    #x2 = mu + sigma * np.random.randn(10000)

    # the histogram of the data
    #counts, bins = np.histogram([x, y])
    n, bins, patches = plt.hist(x, 10, facecolor='g')


    plt.xlabel('Year')
    plt.ylabel('Times Presented')
    plt.title('Histogram Of The Number Of Movies Presented Each Year:')
    plt.xlim(x[0], x[len(x)-1])
    plt.ylim(min(y), max(y)*2/3)
    plt.grid(False)

    plt.show()


def movies_per_country():
    init()
    mov_list = (
        local.cmd.awk["-F", DELMITER, awk_get_col(COUNTRY), "IMDB_n.csv"] | 
        local.cmd.awk["-F", "[, ]", flat_col] | 
        clean_blanc_rows | 
        local.cmd.sort | 
        local.cmd.uniq["-c"] |
        local.cmd.awk["-F", "[\* ]", to_output_format]
    )

    with open('movies.stats','w+') as f:
        f.write(mov_list())
    
    done()


def movies_after_date_by_country(date, country):
    init()
    awk_line = awk_after_date_by_country(date, country)
    mov_list = (
        local.cmd.awk["-F", DELMITER, awk_line, "IMDB_n.csv"] |
        local.cmd.grep["-v", '^\s*$']
    )
    print(mov_list())
    done()


def histogram_graph():
    init()
    mov_list = (
        local.cmd.awk["-F", DELMITER, awk_get_col(YEAR), "IMDB_n.csv"] | 
        local.cmd.awk["-F", "[, ]", flat_col] | 
        clean_blanc_rows | 
        local.cmd.sort | 
        local.cmd.uniq["-c"] |
        local.cmd.awk["-F", "[\* ]", to_output_format2]
    )

    with open('movies.histogram.temp','w+') as file:
        file.write(mov_list())

    (local.cmd.head["-n-1", "movies.histogram.temp"] > "movies.histogram")()
    local.cmd.rm["movies.histogram.temp"]()


    data = []
    with open('movies.histogram') as file:
        next(file)
        for line in file:
            row = line.split()
            row = [int(x) for x in row]
            data.append(row)

    years = list(map(lambda x: x[0], data))
    count = list(map(lambda x: x[1], data))

    make_plot(years, count)
    
    done()


def main():
    print("hey")
    #movies_per_country()
    #movies_after_date_by_country(2000, "USA")

    #histogram_graph()

    #clean()
    

if __name__ == "__main__":
    main()