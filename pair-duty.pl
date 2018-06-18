#! /usr/bin/perl

use v5.22;
use strict;
use warnings;
use utf8;
use List::MoreUtils qw(zip_unflatten);
use DateTime;
#use DateTime::Duration;
#use Time::Moment;
#use DateTime::TimeZone::Local;
use DateTime::Format::Flexible;
use DateTime::Format::Strptime;
use Data::Dump qw(dump);
use Spreadsheet::GenerateXLSX qw(generate_xlsx);

say $ARGV[0];
my $date = $ARGV[0]
    ? DateTime::Format::Flexible->parse_datetime($ARGV[0], european => 1)
    : DateTime->now;

$date->set_formatter(DateTime::Format::Strptime->new(pattern => '%d-%m-%Y'));

my @names = qw(
anton berko boris genady michael moshe nati igor
raphael senya stas yaniv shabtai avi vladimir
);

my @shifted_names = (@names[$#names/2..$#names], @names[0..$#names/2-1]);
dump @shifted_names;

my @result = ();
for (0..$#names/2) {
    my $shifted_elem = shift @shifted_names;
    push @shifted_names, $shifted_elem;
    if ($names[0] ne $shifted_names[0]) {
        push @result, zip_unflatten(@names, @shifted_names);
    }
}

for my $idx (0..$#result) {
    push @{$result[$idx]}, $date->add(weeks => ($idx ? 1 : 0))->stringify();
    unshift @{$result[$idx]}, '';
}
unshift @result, ['toran3', 'toran2', 'toran1', 'date'];
dump @result;

generate_xlsx('pair_duty.xlsx', \@result);

