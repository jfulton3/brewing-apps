#!/usr/bin/perl -T
# Calculates original gravity of mead
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $water_volume = 1;
my $honey_volume = 1;
my $water_unit   = 'gal';
my $honey_unit   = 'lb';
my $Ct           = 1.000;

print header();
print start_html( -title => 'Calculate Original Gravity of Mead' );

print '<center>', br;

print start_form, strong('Volume of Water'),
  textfield(
    -name      => 'water_volume',
    -value     => '1',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'water_unit',
    -values  => [ 'gal', 'qt', 'c' ],
    -default => 'gal'
  ),
  br, strong('Volume of Honey'),
  textfield(
    -name      => 'honey_volume',
    -value     => '1',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'honey_unit',
    -values  => [ 'gal', 'qt', 'c', 'lb', 'oz' ],
    -default => 'lb'
  ),
  br,
  submit( -value => 'Calculate Original Gravity of Mead' ),
  end_form;

if ( !param('water_volume') && !param('honey_volume') ) {
    print br, strong('Please input water and honey volume');
    die 'No water or honey volume';
}

if ( param('water_volume') =~ /^\d+(\.\d{1,3})?$/ ) {
    $water_volume = param('water_volume');
}
else {
    print br, strong('Water volume must be a positive number');
    die 'Water volume must be a positive number';
}

if ( param('honey_volume') =~ /^\d+(\.\d{1,3})?$/ ) {
    $honey_volume = param('honey_volume');
}
else {
    print br, strong('Honey volume must be a positive number');
    die 'Honey volume must be a positive number';
}

if ( param('water_unit') eq 'gal' ) {
    $water_unit   = param('water_unit');
    $water_volume = $water_volume * 16;
}
elsif ( param('water_unit') eq 'qt' ) {
    $water_unit   = param('water_unit');
    $water_volume = $water_volume * 4;
}
elsif ( param('water_unit') eq 'c' ) {
    $water_unit = param('water_unit');
}
else {
    print "Water volume unit is illegal value";
    die "Water volume unit is illegal value";
}

if ( param('honey_unit') eq 'gal' ) {
    $honey_unit   = param('honey_unit');
    $honey_volume = $honey_volume * 16;
}
elsif ( param('honey_unit') eq 'qt' ) {
    $honey_unit   = param('honey_unit');
    $honey_volume = $honey_volume * 4;
}
elsif ( param('honey_unit') eq 'c' ) {
    $honey_unit = param('honey_unit');
}
elsif ( param('honey_unit') eq 'lb' ) {
    $honey_unit   = param('honey_unit');
    $honey_volume = $honey_volume / 11.75 * 16;
}
elsif ( param('honey_unit') eq 'oz' ) {
    $honey_unit   = param('honey_unit');
    $honey_volume = ( $honey_volume / 16 ) / 11.75 * 16;
}
else {
    print "Honey volume unit is illegal value";
    die "Honey volume unit is illegal value";
}

# C1V1+C2V2=CtVt (C=concentration, V=liquid volume, 1=water, 2=honey, t=total)
$Ct =
  ( ( 1 * $water_volume ) + ( 1.417 * $honey_volume ) ) /
  ( $water_volume + $honey_volume );
$Ct = sprintf "%.3f", $Ct;
print br, strong( 'Original Gravity: ' . $Ct );

print '</center>';
print end_html;
exit;
