#!/usr/bin/perl

use File::Stat;
use File::Basename;

my $version = "1.0.1";
# main
my $scriptname = basename($0);
$scriptdir = "/etc/zabbix/scripts";
#my $scriptdir = "/home/zabbix";
# meteor vars
my $meteorcfg = "/opt/meteor/stats/dpdk_ifconfig";
#my $meteorcfg = $scriptdir."/dpdk_ifconfig";
my $meteorout = $scriptdir."/meteor.out";

my @pl2 = qw(objsps objs rx_bps rx_bytes rx_pps rx_packets tx_bps tx_bytes tx_pps tx_packets);
my %props = (
    "obj" => "skipped",
    "rx_" => "traffic",
    "tx_" => "out"
    );

my %mode = (
    "dec" => "1000",
    "bin" => "1024",
    );
my %x = (
    "K" => 1,
    "M" => 2,
    "G" => 3,
    "T" => 4,
    "P" => 5,
    );


# Checking parameteres
if ($ARGV[0] eq "version") {
    print $version;
    exit;
    }
if (($#ARGV == -1) || (! isInList($ARGV[1], @pl2))){
    printUsage();
    }


if (-e $meteorcfg) {
    $meteorout .= ".".int(rand(time));
    my $mt = 0;
    while ($mt != stat($meteorcfg)->mtime) {
        $mt = stat($meteorcfg)->mtime;
        sleep 1;
        }
    system("cp $meteorcfg $meteorout");
    }
else {
    print "$meteorcfg not found";
    exit;
    }

my $grep = "SYSLOG WL app\\[";
my $findstring = "cat ".$meteorout." 2>/dev/null | grep '$grep' | wc -l";  #1
my $test = (int(`$findstring`) > 0);

if ($test) {
    my $tail = int(`cat -n $meteorout | grep '$grep' | awk '{print \$1}'`); #163
    my $text = `cat $meteorout | tail -n+$tail`; 
    chomp $text; # удалить пробелы в dpdk c конца до 163 строки

    $ARGV[0] =~ m/(.*)_(\d+)/;
    my $name = $1;
    my $id = $2;

    $ARGV[1] =~ m/(\w{3}).*/;
    my $prop = $1;

    my @array = split(/(?=$grep)/, $text);
    foreach $block (@array) {
        my $match = $grep.$name."\\] \\(source ".$id."\\)";
        next if ($block !~ m/^$match/);

        my @lines = split(/\n/, $block);
        my @line = grep(/$props{$prop}/, @lines);
        $line = trim(@line[0]);

        if ($prop ne "obj") {
            #$line =~ /\s(.*bps)\s\(.*\[(\d+)\sbytes\]\),\s(.*pps)\s\(.*\[(\d+)\spkts\]\)/;     #new
            $line =~ /\s(.*bps)\s\((.*)\sbytes\),\s(.*pps)\s\((.*)\spkts\)/;
            my $bps = $1;
            my $bytes = $2;
            my $pps = $3;
            my $pkts = $4;
            #print $line."\n";
            if ($ARGV[1] =~ /bps$/) {
                print calcValue($bps, "dec");
                }
            elsif ($ARGV[1] =~ m/bytes$/) {
                print calcValue($bytes, "bin");
                }
            elsif ($ARGV[1] =~ m/pps$/) {
                print calcValue($pps, "dec");
                }
            elsif ($ARGV[1] =~ m/packets$/) {
                print calcValue($pkts, "dec");
                }
            }
        else {
            #$line =~ m/\s(.*obj\/s)\s\(.*\[(\d+)\sobjs\]\)/; # new
            $line =~ m/\s(.*obj\/s)\s\((.*)\sobjs\)/;;
            my $objsps = trimfull($1);
            my $objs = $2;
            #print $line."\n";
            if ($ARGV[1] =~ /objsps$/) {
                print calcValue($objsps, "dec");
                }
            elsif ($ARGV[1] =~ m/objs$/) {
                print calcValue($objs, "dec");
                }
            }
        }
    }
else {
    print "bad";
    }

if (-e $meteorout) {system("rm -f $meteorout");}

#################################################################################

sub printUsage {
    print "\033[1musage:\033[0m\t$scriptname <natw_name_id> <".join("|", @pl2).">\n";
    print "\t$scriptname version\n";
    exit;
    }

sub isInList {
    my ($e, @a) = @_;
    my $c = grep(/^$e$/ig, @a);
    return ($c > 0);
    }

sub  trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };
sub  trimfull { my $s = shift; $s =~ s/\s+//g; return $s };


sub calcValue {
    my ($value, $calcmode) = @_;
    my $power = 0;

    $value =~ m/(^\d+\.?\d+)(\D+$)/;
    $value = $1 if ($1 ne "");

    my $prefix = $2;
    $prefix =~ m/^(.)/;
    $prefix = $1;

    $power = $x{$prefix} if (isInList($prefix, keys %x));
    return int($value*$mode{$calcmode}**$power+0.5);
    }

