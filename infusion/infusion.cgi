#!/usr/bin/perl -T
# Calculates temperature of infusion water
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $Tw     = 0;
my $T1     = 152;
my $T2     = 168;
my $G      = 10;
my $Wm     = 20;
my $Wa     = 14;
my $sparge = 'Y';
my $Ds     = 2;
my $T1t    = 'F';
my $T2t    = 'F';
my $Gu     = 'lbs';
my $WmU    = 'q';
my $DsU    = 'q';
my $WaU    = 'q';

print header();
print start_html( -title => 'Calculate Temperature of Infusion Water' );

print '<center>', br;

print start_form,
  strong('Initial Temperature of Mash '),
  textfield( -name => 'T1', -value => '152', -size => 2, -maxlength => 3 ),
  radio_group(
    -name    => 'T1t',
    -values  => [ 'F', 'C' ],
    -default => 'F'
  ),
  br,
  strong('Target Temperature of Mash '),
  textfield( -name => 'T2', -value => '168', -size => 2, -maxlength => 3 ),
  radio_group(
    -name    => 'T2t',
    -values  => [ 'F', 'C' ],
    -default => 'F'
  ),
  br,

  strong('Amount of Grain in Mash '),
  textfield( -name => 'G', -value => '10', -size => 4, -maxlength => 6 ),
  radio_group(
    -name    => 'Gu',
    -values  => [ 'lbs', 'kg' ],
    -default => 'lbs'
  ),
  br,

  strong('Amount of Water Already in Mash '),
  textfield( -name => 'Wm', -value => '20', -size => 3, -maxlength => 5 ),
  radio_group(
    -name    => 'WmU',
    -values  => [ 'q', 'g', 'l' ],
    -default => 'q'
  ),
  br, strong('Batch Sparge? '),
  radio_group(
    -name    => 'sparge',
    -values  => [ 'Y', 'N' ],
    -default => 'N'
  ),
  br,
  strong('Mash Tun Dead Space '),
  textfield( -name => 'Ds', -value => '0', -size => 3, -maxlength => 3 ),
  radio_group(
    -name    => 'DsU',
    -values  => [ 'q', 'g', 'l' ],
    -default => 'q'
  ),
  br,
  strong('Amount of Water to be Added '),
  textfield( -name => 'Wa', -value => '14', -size => 3, -maxlength => 4 ),
  radio_group(
    -name    => 'WaU',
    -values  => [ 'q', 'g', 'l' ],
    -default => 'q'
  ),
  br,
  submit( -value => 'Calculate Infusion Water Temperature' ),
  end_form;

if (   !param('T1')
    && !param('T2')
    && !param('G')
    && !param('Wm')
    && !param('Wa') )
{
    print br,
      strong('Please input temperature, grain weight and amount of water');
    die 'No temperature, weight or water volume entered';
}

if ( param('T1') =~ /^\d+(\.\d{1,3})?$/ ) {
    $T1 = param('T1');
    if ( param('T1t') eq 'F' ) {
        $T1t = param('T1t');
    }
    elsif ( param('T1t') eq 'C' ) {
        $T1t = param('T1t');
        $T1  = ( $T1 * 1.8 ) + 32;
    }
    else {
        print "Initial temperature unit is illegal value";
        die "Initial temperature unit is illegal value";
    }
}
else {
    print br, strong('Initial temperature must be a positive number');
    die 'Initial temperature must be a positive number';
}

if ( param('T2') =~ /^\d+(\.\d{1,3})?$/ ) {
    $T2 = param('T2');
    if ( param('T2t') eq 'F' ) {
        $T2t = param('T2t');
    }
    elsif ( param('T2t') eq 'C' ) {
        $T2t = param('T2t');
        $T2  = ( $T2 * 1.8 ) + 32;
    }
    else {
        print "Target temperature unit is illegal value";
        die "Target temperature unit is illegal value";
    }
}
else {
    print br, strong('Target temperature must be a positive number');
    die 'Target temperature must be a positive number';
}

if ( param('G') =~ /^\d+(\.\d{1,3})?$/ ) {
    $G = param('G');
    if ( param('Gu') eq 'lbs' ) {
        $Gu = param('Gu');
    }
    elsif ( param('Gu') eq 'kg' ) {
        $Gu = param('Gu');
        $G  = $G * 2.20462;
    }
    else {
        print "Grain unit is illegal value";
        die "Grain unit is illegal value";
    }
}
else {
    print br, strong('Amount of grain must be a positive number');
    die 'Amount of grain must be a positive number';
}

if ( param('Wm') =~ /^\d+(\.\d{1,3})?$/ ) {
    $Wm = param('Wm');
    if ( param('WmU') eq 'q' ) {
        $WmU = param('WmU');
    }
    elsif ( param('WmU') eq 'g' ) {
        $WmU = param('WmU');
        $Wm  = $Wm * 4;
    }
    elsif ( param('WmU') eq 'l' ) {
        $WmU = param('WmU');
        $Wm  = $Wm / 1.056688208;
    }
    else {
        print "Total water unit is illegal value";
        die "Total water unit is illegal value";
    }
}
else {
    print br, strong('Amount of water in mash must be a positive number');
    die 'Amount of water in mash must be a positive number';
}

if ( param('Ds') =~ /^\d+(\.\d{1,3})?$/ ) {
    $Ds = param('Ds');
    if ( param('DsU') eq 'q' ) {
        $DsU = param('DsU');
    }
    elsif ( param('DsU') eq 'g' ) {
        $DsU = param('DsU');
        $Ds  = $Ds * 4;
    }
    elsif ( param('DsU') eq 'l' ) {
        $DsU = param('DsU');
        $Ds  = $Ds / 1.056688208;
    }
    else {
        print "Dead space unit is illegal value";
        die "Dead space unit is illegal value";
    }
    if ( param('sparge') eq 'Y' ) {
        $sparge = param('sparge');
        $Wm = $Ds + ( $G * 0.2 ) * 4;
    }
    elsif ( param('sparge') eq 'N' ) {
        $sparge = param('sparge');
        $Wm     = $Wm;
    }
    else {
        print "Sparge is illegal value";
        die "Sparge is illegal value";
    }
}
else {
    print br, strong('Dead space must be a number');
    die 'Dead space must be a number';
}

if ( param('Wa') =~ /^\d+(\.\d{1,3})?$/ ) {
    $Wa = param('Wa');
    if ( param('WaU') eq 'q' ) {
        $WaU = param('WaU');
    }
    elsif ( param('WaU') eq 'g' ) {
        $WaU = param('WaU');
        $Wa  = $Wa * 4;
    }
    elsif ( param('WaU') eq 'l' ) {
        $WaU = param('WaU');
        $Wa  = $Wa / 1.056688208;
    }
    else {
        print "Water added unit is illegal value";
        die "Water added unit is illegal value";
    }
}
else {
    print br, strong('Amount water added must be a positive number');
    die 'Amount of water added must be a positive number';
}

$Tw = ( ( ( $T2 - $T1 ) * ( ( 0.2 * $G ) + $Wm ) ) / $Wa ) + $T2;
$Tw = sprintf "%.0f", $Tw;
print br, strong( 'Infusion Water Temperature: ' . $Tw );

print '</center>';
print end_html;
exit;
