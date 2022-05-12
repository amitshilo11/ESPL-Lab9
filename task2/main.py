import sys

from plumbum import local
import numpy as np
import matplotlib.pyplot as plt

FILE_SRC = "IMDB.csv"
TEMP_SRC = "temp_table.csv"
DELMITER = '|'

# IMDB.csv format:
# imdb_title_id,original_title,year,genre,duration,country
#      1               2        3     4       5       6
ALL_COLS = '$0'
FIRST_COL = '$1'
SECCOND_COL = '$2'

ID_COL = '$1'
TITLE_COL = '$2'
YEAR_COL = '$3'
GENRE_COL = '$4'
DURATION_COL = '$5'
COUNTRY_COL = '$6'

def init():
    # convert input:
    # csvtool -u \| -t , cat IMDB.csv > IMDB_n.csv
    (local.cmd.csvtool["-u", DELMITER, "-t", ",", "cat", FILE_SRC] > TEMP_SRC)()
    with open(TEMP_SRC, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(TEMP_SRC, 'w') as fout:
        fout.writelines(data[1:])

def done():
    # delete convertion
    local.cmd.rm[TEMP_SRC]()

def clean():
    local.cmd.rm["movies.stats"]()


clean_blanc_rows = local.cmd.grep["-v", '^\s*$']

class awk:
    def get_col(col):
        return (r'{print %s}'%(col))
    
    def get_cols(col1, col2, delim):
        return (r'{print %s"%s"%s}'%(col1, delim, col2))
    
    def replace_char(old_char, new_char, col):
        return (r'{gsub(/\%s/, "%s", %s); print}'%(old_char, new_char, col))

    def serch_in_col(val, col):
        return (r'%s~ /%s/ {print}'%(col, val))
    
    def filter_by_col(val, op, col):
        return (r'{if(%d%s%s) print;}'%(val, op, col))

    def to_output_format(delim):
        return (r'{out=""; i=1; for(i; i<=NF; i++) {if(i==NF) {j = i-1; out = out$i"%s"$j} }; print out}'%(delim))


def movies_per_country():
    OUTPUT_FILE = 'movies.stats'

    init()
    mov_list = (
        local.cmd.cat[TEMP_SRC] | 
        local.cmd.awk["-F", DELMITER, awk.get_col(COUNTRY_COL)] |
        local.cmd.awk[awk.replace_char(r', ', r'\n', ALL_COLS)] |
        local.cmd.sort | 
        local.cmd.uniq["-c"] |
        local.cmd.awk["-F", "[\* ]", awk.to_output_format('|')]
    )

    with open(OUTPUT_FILE,'w+') as f:
        f.write(mov_list())
    done()

def movies_after_date_by_country(date, country):
    init()
    mov_list = (
        local.cmd.cat[TEMP_SRC] | 
        local.cmd.awk["-F", DELMITER, awk.serch_in_col(country, COUNTRY_COL)] |
        local.cmd.awk["-F", DELMITER, awk.filter_by_col(date, '<', YEAR_COL)] |
        local.cmd.awk["-F", DELMITER, awk.get_col(TITLE_COL)]
    )
    result = mov_list()
    done()
    return result

def histogram_graph():
    init()
    data = (
        local.cmd.cat[TEMP_SRC] | 
        local.cmd.awk["-F", DELMITER, awk.get_col(YEAR_COL)] |
        clean_blanc_rows
    )

    data_vector = data().split('\n')
    data_vector = np.delete(data_vector, len(data_vector)-1)
    data_vector = list(map(int, data_vector))

    n, bins, patches = plt.hist(data_vector, bins='auto')
    plt.xlabel('Year')
    plt.ylabel('Times Presented')
    plt.title('Histogram Of The Number Of Movies Presented Each Year:')
    plt.grid(False)

    plt.show()
    done()

# Calculate the total duration of movies for each genre
def average_duration_by_genre():
    init()
    data = (
        local.cmd.cat[TEMP_SRC] | 
        local.cmd.awk["-F", DELMITER, awk.get_col(GENRE_COL)] |
        local.cmd.awk[awk.replace_char(r', ', r'\n', ALL_COLS)] |
        local.cmd.sort |
        local.cmd.uniq
    )
    genres = data().split('\n')
    genres = np.delete(genres, len(genres)-1)

    cluc_ave = (r'BEGIN{sum=0; count=0;}'\
                r'{sum=sum+$5; count++}'\
                r'END{if(count>0) print sum/count}')

    ave_str = ""
    for g in genres:
        ave_data = (
            local.cmd.cat[TEMP_SRC] | 
            local.cmd.awk["-F", DELMITER, awk.serch_in_col(g, GENRE_COL)] |
            local.cmd.awk["-F", DELMITER, cluc_ave]
        )
        ave_str += g + "\t" + ave_data()

    print(ave_str)
    done()

def get_unic_arr_by_col(col):
    init()
    data = (
            local.cmd.cat[TEMP_SRC] |
            local.cmd.awk["-F", DELMITER, awk.get_col(col)] |
            local.cmd.awk[awk.replace_char(r', ', r'\n', ALL_COLS)] |
            local.cmd.sort |
            local.cmd.uniq
    )
    arr = data().split('\n')
    arr = np.delete(arr, len(arr) - 1)
    done()
    return arr

def genres_cunter_in_country(country):
    genres = get_unic_arr_by_col(GENRE_COL)
    init()
    print("genres cunter in: ", country)
    for g in genres:
        data = (
                local.cmd.cat[TEMP_SRC] |
                local.cmd.awk["-F", DELMITER, awk.serch_in_col(country, COUNTRY_COL)] |
                local.cmd.awk["-F", DELMITER, awk.serch_in_col(g, GENRE_COL)] |
                clean_blanc_rows |
                local.cmd.wc["-l"]
        )
        print(g, data())



def main():
    print("hey")
    #movies_per_country()
    #print(movies_after_date_by_country(1980, "USA"))
    #histogram_graph()
    #average_duration_by_genre()
    #genres_cunter_in_country("USA")
    #init()
    #clean()
    

if __name__ == "__main__":
    main()