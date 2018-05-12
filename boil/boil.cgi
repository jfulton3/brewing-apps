#!/usr/bin/perl -T
# Calculates post boil gravity
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $pre_volume  = 1;
my $post_volume = 1;
my $pre_sg      = 1.000;
my $post_sg     = 1.000;
my $pre_unit    = 'g';
my $post_unit   = 'g';

print header();
print start_html( -title => 'Calculate Post Boil Gravity' );

print '<center>', br;

print start_form, strong('Volume of Pre Boil Wort'),
  textfield(
    -name      => 'pre_volume',
    -value     => '1',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'pre_unit',
    -values  => [ 'q', 'g', 'l' ],
    -default => 'g'
  ),
  br, strong('Pre Boil Gravity'),
  textfield(
    -name      => 'pre_sg',
    -value     => '1.000',
    -size      => 7,
    -maxlength => 5
  ),
  br, strong('Post Boil Target Volume'),
  textfield(
    -name      => 'post_volume',
    -value     => '1',
    -size      => 3,
    -maxlength => 4
  ),
  radio_group(
    -name    => 'post_unit',
    -values  => [ 'q', 'g', 'l' ],
    -default => 'g'
  ),
  br,
  submit( -value => 'Calculate Post Boil Gravity' ),
  end_form;

if ( !param('pre_volume') && !param('post_volume') && !param('pre_sg') ) {
    print br,
      strong('Please input pre, post volumes and pre boil specific gravity');
    die 'No volume or gravity entered';
}

if ( param('pre_volume') =~ /^\d+(\.\d{1,5})?$/ ) {
    $pre_volume = param('pre_volume');
    if ( param('pre_unit') eq 'g' ) {
        $pre_unit = param('pre_unit');
    }
    elsif ( param('pre_unit') eq 'q' ) {
        $pre_unit   = param('pre_unit');
        $pre_volume = $pre_volume / 4;
    }
    elsif ( param('pre_unit') eq 'l' ) {
        $pre_unit   = param('pre_unit');
        $pre_volume = $pre_volume / 3.785;
    }
    else {
        print "Pre boil volume unit is illegal value";
        die "Pre boil volume unit is illegal value";
    }
}
else {
    print br, strong('Pre boil volume must be a positive number');
    die 'Pre boil volume must be a positive number';
}

if ( param('post_volume') =~ /^\d+(\.\d{1,3})?$/ ) {
    $post_volume = param('post_volume');
    if ( param('post_unit') eq 'g' ) {
        $post_unit = param('post_unit');
    }
    elsif ( param('post_unit') eq 'q' ) {
        $post_unit   = param('post_unit');
        $post_volume = $post_volume / 4;
    }
    elsif ( param('post_unit') eq 'l' ) {
        $post_unit   = param('post_unit');
        $post_volume = $post_volume / 3.785;
    }
    else {
        print "Pre boil volume unit is illegal value";
        die "Pre boil volume unit is illegal value";
    }
}
else {
    print br, strong('Post boil volume must be a positive number');
    die 'Post boil volume must be a positive number';
}

if ( param('pre_sg') =~ /^\d+(\.\d{1,7})?$/ ) {
    $pre_sg = param('pre_sg');
}
else {
    print br, strong('Pre boil gravity must be a positive number');
    die 'Pre boil gravity must be a positive number';
}

$pre_sg  = ( $pre_sg * 1000 ) - 1000;
$post_sg = ( $pre_volume * $pre_sg ) / $post_volume;
$post_sg = sprintf "%.0f", $post_sg;
$post_sg = ( 1000 + $post_sg ) / 1000;
print br, strong( 'Post Boil Gravity: ' . $post_sg );

print '</center>';
print end_html;
exit;
