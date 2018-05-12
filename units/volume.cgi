#!/usr/bin/perl -T
# Converts liquid volume units
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $t1   = 'qt';
my $t2   = 'gal';
my $from = 0;
my $to   = 0;

print header();
print start_html( -title => 'Liquid Volume Unit Converter' );

print '<center>', br;

print start_form, strong('Liquid Volume to convert from'),
  textfield(
    -name      => 'from',
    -value     => '0',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 't1',
    -values  => [ 'qt', 'gal', 'c', 'l' ],
    -default => 'qt'
  ),
  br, strong('Liquid Volume unit to convert to'),

  radio_group(
    -name    => 't2',
    -values  => [ 'qt', 'gal', 'c', 'l' ],
    -default => 'gal'
  ),
  br,
  submit( -value => 'Convert volume' ),
  end_form;

if ( !param('t1') && !param('t2') && !param('from') ) {
    print br, strong('Please input unit of volume to convert');
    die 'No volume unit';
}
$t1   = param('t1');
$t2   = param('t2');
$from = param('from');
if ( $t1 eq 'qt' && $t2 eq 'gal' ) {
    $to = $from / 4;
}
elsif ( $t1 eq 'qt' && $t2 eq 'c' ) {
    $to = $from * 4;
}
elsif ( $t1 eq 'qt' && $t2 eq 'l' ) {
    $to = ( $from / 4 ) * 3.78541178;
}
elsif ( $t1 eq 'c' && $t2 eq 'qt' ) {
    $to = $from / 4;
}
elsif ( $t1 eq 'c' && $t2 eq 'gal' ) {
    $to = $from / 16;
}
elsif ( $t1 eq 'c' && $t2 eq 'l' ) {
    $to = ( $from / 16 ) * 3.78541178;
}
elsif ( $t1 eq 'gal' && $t2 eq 'qt' ) {
    $to = $from * 4;
}
elsif ( $t1 eq 'gal' && $t2 eq 'c' ) {
    $to = $from * 16;
}
elsif ( $t1 eq 'gal' && $t2 eq 'l' ) {
    $to = $from * 3.78541178;
}
elsif ( $t1 eq 'l' && $t2 eq 'gal' ) {
    $to = $from / 3.78541178;
}
elsif ( $t1 eq 'l' && $t2 eq 'c' ) {
    $to = ( $from / 3.78541178 ) * 16;
}
elsif ( $t1 eq 'l' && $t2 eq 'qt' ) {
    $to = ( $from / 3.78541178 ) * 4;
}
else {
    print "Volume unit is illegal value";
    die "Volume unit is illegal value";
}

print br, strong( 'Converted Unit: ' . $to . $t2 );

print '</center>';
print end_html;
exit;
