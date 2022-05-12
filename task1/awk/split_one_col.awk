BEGIN {
    FS = "[, ]";
}
{
    out = ""; 
    for(i=1; i<=NF; i++){
        out = out"\n"$i
        }; 
    print out
}
END {

}