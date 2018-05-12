#!/usr/bin/perl -T
# Calculates amount of mash and sparge water
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $batch       = 5;
my $batch_unit  = 'gal';
my $grain       = 10;
my $grain_unit  = 'lb';
my $boil        = 60;
my $loss        = 1;
my $loss_unit   = 'lb';
my $trub        = 1;
my $trub_unit   = 'lb';
my $evaporation = 0;
my $KettleLoss  = 0;
my $GrainLoss   = 0;
my $TotalWater  = 0;
my $MashWater   = 0;
my $SpargeWater = 0;
my $evap        = 10;

print header();
print start_html( -title => 'Calculate Amount of Mash and Sparge Water' );

print '<center>', br;

print start_form, strong('Batch volume '),
  textfield(
    -name      => 'batch',
    -value     => '5',
    -size      => 3,
    -maxlength => 3
  ),
  radio_group(
    -name    => 'batch_unit',
    -values  => [ 'gal', 'qt', 'c', 'l' ],
    -default => 'gal'
  ),
  br, strong('Pounds of grain '),
  textfield(
    -name      => 'grain',
    -value     => '10',
    -size      => 5,
    -maxlength => 5
  ),
  radio_group(
    -name    => 'grain_unit',
    -values  => [ 'lb', 'oz', 'kg', 'g' ],
    -default => 'lb'
  ),
  br, strong('Minutes boiled '),
  textfield(
    -name      => 'boil',
    -value     => '60',
    -size      => 3,
    -maxlength => 3
  ),
  br, strong('Evaporation Percentage '),
  textfield(
    -name      => 'evap',
    -value     => '10',
    -size      => 2,
    -maxlength => 2
  ),
  strong('%'), br, strong('Loss to Dead Space of Mash Tun '),
  textfield(
    -name      => 'loss',
    -value     => '1',
    -size      => 4,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'loss_unit',
    -values  => [ 'gal', 'qt', 'c', 'l' ],
    -default => 'gal'
  ),
  br, strong('Loss to Trub '),
  textfield(
    -name      => 'trub',
    -value     => '1',
    -size      => 4,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'trub_unit',
    -values  => [ 'gal', 'qt', 'c', 'l' ],
    -default => 'gal'
  ),
  br,
  submit( -value => 'Calculate Water Volume' ),
  end_form;

if (   !param('grain')
    && !param('loss')
    && !param('trub')
    && !param('batch')
    && !param('boil') )
{
    print br,
      strong(
'Please input batch size, grain weight, boil length, evaporation percentage, mash tun loss, and trub amounts'
      );
    die 'No batch, grain, boil, evporation percentage, mash tun loss, or trub entered';
}

if ( param('batch') =~ /^\d+(\.\d{1,3})?$/ ) {
    $batch = param('batch');
}
else {
    print br, strong('Batch volume must be a positive number');
    die 'Batch volume must be a positive number';
}

if ( param('batch_unit') eq 'gal' ) {
    $batch_unit = param('batch_unit');
    $batch      = $batch;
}
elsif ( param('batch_unit') eq 'qt' ) {
    $batch_unit = param('batch_unit');
    $batch      = $batch / 4;
}
elsif ( param('batch_unit') eq 'c' ) {
    $batch_unit = param('batch_unit');
    $batch      = $batch / 16;
}
elsif ( param('batch_unit') eq 'l' ) {
    $batch_unit = param('batch_unit');
    $batch      = $batch * 0.264172052;
}
else {
    print "Batch unit is illegal value";
    die "Batch unit is illegal value";
}

if ( param('grain') =~ /^\d+(\.\d{1,3})?$/ ) {
    $grain = param('grain');
}
else {
    print br, strong('Grain weight must be a positive number');
    die 'Grain weight must be a positive number';
}

if ( param('grain_unit') eq 'lb' ) {
    $grain_unit = param('grain_unit');
    $grain      = $grain;
}
elsif ( param('grain_unit') eq 'oz' ) {
    $grain_unit = param('grain_unit');
    $grain      = $grain / 16;
}
elsif ( param('grain_unit') eq 'kg' ) {
    $grain_unit = param('grain_unit');
    $grain      = $grain * 2.20462262;
}
elsif ( param('grain_unit') eq 'g' ) {
    $grain_unit = param('grain_unit');
    $grain      = $grain * 0.00220462262;
}
else {
    print "Grain unit is illegal value";
    die "Grain unit is illegal value";
}

if ( param('boil') =~ /^\d+(\.\d{1,3})?$/ ) {
    $boil = param('boil');
}
else {
    print br, strong('Minutes boiled must be a positive number');
    die 'Minutes boiled must be a positive number';
}

if ( param('evap') =~ /^\d+(\.\d{1,3})?$/ ) {
    $evap = param('evap') / 100;
}
else {
    print br, strong('Evaporation percentage must be a positive number');
    die 'Evaporation percentage must be a positive number';
}

if ( param('loss') =~ /^\d+(\.\d{1,3})?$/ ) {
    $loss = param('loss');
}
else {
    print br, strong('Mash tun loss must be a positive number');
    die 'Mash tun loss must be a positive number';
}

if ( param('loss_unit') eq 'gal' ) {
    $loss_unit = param('loss_unit');
    $loss      = $loss;
}
elsif ( param('loss_unit') eq 'qt' ) {
    $loss_unit = param('loss_unit');
    $loss      = $loss / 4;
}
elsif ( param('loss_unit') eq 'c' ) {
    $loss_unit = param('loss_unit');
    $loss      = $loss / 16;
}
elsif ( param('loss_unit') eq 'l' ) {
    $loss_unit = param('loss_unit');
    $loss      = $loss * 0.264172052;
}
else {
    print "Mash tun loss unit is illegal value";
    die "Mash tun loss unit is illegal value";
}

if ( param('trub') =~ /^\d+(\.\d{1,3})?$/ ) {
    $trub = param('trub');
}
else {
    print br, strong('Trub must be a positive number');
    die 'Trub must be a positive number';
}

if ( param('trub_unit') eq 'gal' ) {
    $trub_unit = param('trub_unit');
    $trub      = $trub;
}
elsif ( param('trub_unit') eq 'qt' ) {
    $trub_unit = param('trub_unit');
    $trub      = $trub / 4;
}
elsif ( param('trub_unit') eq 'c' ) {
    $trub_unit = param('trub_unit');
    $trub      = $trub / 16;
}
elsif ( param('trub_unit') eq 'l' ) {
    $trub_unit = param('trub_unit');
    $trub      = $trub * 0.264172052;
}
else {
    print "Trub loss unit is illegal value";
    die "Trub loss unit is illegal value";
}

# Grain Loss = Grain volume * 0.1
$GrainLoss = $grain * 0.1;

# Evaporation = 1 - (Percent Evaporation * (Minutes Boiled / 60))
$evaporation = 1 - ( $evap * ( $boil / 60 ) );

# Kettle loss = ((Batch Volume + Loss to trub) / 0.96) / $evaporation
$KettleLoss = ( ( $batch + $trub ) / 0.96 ) / $evaporation;

# Total Water = Kettle Loss + Mash tun loss + Loss to grain absorption
$TotalWater = $KettleLoss + $loss + $GrainLoss;
$TotalWater = sprintf "%.3f", $TotalWater;

# Mash Water = (1.25 * Grain Volume) / 4
$MashWater = ( 1.25 * $grain ) / 4;
$MashWater = sprintf "%.3f", $MashWater;

# Sparge Water = Total Water - Mash Water
$SpargeWater = $TotalWater - $MashWater;
$SpargeWater = sprintf "%.3f", $SpargeWater;

print br, 'Total Water ' . $TotalWater . ' gal';
print br, 'Mash Water ' . $MashWater . ' gal';
print br, 'Sparge Water ' . $SpargeWater . ' gal';

print '</center>';
print end_html;
exit;
