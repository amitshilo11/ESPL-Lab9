BEGIN {
    FS = "[|]";
}
{
    print $NF
}
END {

}