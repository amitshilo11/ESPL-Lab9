BEGIN {
    FS = "[|]";
}
{
    out = ""; 
    year = 2000;
    country = "USA";
    if(($3 > year) &&($6 == country)){
        out = out"\n"$0
        }; 
    print out
}
END {

}