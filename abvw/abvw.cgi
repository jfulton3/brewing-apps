#!/usr/bin/perl -T
# Calculates alcohol content by weight and volume
# written by John Fulton jfulton3@hotmail.com

use strict;
use warnings;
use diagnostics;
use CGI qw/:standard/;

my $og         = 1;
my $fg         = 1;
my $temp       = 59;
my $temp_unit  = 'F';
my $correction = 0;
my $abv        = 0;
my $abw        = 0;
my $aa         = 0;
my $ra         = 0;
my $pi         = 0;
my $pf         = 0;
my $re         = 0;
my $cal        = 0;
my $bi         = 0;
my $bf         = 0;
my $ri         = 0;
my $rf         = 0;
my $fp         = 0;

print header();
print start_html( -title => 'Calculate Alcohol Content by Weight and Volume' );

print '<center>', br;

print start_form,
  strong('Original Gravity'),
  textfield( -name => 'og', -value => '1.000', -size => 5, -maxlength => 5 ),
  br,
  strong('Final Gravity'),
  textfield( -name => 'fg', -value => '1.000', -size => 5, -maxlength => 5 ),
  br,
  strong('Temperature'),
  textfield( -name => 'temp', -value => '59', -size => 3, -maxlength => 3 ),
  radio_group(
    -name    => 'temp_unit',
    -values  => [ 'C', 'F' ],
    -default => 'F'
  ),
  br,
  submit( -value => 'Calculate ABV and ABW' ),
  end_form;

if ( !param('og') && !param('fg') ) {
    print br, strong('Please input orginal and final gravity');
    die 'No original or final gravity';
}

if ( param('og') =~ /^\d+(\.\d{1,5})?$/ ) {
    $og = param('og');
}
else {
    print br, strong('Original gravity must be a number');
    die 'Original gravity must be a number';
}

if ( param('fg') =~ /^\d+(\.\d{1,5})?$/ ) {
    $fg = param('fg');
}
else {
    print br, strong('Final gravity must be a number');
    die 'Final gravity must be a number';
}

if ( param('temp') =~ /^\d+(\.\d{1,5})?$/ ) {
    $temp = param('temp');
    if ( param('temp_unit') eq 'F' ) {
        $temp_unit = param('temp_unit');
    }
    elsif ( param('temp_unit') eq 'C' ) {
        $temp_unit = param('temp_unit');
        $temp      = ( $temp * 1.8 ) + 32;
    }
    else {
        print "Temperature unit is illegal value";
        die "Temperature unit is illegal value";
    }
}
else {
    print br, strong('Temperature must be a number');
    die 'Temperature must be a number';
}

if ( $og < $fg ) {
    print br,
      strong('Final gravity must be equal or less than original gravity');
    die 'Final gravity must be equal or less than original gravity';
}

if ( $og > 900 ) {
    $og = $og / 1000;
}

if ( $fg > 900 ) {
    $fg = $fg / 1000;
}

if ( $og > 2 ) {
    print br, strong('Original gravity is too high');
    die 'Original gravity is too high';
}

if ( $fg < 0.1 ) {
    print br, strong('Final gravity is too low');
    die 'Final gravity is too low';
}

$correction = (
    (
        (
            1.313454 -
              ( 0.132674 * $temp ) +
              ( 0.002057793 * ( $temp**2 ) ) -
              ( 0.000002627634 * ( $temp**3 ) )
        )
    ) / 1000
);
$og = $og + $correction;
$fg = $fg + $correction;

# Plato = -676.67 + 1286.4*SG - 800.47*SG^2 + 190.74*SG^3
$pi =
  -676.67 +
  ( 1286.4 * $og ) -
  ( 800.47 * ( $og**2 ) ) +
  ( 190.74 * ( $og**3 ) );
$pi = sprintf "%.2f", $pi;
$pf =
  -676.67 +
  ( 1286.4 * $fg ) -
  ( 800.47 * ( $fg**2 ) ) +
  ( 190.74 * ( $fg**3 ) );
$pf = sprintf "%.2f", $pf;
print br, strong( 'Original Gravity Plato: ' . $pi . chr(0x00b0) . 'P' );
print br, strong( 'Final Gravity Plato: ' . $pf . chr(0x00b0) . 'P' ), br;

# Real Extract  = (0.1808 * °Pi) + (0.8192 * °Pf)
$re = ( 0.1808 * $pi ) + ( 0.8192 * $pf );
$re = sprintf "%.2f", $re;
print br, strong( 'Real Extract: ' . $re . chr(0x00b0) . 'P' ), br;

# Brix = 261.3 * (1 - (1 / SG))
$bi = 261.3 * ( 1 - ( 1 / $og ) );
$bi = sprintf "%.2f", $bi;
$bf = 261.3 * ( 1 - ( 1 / $fg ) );
$bf = sprintf "%.2f", $bf;
print br, strong( 'Original Gravity Brix: ' . $bi . chr(0x00b0) . 'Bx' );
print br, strong( 'Final Gravity Brix: ' . $bf . chr(0x00b0) . 'Bx' ), br;

# Refractive Index  = 1.33302 + 0.001427193*Bx + 0.000005791157*Bx^2
$ri = 1.33302 + ( 0.001427193 * $bi ) + 0.000005791157 * ( $bi**2 );
$ri = sprintf "%.2f", $ri;
$rf = 1.33302 + ( 0.001427193 * $bf ) + 0.000005791157 * ( $bf**2 );
$rf = sprintf "%.2f", $rf;
print br, strong( 'Original Refractive Index: ' . $ri );
print br, strong( 'Final Refractive Index: ' . $rf ), br;

# ABV = (OG - FG) / 0.75
# $abv = ( ( $og - $fg ) / 0.75 ) * 100;
# ABV =  ((1.05 * (OG – FG)) / FG) / 0.79
# $abv =  ((1.05 * ($og - $fg)) / $fg) / 0.79;
# ABV =(76.08 * (og-fg) / (1.775-og)) * (fg / 0.794)
$abv = ( 76.08 * ( $og - $fg ) / ( 1.775 - $og ) ) * ( $fg / 0.794 );
$abv = sprintf "%.2f", $abv;
print br, strong( 'Alcohol By Volume: ' . $abv . '%' );

# ABW = (0.79 * ABV) / FG
$abw = ( ( 0.79 * ( $abv / 100 ) ) / $fg ) * 100;
$abw = sprintf "%.2f", $abw;
print br, strong( 'Alcohol By Weight: ' . $abw . '%' );

$aa = ( ( $og - $fg ) / ( $og - 1 ) ) * 100;
$ra = $aa * 0.814;
if ( $aa < 100 ) {
    $aa = sprintf "%.2f", $aa;
}
else {
    $aa = 100;
}
if ( $ra < 100 ) {
    $ra = sprintf "%.2f", $ra;
}
else {
    $ra = 100;
}
print br, br, strong( 'Apparent Attenuation: ' . $aa . '%' );
print br, strong( 'Real Attenuation: ' . $ra . '%' ), br;

# freezing point = (-0.42 * abw) + (0.04 * pi) + 0.2
$fp = ( -0.42 * $abw ) + ( 0.04 * $pi ) + 0.2;
$fp = sprintf "%.2f", $fp;
if ( $temp_unit eq 'C' ) {
    print br, strong( 'Freezing Point: ' . $fp . chr(0x00B0) . 'C' ), br;
}
else {
    $fp = ( $fp * 1.8 ) + 32;
    $fp = sprintf "%.2f", $fp;
    print br, strong( 'Freezing Point: ' . $fp . chr(0x00B0) . 'F' ), br;
}

# calories per 12 oz = ((6.9 * ABW) + 4.0 * (RE - 0.1)) * FG * 3.55
$cal = ( ( 6.9 * $abw ) + 4.0 * ( $re - 0.1 ) ) * $fg * 3.55;
$cal = sprintf "%.2f", $cal;
if ( $cal < 0 ) {
    $cal = 0;
}
print br, strong( 'Calories per 12oz: ' . $cal ), br;

# BJCP Styles
my $c1  = '<span style="color:#000000;background-color:#FFE699">';
my $c2  = '<span style="color:#000000;background-color:#FFD878">';
my $c3  = '<span style="color:#000000;background-color:#FFCA5A">';
my $c4  = '<span style="color:#000000;background-color:#FFBF42">';
my $c5  = '<span style="color:#000000;background-color:#FBB123">';
my $c6  = '<span style="color:#000000;background-color:#F8A600">';
my $c7  = '<span style="color:#ffffff;background-color:#F39C00">';
my $c8  = '<span style="color:#ffffff;background-color:#EA8F00">';
my $c9  = '<span style="color:#ffffff;background-color:#E58500">';
my $c10 = '<span style="color:#ffffff;background-color:#DE7C00">';
my $c11 = '<span style="color:#ffffff;background-color:#D77200">';
my $c12 = '<span style="color:#ffffff;background-color:#CF6900">';
my $c13 = '<span style="color:#ffffff;background-color:#CB6200">';
my $c14 = '<span style="color:#ffffff;background-color:#C35900">';
my $c15 = '<span style="color:#ffffff;background-color:#BB5100">';
my $c16 = '<span style="color:#ffffff;background-color:#B54C00">';
my $c17 = '<span style="color:#ffffff;background-color:#B04500">';
my $c18 = '<span style="color:#ffffff;background-color:#A63E00">';
my $c19 = '<span style="color:#ffffff;background-color:#A13700">';
my $c20 = '<span style="color:#ffffff;background-color:#9B3200">';
my $c21 = '<span style="color:#ffffff;background-color:#952D00">';
my $c22 = '<span style="color:#ffffff;background-color:#8E2900">';
my $c23 = '<span style="color:#ffffff;background-color:#882300">';
my $c24 = '<span style="color:#ffffff;background-color:#821E00">';
my $c25 = '<span style="color:#ffffff;background-color:#7B1A00">';
my $c26 = '<span style="color:#ffffff;background-color:#771900">';
my $c27 = '<span style="color:#ffffff;background-color:#701400">';
my $c28 = '<span style="color:#ffffff;background-color:#6A0E00">';
my $c29 = '<span style="color:#ffffff;background-color:#660D00">';
my $c30 = '<span style="color:#ffffff;background-color:#5E0B00">';
my $c31 = '<span style="color:#ffffff;background-color:#5A0A02">';
my $c32 = '<span style="color:#ffffff;background-color:#600903">';
my $c33 = '<span style="color:#ffffff;background-color:#520907">';
my $c34 = '<span style="color:#ffffff;background-color:#4C0505">';
my $c35 = '<span style="color:#ffffff;background-color:#470606">';
my $c36 = '<span style="color:#ffffff;background-color:#440607">';
my $c37 = '<span style="color:#ffffff;background-color:#3F0708">';
my $c38 = '<span style="color:#ffffff;background-color:#3B0607">';
my $c39 = '<span style="color:#ffffff;background-color:#3A070B">';
my $c40 = '<span style="color:#ffffff;background-color:#36080A">';

# Light Lager
if ( ( $og >= 1.028 ) && ( $og <= 1.04 ) ) {
    if ( ( $fg >= 0.998 ) && ( $fg <= 1.008 ) ) {
        if ( ( $abv >= 2.8 ) && ( $abv <= 4.2 ) ) {
            print br, $c2 . 'Lite Amer</span>' . $c3 . 'ican Lager</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.05 ) ) {
    if ( ( $fg >= 1.004 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 5.3 ) ) {
            print br,
                $c2
              . 'Standard</span>'
              . $c3
              . ' America</span>'
              . $c4
              . 'n Lager</span>';
        }
    }
}
if ( ( $og >= 1.046 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.6 ) && ( $abv <= 6 ) ) {
            print br,
                $c2
              . 'Prem</span>'
              . $c3
              . 'ium </span>'
              . $c4
              . 'Amer</span>'
              . $c5
              . 'ican </span>'
              . $c6
              . 'Lager</span>';
        }
    }
}
if ( ( $og >= 1.045 ) && ( $og <= 1.051 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.7 ) && ( $abv <= 5.4 ) ) {
            print br,
              $c3 . 'Muni</span>' . $c4 . 'ch He</span>' . $c5 . 'lles</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.8 ) && ( $abv <= 6 ) ) {
            print br,
                $c4
              . 'Dortmu</span>'
              . $c5
              . 'nder E</span>'
              . $c6
              . 'xport</span>';
        }
    }
}

# Pilsner
if ( ( $og >= 1.044 ) && ( $og <= 1.05 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 4.4 ) && ( $abv <= 5.2 ) ) {
            print br,
                $c2
              . 'Germa</span>'
              . $c3
              . 'n Pil</span>'
              . $c4
              . 'sner </span>'
              . $c5
              . '(Pils)</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.013 ) && ( $fg <= 1.017 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 5.4 ) ) {
            print br,
                $c3
              . 'Bohe</span>'
              . $c4
              . 'mian</span>'
              . $c5
              . ' Pil</span>'
              . $c6
              . 'sener</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 6 ) ) {
            print br,
                $c3
              . 'Classi</span>'
              . $c4
              . 'c Amer</span>'
              . $c5
              . 'ican P</span>'
              . $c6
              . 'ilsner</span>';
        }
    }
}

# European Amber Lager
if ( ( $og >= 1.046 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.5 ) ) {
            print br,
                $c10
              . 'Vi</span>'
              . $c11
              . 'en</span>'
              . $c12
              . 'na</span>'
              . $c13
              . ' L</span>'
              . $c14
              . 'ag</span>'
              . $c15
              . 'e</span>'
              . $c16
              . 'r</span>';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.057 ) ) {
    if ( ( $fg >= 1.012 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.8 ) && ( $abv <= 5.7 ) ) {
            print br,
                $c7
              . 'Ok</span>'
              . $c8
              . 'to</span>'
              . $c9
              . 'be</span>'
              . $c10
              . 'rf</span>'
              . $c11
              . 'es</span>'
              . $c12
              . 't/</span>'
              . $c13
              . 'Mar</span>'
              . $c14
              . 'zen</span>';
        }
    }
}

# Dark Lager
if ( ( $og >= 1.044 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 6 ) ) {
            print br,
                $c14
              . 'Dar</span>'
              . $c15
              . 'k </span>'
              . $c16
              . 'Am</span>'
              . $c17
              . 'er</span>'
              . $c18
              . 'ic</span>'
              . $c19
              . 'an</span>'
              . $c20
              . ' L</span>'
              . $c21
              . 'ag</span>'
              . $c22
              . 'er</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.6 ) ) {
            print br,
                $c14
              . chr(0x00A0)
              . '</span>'
              . $c15
              . 'M</span>'
              . $c16
              . 'u</span>'
              . $c17
              . 'n</span>'
              . $c18
              . 'i</span>'
              . $c19
              . 'c</span>'
              . $c20
              . 'h</span>'
              . $c21
              . ' </span>'
              . $c22
              . 'D</span>'
              . $c23
              . 'u</span>'
              . $c24
              . 'n</span>'
              . $c25
              . 'k</span>'
              . $c26
              . 'e</span>'
              . $c27
              . 'l</span>'
              . $c28
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.046 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.4 ) && ( $abv <= 5.4 ) ) {
            print br,
                $c17
              . chr(0x00A0)
              . '</span>'
              . $c18
              . 'S</span>'
              . $c19
              . 'c</span>'
              . $c20
              . 'h</span>'
              . $c21
              . 'w</span>'
              . $c22
              . 'a</span>'
              . $c23
              . 'r</span>'
              . $c24
              . 'z</span>'
              . $c25
              . 'b</span>'
              . $c26
              . 'i</span>'
              . $c27
              . 'e</span>'
              . $c28
              . 'r</span>'
              . $c29
              . chr(0x00A0)
              . '</span>'
              . $c30
              . ' </span>';
        }
    }
}

# Bock
if ( ( $og >= 1.064 ) && ( $og <= 1.072 ) ) {
    if ( ( $fg >= 1.011 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 6.3 ) && ( $abv <= 7.4 ) ) {
            print br,
                $c6
              . 'Mai</span>'
              . $c7
              . 'boc</span>'
              . $c8
              . 'k/H</span>'
              . $c9
              . 'ell</span>'
              . $c10
              . 'es </span>'
              . $c11
              . 'Bock</span>';
        }
    }
}
if ( ( $og >= 1.064 ) && ( $og <= 1.072 ) ) {
    if ( ( $fg >= 1.013 ) && ( $fg <= 1.019 ) ) {
        if ( ( $abv >= 6.3 ) && ( $abv <= 7.2 ) ) {
            print br,
                $c14
              . 'Tr</span>'
              . $c15
              . 'ad</span>'
              . $c16
              . 'it</span>'
              . $c17
              . 'io</span>'
              . $c18
              . 'na</span>'
              . $c19
              . 'l </span>'
              . $c20
              . 'Bo</span>'
              . $c21
              . 'c</span>'
              . $c22
              . 'k</span>';
        }
    }
}
if ( ( $og >= 1.072 ) && ( $og <= 1.112 ) ) {
    if ( ( $fg >= 1.016 ) && ( $fg <= 1.024 ) ) {
        if ( ( $abv >= 7 ) && ( $abv <= 10 ) ) {
            print br,
                $c6
              . chr(0x00A0)
              . '</span>'
              . $c7
              . chr(0x00A0)
              . '</span>'
              . $c8
              . chr(0x00A0)
              . '</span>'
              . $c9
              . chr(0x00A0)
              . '</span>'
              . $c10
              . chr(0x00A0)
              . '</span>'
              . $c11
              . 'D</span>'
              . $c12
              . 'o</span>'
              . $c13
              . 'p</span>'
              . $c14
              . 'p</span>'
              . $c15
              . 'e</span>'
              . $c16
              . 'l</span>'
              . $c17
              . 'b</span>'
              . $c18
              . 'o</span>'
              . $c19
              . 'c</span>'
              . $c20
              . 'k</span>'
              . $c21
              . chr(0x00A0)
              . '</span>'
              . $c22
              . chr(0x00A0)
              . '</span>'
              . $c23
              . chr(0x00A0)
              . '</span>'
              . $c24
              . chr(0x00A0)
              . '</span>'
              . $c25
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.078 ) && ( $og <= 1.12 ) ) {
    if ( ( $fg >= 1.02 ) && ( $fg <= 1.035 ) ) {
        if ( ( $abv >= 9 ) && ( $abv <= 14 ) ) {
            print br,
                $c18
              . chr(0x00A0)
              . '</span>'
              . $c19
              . chr(0x00A0)
              . '</span>'
              . $c20
              . chr(0x00A0)
              . '</span>'
              . $c21
              . 'E</span>'
              . $c22
              . 'i</span>'
              . $c23
              . 's</span>'
              . $c24
              . 'b</span>'
              . $c25
              . 'o</span>'
              . $c26
              . 'c</span>'
              . $c27
              . 'k</span>'
              . $c28
              . chr(0x00A0)
              . '</span>'
              . $c29
              . chr(0x00A0)
              . '</span>'
              . $c30
              . chr(0x00A0)
              . '</span>';
        }
    }
}

# Light Hybrid Beer
if ( ( $og >= 1.042 ) && ( $og <= 1.055 ) ) {
    if ( ( $fg >= 1.006 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 5.6 ) ) {
            print br,
                $c2
              . 'Cre</span>'
              . $c3
              . 'am</span>'
              . $c4
              . ' A</span>'
              . $c5
              . 'le</span>';
        }
    }
}
if ( ( $og >= 1.038 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 3.8 ) && ( $abv <= 5.5 ) ) {
            print br,
                $c3
              . 'Blo</span>'
              . $c4
              . 'nde</span>'
              . $c5
              . ' A</span>'
              . $c6
              . 'le</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.05 ) ) {
    if ( ( $fg >= 1.007 ) && ( $fg <= 1.011 ) ) {
        if ( ( $abv >= 4.4 ) && ( $abv <= 5.2 ) ) {
            print br, $c3 . 'Ko</span>' . $c4 . 'ls</span>' . $c5 . 'ch</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.055 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 5.5 ) ) {
            print br,
                $c3
              . 'America</span>'
              . $c4
              . 'n Wheat</span>'
              . $c5
              . ' or Ry</span>'
              . $c6
              . 'e Beer</span>';
        }
    }
}

# Amber Hybrid Beer
if ( ( $og >= 1.046 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.2 ) ) {
            print br,
                $c13
              . 'Nort</span>'
              . $c14
              . 'hern</span>'
              . $c15
              . ' Ge</span>'
              . $c16
              . 'rma</span>'
              . $c17
              . 'n A</span>'
              . $c18
              . 'ltb</span>'
              . $c19
              . 'ier</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.011 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.5 ) ) {
            print br,
                $c10
              . 'Calif</span>'
              . $c11
              . 'ornia</span>'
              . $c12
              . ' Com</span>'
              . $c13
              . 'mon </span>'
              . $c14
              . 'Beer</span>';
        }
    }
}
if ( ( $og >= 1.046 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.2 ) ) {
            print br,
                $c10
              . 'Duss</span>'
              . $c11
              . 'eldo</span>'
              . $c12
              . 'rf A</span>'
              . $c13
              . 'ltb</span>'
              . $c14
              . 'ier</span>';
        }
    }
}

# English Pale Ale
if ( ( $og >= 1.032 ) && ( $og <= 1.04 ) ) {
    if ( ( $fg >= 1.007 ) && ( $fg <= 1.011 ) ) {
        if ( ( $abv >= 3.2 ) && ( $abv <= 3.8 ) ) {
            print br,
                $c4
              . 'St</span>'
              . $c5
              . 'an</span>'
              . $c6
              . 'da</span>'
              . $c7
              . 'rd</span>'
              . $c8
              . '/O</span>'
              . $c9
              . 'rd</span>'
              . $c10
              . 'in</span>'
              . $c11
              . 'ar</span>'
              . $c12
              . 'y </span>'
              . $c13
              . 'Bit</span>'
              . $c14
              . 'ter</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.048 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 3.8 ) && ( $abv <= 4.6 ) ) {
            print br,
                $c5
              . 'Spe</span>'
              . $c6
              . 'cia</span>'
              . $c7
              . 'l/B</span>'
              . $c8
              . 'es</span>'
              . $c9
              . 't/</span>'
              . $c10
              . 'Pr</span>'
              . $c11
              . 'em</span>'
              . $c12
              . 'iu</span>'
              . $c13
              . 'm </span>'
              . $c14
              . 'Bi</span>'
              . $c15
              . 'tt</span>'
              . $c16
              . 'er</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.6 ) && ( $abv <= 6.2 ) ) {
            print br,
                $c6
              . 'Extr</span>'
              . $c7
              . 'a Sp</span>'
              . $c8
              . 'ecia</span>'
              . $c9
              . 'l/S</span>'
              . $c10
              . 'tro</span>'
              . $c11
              . 'ng </span>'
              . $c12
              . 'Bit</span>'
              . $c13
              . 'ter</span>'
              . $c14
              . ' (E</span>'
              . $c15
              . 'ngl</span>'
              . $c16
              . 'ish </span>'
              . $c17
              . 'Pale</span>'
              . $c18
              . ' Ale)</span>';
        }
    }
}

# Scottish and Irish Ale
if ( ( $og >= 1.03 ) && ( $og <= 1.035 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 2.5 ) && ( $abv <= 3.2 ) ) {
            print br,
                $c9
              . 'Sco</span>'
              . $c10
              . 'tt</span>'
              . $c11
              . 'is</span>'
              . $c12
              . 'h </span>'
              . $c13
              . 'Li</span>'
              . $c14
              . 'gh</span>'
              . $c15
              . 't </span>'
              . $c16
              . '60</span>'
              . $c17
              . '/-</span>';
        }
    }
}
if ( ( $og >= 1.035 ) && ( $og <= 1.04 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 3.2 ) && ( $abv <= 3.9 ) ) {
            print br,
                $c9
              . 'Sco</span>'
              . $c10
              . 'tt</span>'
              . $c11
              . 'is</span>'
              . $c12
              . 'h </span>'
              . $c13
              . 'He</span>'
              . $c14
              . 'av</span>'
              . $c15
              . 'y </span>'
              . $c16
              . '70</span>'
              . $c17
              . '/-</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 3.9 ) && ( $abv <= 5 ) ) {
            print br,
                $c9
              . 'Sco</span>'
              . $c10
              . 'tt</span>'
              . $c11
              . 'is</span>'
              . $c12
              . 'h </span>'
              . $c13
              . 'Ex</span>'
              . $c14
              . 'po</span>'
              . $c15
              . 'rt</span>'
              . $c16
              . ' 8</span>'
              . $c17
              . '0/-</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 6 ) ) {
            print br,
                $c9
              . 'Ir</span>'
              . $c10
              . 'is</span>'
              . $c11
              . 'h</span>'
              . $c12
              . ' </span>'
              . $c13
              . 'R</span>'
              . $c14
              . 'e</span>'
              . $c15
              . 'd</span>'
              . $c16
              . ' </span>'
              . $c17
              . 'A</span>'
              . $c18
              . 'le</span>';
        }
    }
}
if ( ( $og >= 1.07 ) && ( $og <= 1.13 ) ) {
    if ( ( $fg >= 1.018 ) && ( $fg <= 1.056 ) ) {
        if ( ( $abv >= 6.5 ) && ( $abv <= 10 ) ) {
            print br,
                $c14
              . 'St</span>'
              . $c15
              . 'ro</span>'
              . $c16
              . 'ng</span>'
              . $c17
              . ' </span>'
              . $c18
              . 'S</span>'
              . $c19
              . 'c</span>'
              . $c20
              . 'o</span>'
              . $c21
              . 't</span>'
              . $c22
              . 'c</span>'
              . $c23
              . 'h</span>'
              . $c24
              . ' A</span>'
              . $c25
              . 'le</span>';
        }
    }
}

# American Ale
if ( ( $og >= 1.045 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 6.2 ) ) {
            print br,
                $c5
              . 'Am</span>'
              . $c6
              . 'er</span>'
              . $c7
              . 'ic</span>'
              . $c8
              . 'an</span>'
              . $c9
              . ' Pa</span>'
              . $c10
              . 'l</span>'
              . $c11
              . 'e</span>'
              . $c12
              . ' </span>'
              . $c13
              . 'A</span>'
              . $c14
              . 'l</span>'
              . $c15
              . 'e</span>';
        }
    }
}
if ( ( $og >= 1.045 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.015 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 6.2 ) ) {
            print br,
                $c10
              . 'Am</span>'
              . $c11
              . 'er</span>'
              . $c12
              . 'ic</span>'
              . $c13
              . 'an</span>'
              . $c14
              . ' A</span>'
              . $c15
              . 'mb</span>'
              . $c16
              . 'er </span>'
              . $c17
              . 'Ale</span>';
        }
    }
}
if ( ( $og >= 1.045 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.3 ) && ( $abv <= 6.2 ) ) {
            print br,
                $c18
              . 'A</span>'
              . $c19
              . 'm</span>'
              . $c20
              . 'e</span>'
              . $c21
              . 'r</span>'
              . $c22
              . 'i</span>'
              . $c23
              . 'c</span>'
              . $c24
              . 'a</span>'
              . $c25
              . 'n</span>'
              . $c26
              . ' </span>'
              . $c27
              . 'B</span>'
              . $c28
              . 'r</span>'
              . $c29
              . 'o</span>'
              . $c30
              . 'w</span>'
              . $c31
              . 'n</span>'
              . $c32
              . ' </span>'
              . $c33
              . 'A</span>'
              . $c34
              . 'l</span>'
              . $c35
              . 'e</span>';
        }
    }
}

# English Brown Ale
if ( ( $og >= 1.03 ) && ( $og <= 1.038 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 2.8 ) && ( $abv <= 4.5 ) ) {
            print br,
                $c12
              . 'Mi</span>'
              . $c13
              . 'ld</span>'
              . $c14
              . ' E</span>'
              . $c15
              . 'n</span>'
              . $c16
              . 'g</span>'
              . $c17
              . 'l</span>'
              . $c18
              . 'i</span>'
              . $c19
              . 's</span>'
              . $c20
              . 'h</span>'
              . $c21
              . ' B</span>'
              . $c22
              . 'ro</span>'
              . $c23
              . 'wn</span>'
              . $c24
              . ' A</span>'
              . $c25
              . 'le</span>';
        }
    }
}
if ( ( $og >= 1.033 ) && ( $og <= 1.042 ) ) {
    if ( ( $fg >= 1.011 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 2.8 ) && ( $abv <= 4.1 ) ) {
            print br,
                $c19
              . 'So</span>'
              . $c20
              . 'ut</span>'
              . $c21
              . 'he</span>'
              . $c22
              . 'rn</span>'
              . $c23
              . ' </span>'
              . $c24
              . 'E</span>'
              . $c25
              . 'n</span>'
              . $c26
              . 'g</span>'
              . $c27
              . 'l</span>'
              . $c28
              . 'i</span>'
              . $c29
              . 's</span>'
              . $c30
              . 'h</span>'
              . $c31
              . ' B</span>'
              . $c32
              . 'ro</span>'
              . $c33
              . 'wn</span>'
              . $c34
              . ' A</span>'
              . $c35
              . 'le</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.013 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 5.4 ) ) {
            print br,
                $c12
              . 'No</span>'
              . $c13
              . 'rt</span>'
              . $c14
              . 'he</span>'
              . $c15
              . 'rn</span>'
              . $c16
              . ' E</span>'
              . $c17
              . 'ng</span>'
              . $c18
              . 'li</span>'
              . $c19
              . 'sh </span>'
              . $c20
              . 'Bro</span>'
              . $c21
              . 'wn </span>'
              . $c22
              . 'Ale</span>';
        }
    }
}

# Porter
if ( ( $og >= 1.04 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 5.4 ) ) {
            print br,
                $c20
              . 'Br</span>'
              . $c21
              . 'o</span>'
              . $c22
              . 'w</span>'
              . $c23
              . 'n</span>'
              . $c24
              . ' </span>'
              . $c25
              . 'P</span>'
              . $c26
              . 'o</span>'
              . $c27
              . 'r</span>'
              . $c28
              . 't</span>'
              . $c29
              . 'e</span>'
              . $c30
              . 'r</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.065 ) ) {
    if ( ( $fg >= 1.012 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.8 ) && ( $abv <= 6.5 ) ) {
            print br,
                $c22
              . 'R</span>'
              . $c23
              . 'o</span>'
              . $c24
              . 'b</span>'
              . $c25
              . 'u</span>'
              . $c26
              . 's</span>'
              . $c27
              . 't</span>'
              . $c28
              . ' </span>'
              . $c29
              . 'P</span>'
              . $c30
              . 'o</span>'
              . $c31
              . 'r</span>'
              . $c32
              . 't</span>'
              . $c33
              . 'e</span>'
              . $c34
              . 'r</span>'
              . $c35
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.06 ) && ( $og <= 1.09 ) ) {
    if ( ( $fg >= 1.016 ) && ( $fg <= 1.024 ) ) {
        if ( ( $abv >= 5.5 ) && ( $abv <= 9.5 ) ) {
            print br,
                $c17
              . 'B</span>'
              . $c18
              . 'a</span>'
              . $c19
              . 'l</span>'
              . $c20
              . 't</span>'
              . $c21
              . 'i</span>'
              . $c22
              . 'c</span>'
              . $c23
              . ' </span>'
              . $c24
              . 'P</span>'
              . $c25
              . 'o</span>'
              . $c26
              . 'r</span>'
              . $c27
              . 't</span>'
              . $c28
              . 'e</span>'
              . $c29
              . 'r</span>'
              . $c30
              . chr(0x00A0)
              . '</span>';
        }
    }
}

# Stout
if ( ( $og >= 1.036 ) && ( $og <= 1.05 ) ) {
    if ( ( $fg >= 1.007 ) && ( $fg <= 1.011 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 5 ) ) {
            print br,
                $c25
              . chr(0x00A0)
              . '</span>'
              . $c26
              . chr(0x00A0)
              . '</span>'
              . $c27
              . chr(0x00A0)
              . '</span>'
              . $c28
              . 'D</span>'
              . $c29
              . 'r</span>'
              . $c30
              . 'y</span>'
              . $c31
              . ' </span>'
              . $c32
              . 'S</span>'
              . $c33
              . 't</span>'
              . $c34
              . 'o</span>'
              . $c35
              . 'u</span>'
              . $c36
              . 't</span>'
              . $c37
              . chr(0x00A0)
              . '</span>'
              . $c38
              . chr(0x00A0)
              . '</span>'
              . $c39
              . chr(0x00A0)
              . '</span>'
              . $c40
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1.012 ) && ( $fg <= 1.024 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 6 ) ) {
            print br,
                $c30
              . 'S</span>'
              . $c31
              . 'w</span>'
              . $c32
              . 'e</span>'
              . $c33
              . 'e</span>'
              . $c34
              . 't</span>'
              . $c35
              . ' </span>'
              . $c36
              . 'S</span>'
              . $c37
              . 't</span>'
              . $c38
              . 'o</span>'
              . $c39
              . 'u</span>'
              . $c40
              . 't</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.065 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 4.2 ) && ( $abv <= 5.9 ) ) {
            print br,
                $c22
              . chr(0x00A0)
              . '</span>'
              . $c23
              . chr(0x00A0)
              . '</span>'
              . $c24
              . chr(0x00A0)
              . '</span>'
              . $c25
              . 'O</span>'
              . $c26
              . 'a</span>'
              . $c27
              . 't</span>'
              . $c28
              . 'm</span>'
              . $c29
              . 'e</span>'
              . $c30
              . 'a</span>'
              . $c31
              . 'l</span>'
              . $c32
              . ' </span>'
              . $c33
              . 'S</span>'
              . $c34
              . 't</span>'
              . $c35
              . 'o</span>'
              . $c36
              . 'u</span>'
              . $c37
              . 't</span>'
              . $c38
              . chr(0x00A0)
              . '</span>'
              . $c39
              . chr(0x00A0)
              . '</span>'
              . $c40
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.056 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 5.5 ) && ( $abv <= 8 ) ) {
            print br,
                $c30
              . 'Fo</span>'
              . $c31
              . 're</span>'
              . $c32
              . 'ig</span>'
              . $c33
              . 'n </span>'
              . $c34
              . 'Ex</span>'
              . $c35
              . 'tr</span>'
              . $c36
              . 'a </span>'
              . $c37
              . 'St</span>'
              . $c38
              . 'o</span>'
              . $c39
              . 'u</span>'
              . $c40
              . 't</span>';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.022 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 7 ) ) {
            print br,
                $c30
              . 'Am</span>'
              . $c31
              . 'er</span>'
              . $c32
              . 'i</span>'
              . $c33
              . 'c</span>'
              . $c34
              . 'a</span>'
              . $c35
              . 'n</span>'
              . $c36
              . ' </span>'
              . $c37
              . 'S</span>'
              . $c38
              . 't</span>'
              . $c39
              . 'o</span>'
              . $c40
              . 'ut</span>';
        }
    }
}
if ( ( $og >= 1.075 ) && ( $og <= 1.115 ) ) {
    if ( ( $fg >= 1.018 ) && ( $fg <= 1.03 ) ) {
        if ( ( $abv >= 8 ) && ( $abv <= 12 ) ) {
            print br,
                $c30
              . 'Ru</span>'
              . $c31
              . 'ss</span>'
              . $c32
              . 'ia</span>'
              . $c33
              . 'n </span>'
              . $c34
              . 'Im</span>'
              . $c35
              . 'pe</span>'
              . $c36
              . 'ri</span>'
              . $c37
              . 'al</span>'
              . $c38
              . ' S</span>'
              . $c39
              . 'to</span>'
              . $c40
              . 'ut</span>';
        }
    }
}

# India Pale Ale (IPA)
if ( ( $og >= 1.05 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 7.5 ) ) {
            print br,
                $c8
              . 'En</span>'
              . $c9
              . 'gl</span>'
              . $c10
              . 'i</span>'
              . $c11
              . 's</span>'
              . $c12
              . 'h</span>'
              . $c13
              . ' </span>'
              . $c14
              . 'I</span>'
              . $c15
              . 'PA</span>';
        }
    }
}
if ( ( $og >= 1.056 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 5.5 ) && ( $abv <= 7.5 ) ) {
            print br,
                $c6
              . 'Am</span>'
              . $c7
              . 'e</span>'
              . $c8
              . 'r</span>'
              . $c9
              . 'i</span>'
              . $c10
              . 'c</span>'
              . $c11
              . 'a</span>'
              . $c13
              . 'n</span>'
              . $c14
              . ' I</span>'
              . $c15
              . 'PA</span>';
        }
    }
}
if ( ( $og >= 1.07 ) && ( $og <= 1.09 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 7.5 ) && ( $abv <= 10 ) ) {
            print br,
                $c8
              . 'Im</span>'
              . $c9
              . 'pe</span>'
              . $c10
              . 'r</span>'
              . $c11
              . 'i</span>'
              . $c12
              . 'a</span>'
              . $c13
              . 'l</span>'
              . $c14
              . ' I</span>'
              . $c15
              . 'PA</span>';
        }
    }
}

# German Wheat and Rye Beer
if ( ( $og >= 1.044 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.3 ) && ( $abv <= 5.6 ) ) {
            print br,
                $c2
              . 'Wei</span>'
              . $c3
              . 'ze</span>'
              . $c4
              . 'n/</span>'
              . $c5
              . 'We</span>'
              . $c6
              . 'is</span>'
              . $c7
              . 'sb</span>'
              . $c8
              . 'ier</span>';
        }
    }
}
if ( ( $og >= 1.044 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.3 ) && ( $abv <= 5.6 ) ) {
            print br,
                $c14
              . 'Du</span>'
              . $c15
              . 'n</span>'
              . $c16
              . 'k</span>'
              . $c17
              . 'e</span>'
              . $c18
              . 'l</span>'
              . $c19
              . 'w</span>'
              . $c20
              . 'e</span>'
              . $c21
              . 'i</span>'
              . $c22
              . 'z</span>'
              . $c23
              . 'en</span>';
        }
    }
}
if ( ( $og >= 1.064 ) && ( $og <= 1.09 ) ) {
    if ( ( $fg >= 1.015 ) && ( $fg <= 1.022 ) ) {
        if ( ( $abv >= 6.5 ) && ( $abv <= 8 ) ) {
            print br,
                $c12
              . chr(0x00A0)
              . '</span>'
              . $c13
              . chr(0x00A0)
              . '</span>'
              . $c14
              . 'W</span>'
              . $c15
              . 'e</span>'
              . $c16
              . 'i</span>'
              . $c17
              . 'z</span>'
              . $c18
              . 'e</span>'
              . $c19
              . 'n</span>'
              . $c20
              . 'b</span>'
              . $c21
              . 'o</span>'
              . $c22
              . 'c</span>'
              . $c23
              . 'k</span>'
              . $c24
              . chr(0x00A0)
              . '</span>'
              . $c25
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.046 ) && ( $og <= 1.056 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 6 ) ) {
            print br,
                $c14
              . 'Rogge</span>'
              . $c15
              . 'nbie</span>'
              . $c16
              . 'r (G</span>'
              . $c17
              . 'erma</span>'
              . $c18
              . 'n Rye</span>'
              . $c19
              . ' Beer)</span>';
        }
    }
}

# Belgian and French Ale
if ( ( $og >= 1.044 ) && ( $og <= 1.052 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.5 ) && ( $abv <= 5.5 ) ) {
            print br,
              $c2 . 'Wit</span>' . $c3 . 'bi</span>' . $c4 . 'er</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 4.8 ) && ( $abv <= 5.5 ) ) {
            print br,
                $c8
              . 'Bel</span>'
              . $c9
              . 'gi</span>'
              . $c10
              . 'an</span>'
              . $c11
              . ' P</span>'
              . $c12
              . 'al</span>'
              . $c13
              . 'e </span>'
              . $c14
              . 'Ale</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.065 ) ) {
    if ( ( $fg >= 1.002 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 7 ) ) {
            print br,
                $c5
              . chr(0x00A0)
              . '</span>'
              . $c6
              . chr(0x00A0)
              . '</span>'
              . $c7
              . 'S</span>'
              . $c8
              . 'a</span>'
              . $c9
              . 'i</span>'
              . $c10
              . 's</span>'
              . $c11
              . 'o</span>'
              . $c12
              . 'n</span>'
              . $c13
              . chr(0x00A0)
              . '</span>'
              . $c14
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.06 ) && ( $og <= 1.08 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 6 ) && ( $abv <= 8.5 ) ) {
            print br,
                $c6
              . 'B</span>'
              . $c7
              . 'i</span>'
              . $c8
              . 'e</span>'
              . $c9
              . 'r</span>'
              . $c10
              . 'e</span>'
              . $c11
              . ' </span>'
              . $c12
              . 'd</span>'
              . $c13
              . 'e</span>'
              . $c14
              . ' </span>'
              . $c15
              . 'G</span>'
              . $c16
              . 'a</span>'
              . $c17
              . 'r</span>'
              . $c18
              . 'd</span>'
              . $c19
              . 'e</span>';
        }
    }
}

# Sour Ale
if ( ( $og >= 1.028 ) && ( $og <= 1.032 ) ) {
    if ( ( $fg >= 1.003 ) && ( $fg <= 1.006 ) ) {
        if ( ( $abv >= 2.8 ) && ( $abv <= 3.8 ) ) {
            print br, $c2 . 'Berliner</span>' . $c3 . ' Weisse</span>';
        }
    }
}
if ( ( $og >= 1.048 ) && ( $og <= 1.057 ) ) {
    if ( ( $fg >= 1.002 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4.6 ) && ( $abv <= 6.5 ) ) {
            print br,
                $c10
              . 'Fla</span>'
              . $c11
              . 'nd</span>'
              . $c12
              . 'er</span>'
              . $c13
              . 's </span>'
              . $c14
              . 'Re</span>'
              . $c15
              . 'd </span>'
              . $c16
              . 'Ale</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.074 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.012 ) ) {
        if ( ( $abv >= 4 ) && ( $abv <= 8 ) ) {
            print br,
                $c15
              . 'Fla</span>'
              . $c16
              . 'nde</span>'
              . $c17
              . 'rs </span>'
              . $c18
              . 'Bro</span>'
              . $c19
              . 'wn A</span>'
              . $c20
              . 'le/O</span>'
              . $c21
              . 'ud B</span>'
              . $c22
              . 'ruin</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.054 ) ) {
    if ( ( $fg >= 1.001 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 6.5 ) ) {
            print br,
                $c3
              . 'Straig</span>'
              . $c4
              . 'ht (U</span>'
              . $c5
              . 'nblen</span>'
              . $c6
              . 'ded) </span>'
              . $c7
              . 'Lambic</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1 ) && ( $fg <= 1.006 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 8 ) ) {
            print br,
                $c3
              . 'Gu</span>'
              . $c4
              . 'e</span>'
              . $c5
              . 'u</span>'
              . $c6
              . 'z</span>'
              . $c7
              . 'e</span>';
        }
    }
}
if ( ( $og >= 1.04 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 7 ) ) {
            print br,
                $c3
              . 'Fr</span>'
              . $c4
              . 'ui</span>'
              . $c5
              . 't </span>'
              . $c6
              . 'Lam</span>'
              . $c7
              . 'bic</span>';
        }
    }
}

# Belgian Strong Ale
if ( ( $og >= 1.062 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 6 ) && ( $abv <= 7.5 ) ) {
            print br,
                $c4
              . 'Belg</span>'
              . $c5
              . 'ian </span>'
              . $c6
              . 'Blon</span>'
              . $c7
              . 'd Ale</span>';
        }
    }
}
if ( ( $og >= 1.062 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.018 ) ) {
        if ( ( $abv >= 6 ) && ( $abv <= 7.6 ) ) {
            print br,
                $c10
              . 'Be</span>'
              . $c11
              . 'lg</span>'
              . $c12
              . 'i</span>'
              . $c13
              . 'a</span>'
              . $c14
              . 'n </span>'
              . $c15
              . 'Du</span>'
              . $c16
              . 'bb</span>'
              . $c17
              . 'el</span>';
        }
    }
}
if ( ( $og >= 1.075 ) && ( $og <= 1.085 ) ) {
    if ( ( $fg >= 1.008 ) && ( $fg <= 1.014 ) ) {
        if ( ( $abv >= 7.5 ) && ( $abv <= 9.5 ) ) {
            print br,
                $c4
              . 'Bel</span>'
              . $c5
              . 'gia</span>'
              . $c6
              . 'n Tr</span>'
              . $c7
              . 'ipel</span>';
        }
    }
}
if ( ( $og >= 1.07 ) && ( $og <= 1.095 ) ) {
    if ( ( $fg >= 1.005 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 7.5 ) && ( $abv <= 10.5 ) ) {
            print br,
                $c3
              . 'Belgia</span>'
              . $c4
              . 'n Gold</span>'
              . $c5
              . 'en Str</span>'
              . $c6
              . 'ong Ale</span>';
        }
    }
}
if ( ( $og >= 1.075 ) && ( $og <= 1.11 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.024 ) ) {
        if ( ( $abv >= 8 ) && ( $abv <= 11 ) ) {
            print br,
                $c12
              . 'Bel</span>'
              . $c13
              . 'gi</span>'
              . $c14
              . 'an</span>'
              . $c15
              . ' D</span>'
              . $c16
              . 'ar</span>'
              . $c17
              . 'k </span>'
              . $c18
              . 'St</span>'
              . $c19
              . 'ro</span>'
              . $c20
              . 'ng</span>'
              . $c21
              . ' A</span>'
              . $c22
              . 'le</span>';
        }
    }
}

# Strong Ale
if ( ( $og >= 1.06 ) && ( $og <= 1.09 ) ) {
    if ( ( $fg >= 1.015 ) && ( $fg <= 1.022 ) ) {
        if ( ( $abv >= 6 ) && ( $abv <= 9 ) ) {
            print br,
                $c10
              . chr(0x00A0)
              . '</span>'
              . $c11
              . chr(0x00A0)
              . '</span>'
              . $c12
              . chr(0x00A0)
              . '</span>'
              . $c13
              . 'O</span>'
              . $c14
              . 'l</span>'
              . $c15
              . 'd</span>'
              . $c16
              . ' </span>'
              . $c17
              . 'A</span>'
              . $c18
              . 'l</span>'
              . $c19
              . 'e</span>'
              . $c20
              . chr(0x00A0)
              . '</span>'
              . $c21
              . chr(0x00A0)
              . '</span>'
              . $c22
              . chr(0x00A0)
              . '</span>';
        }
    }
}
if ( ( $og >= 1.08 ) && ( $og <= 1.12 ) ) {
    if ( ( $fg >= 1.018 ) && ( $fg <= 1.03 ) ) {
        if ( ( $abv >= 8 ) && ( $abv <= 12 ) ) {
            print br,
                $c8
              . 'E</span>'
              . $c9
              . 'n</span>'
              . $c10
              . 'g</span>'
              . $c11
              . 'l</span>'
              . $c12
              . 'i</span>'
              . $c13
              . 's</span>'
              . $c14
              . 'h</span>'
              . $c15
              . ' </span>'
              . $c16
              . 'B</span>'
              . $c17
              . 'a</span>'
              . $c18
              . 'r</span>'
              . $c19
              . 'l</span>'
              . $c20
              . 'ey</span>'
              . $c21
              . 'wi</span>'
              . $c22
              . 'ne</span>';
        }
    }
}
if ( ( $og >= 1.08 ) && ( $og <= 1.12 ) ) {
    if ( ( $fg >= 1.016 ) && ( $fg <= 1.03 ) ) {
        if ( ( $abv >= 8 ) && ( $abv <= 12 ) ) {
            print br,
                $c10
              . 'Am</span>'
              . $c11
              . 'er</span>'
              . $c12
              . 'ic</span>'
              . $c13
              . 'a</span>'
              . $c14
              . 'n </span>'
              . $c15
              . 'Ba</span>'
              . $c16
              . 'rl</span>'
              . $c17
              . 'ey</span>'
              . $c18
              . 'wi</span>'
              . $c19
              . 'ne</span>';
        }
    }
}

# Smoke-Flavored and Wood Aged Beer
if ( ( $og >= 1.05 ) && ( $og <= 1.057 ) ) {
    if ( ( $fg >= 1.012 ) && ( $fg <= 1.016 ) ) {
        if ( ( $abv >= 4.8 ) && ( $abv <= 6 ) ) {
            print br,
                $c12
              . 'Cl</span>'
              . $c13
              . 'as</span>'
              . $c14
              . 's</span>'
              . $c15
              . 'i</span>'
              . $c16
              . 'c</span>'
              . $c17
              . ' </span>'
              . $c18
              . 'Ra</span>'
              . $c19
              . 'uc</span>'
              . $c20
              . 'hb</span>'
              . $c21
              . 'ie</span>'
              . $c22
              . 'r</span>';
        }
    }
}

#Standard Cider and Perry
if ( ( $og >= 1.045 ) && ( $og <= 1.065 ) ) {
    if ( ( $fg >= 1 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 8 ) ) {
            print br, 'Common Cider';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.075 ) ) {
    if ( ( $fg >= 0.995 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 6 ) && ( $abv <= 9 ) ) {
            print br, 'English Cider';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.065 ) ) {
    if ( ( $fg >= 1.01 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 3 ) && ( $abv <= 6 ) ) {
            print br, 'French Cider';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.06 ) ) {
    if ( ( $fg >= 1 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 7 ) ) {
            print br, 'Common Perry';
        }
    }
}
if ( ( $og >= 1.05 ) && ( $og <= 1.07 ) ) {
    if ( ( $fg >= 1 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 9 ) ) {
            print br, 'Traditional Perry';
        }
    }
}

# Specialty Cider and Perry
if ( ( $og >= 1.06 ) && ( $og <= 1.1 ) ) {
    if ( ( $fg >= 0.995 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 7 ) && ( $abv <= 13 ) ) {
            print br, 'New England Cider';
        }
    }
}
if ( ( $og >= 1.045 ) && ( $og <= 1.07 ) ) {
    if ( ( $fg >= 0.995 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 9 ) ) {
            print br, 'Fruit Cider';
        }
    }
}
if ( ( $og >= 1.07 ) && ( $og <= 1.1 ) ) {
    if ( ( $fg >= 0.995 ) && ( $fg <= 1.01 ) ) {
        if ( ( $abv >= 9 ) && ( $abv <= 12 ) ) {
            print br, 'Applewine';
        }
    }
}
if ( ( $og >= 1.045 ) && ( $og <= 1.1 ) ) {
    if ( ( $fg >= 0.995 ) && ( $fg <= 1.02 ) ) {
        if ( ( $abv >= 5 ) && ( $abv <= 12 ) ) {
            print br, 'Other Specialty Cider/Perry';
        }
    }
}

print '</center>';
print end_html;
exit;
