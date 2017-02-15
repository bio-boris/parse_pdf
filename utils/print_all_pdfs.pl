#!/usr/bin/env perl
use strict;
my $ls = `ls | grep *.pdf_`;
my @files = split "\n", $ls;


foreach my $file(@files){
    my $command = "time python ~/Documents/parse_pdf/pdf_watermark.py $file";
    print "About to $command\n";
    my $t = system($command);
    print($t); 
}
