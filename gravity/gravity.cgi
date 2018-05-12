#!/usr/bin/perl -T
# Correct specific gravity for temperature
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $temp      = 70;
my $gravity   = 1.050;
my $temp_unit = 'f';
my $sg        = 1.050;

print header();
print start_html( -title => 'Specific Gravity Temperature Correction' );

print '<center>', br;

print start_form, strong('Temperature'),
  textfield(
    -name      => 'temp',
    -value     => '150',
    -size      => 2,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'temp_unit',
    -values  => [ 'c', 'f' ],
    -default => 'f'
  ),
  br, strong('Specific Gravity'),
  textfield(
    -name      => 'gravity',
    -value     => '1.050',
    -size      => 4,
    -maxlength => 5
  ),
  br,
  submit( -value => 'Calculate Post Boil Gravity' ),
  end_form;

if ( !param('temp') && !param('temp_unit') && !param('gravity') ) {
    print br,
      strong('Please input specific gravity, temperature and temperature unit');
    die 'No temperature or gravity entered';
}

if ( param('temp') =~ /^\d+(\.\d{1,5})?$/ ) {
    $temp = param('temp');
    if ( param('temp_unit') eq 'f' ) {
        $temp_unit = param('temp_unit');
    }
    elsif ( param('temp_unit') eq 'c' ) {
        $temp_unit = param('temp_unit');
        $temp      = ( $temp - 32 ) / 1.8;
    }
    else {
        print "Temperature unit is illegal value";
        die "Temperature unit is illegal value";
    }
}
else {
    print br, strong('Temperature must be a positive number');
    die 'Temperature must be a positive number';
}

if ( param('gravity') =~ /^\d+(\.\d{1,7})?$/ ) {
    $gravity = param('gravity');
}
else {
    print br, strong('Gravity must be a positive number');
    die 'Gravity must be a positive number';
}

$sg =
  1.313454 -
  0.132674 * $temp +
  0.002057793 * $temp**2 -
  0.000002627634 * $temp**3;
$sg = $gravity + ( $sg * 0.001 );
$sg = sprintf "%.3f", $sg;
print br, strong( 'Adjusted Gravity: ' . $sg );

print '</center>';
print end_html;
exit;
