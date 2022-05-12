BEGIN {
    FS = "[\* ]";
}
{
    out = ""; 
    i = 1;
    for(i; i<=NF; i++){
        if(i==NF){
            j = i-1;
            out = out$i"|"$j
            }
        }; 
    print out
}
END {

}