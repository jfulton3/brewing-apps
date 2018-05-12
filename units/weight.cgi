#!/usr/bin/perl -T
# Converts weight units
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $t1   = 'lb';
my $t2   = 'kg';
my $from = 0;
my $to   = 0;

print header();
print start_html( -title => 'Weight Unit Converter' );

print '<center>', br;

print start_form, strong('Weight to convert from'),
  textfield(
    -name      => 'from',
    -value     => '0',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 't1',
    -values  => [ 'lb', 'kg', 'oz', 'g' ],
    -default => 'lb'
  ),
  br, strong('Weight unit to convert to'),

  radio_group(
    -name    => 't2',
    -values  => [ 'lb', 'kg', 'oz', 'g' ],
    -default => 'kg'
  ),
  br,
  submit( -value => 'Convert weight' ),
  end_form;

if ( !param('t1') && !param('t2') && !param('from') ) {
    print br, strong('Please input unit of weight to convert');
    die 'No weight unit';
}
$t1   = param('t1');
$t2   = param('t2');
$from = param('from');
if ( $t1 eq 'lb' && $t2 eq 'kg' ) {
    $to = $from * 0.45359;
}
elsif ( $t1 eq 'lb' && $t2 eq 'oz' ) {
    $to = $from * 16;
}
elsif ( $t1 eq 'lb' && $t2 eq 'g' ) {
    $to = $from * 453.59232;
}
elsif ( $t1 eq 'kg' && $t2 eq 'lb' ) {
    $to = $from * 2.20462;
}
elsif ( $t1 eq 'kg' && $t2 eq 'oz' ) {
    $to = $from * 35.27397;
}
elsif ( $t1 eq 'kg' && $t2 eq 'g' ) {
    $to = $from * 1000;
}
elsif ( $t1 eq 'oz' && $t2 eq 'lb' ) {
    $to = $from / 16;
}
elsif ( $t1 eq 'oz' && $t2 eq 'kg' ) {
    $to = $from * 0.02835;
}
elsif ( $t1 eq 'oz' && $t2 eq 'g' ) {
    $to = $from * 28.34952;
}
elsif ( $t1 eq 'g' && $t2 eq 'lb' ) {
    $to = $from * 0.0022;
}
elsif ( $t1 eq 'g' && $t2 eq 'kg' ) {
    $to = $from / 1000;
}
elsif ( $t1 eq 'g' && $t2 eq 'oz' ) {
    $to = $from * 0.03527;
}
else {
    print "Weight unit is illegal value";
    die "Weight unit is illegal value";
}

print br, strong( 'Converted Unit: ' . $to . $t2 );

print '</center>';
print end_html;
exit;
