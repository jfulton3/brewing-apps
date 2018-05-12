#!/usr/bin/perl -T
# Converts temperature units
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $t1   = 'C';
my $t2   = 'F';
my $from = 0;
my $to   = 0;

print header();
print start_html( -title => 'Temperature Unit Converter' );

print '<center>', br;

print start_form, strong('Temperature to convert from'),
  textfield(
    -name      => 'from',
    -value     => '0',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 't1',
    -values  => [ 'C', 'F', 'K' ],
    -default => 'C'
  ),
  br, strong('Temperature unit to convert to'),

  radio_group(
    -name    => 't2',
    -values  => [ 'C', 'F', 'K' ],
    -default => 'F'
  ),
  br,
  submit( -value => 'Convert temperature' ),
  end_form;

if ( !param('t1') && !param('t2') && !param('from') ) {
    print br, strong('Please input unit of temperature to convert');
    die 'No temperature unit';
}
$t1   = param('t1');
$t2   = param('t2');
$from = param('from');
if ( $t1 eq 'C' && $t2 eq 'F' ) {
    $to = ( $from * 1.8 ) + 32;
}
elsif ( $t1 eq 'F' && $t2 eq 'C' ) {
    $to = ( $from - 32 ) / 1.8;
}
elsif ( $t1 eq 'F' && $t2 eq 'K' ) {
    $to = ( $from + 459.67 ) * 5 / 9;
}
elsif ( $t1 eq 'K' && $t2 eq 'F' ) {
    $to = ( $from - 273.15 ) * 1.8 + 32;
}
elsif ( $t1 eq 'C' && $t2 eq 'K' ) {
    $to = $from + 273.15;
}
elsif ( $t1 eq 'K' && $t2 eq 'C' ) {
    $to = $from - 273.15;
}
else {
    print "Temperature unit is illegal value";
    die "Temperature unit is illegal value";
}

print br, strong( 'Converted Unit: ' . $to . $t2 );

print '</center>';
print end_html;
exit;
