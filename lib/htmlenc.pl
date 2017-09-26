use strict;
use HTML::Entities;

sub htmlenc {
    my $input = shift;

#    $input=~s/&/\&amp;/g;
#    $input=~s/</\&lt;/g;
#    $input=~s/>/\&gt;/g;
#    $input=~s/"/\&#34;/g;
#    $input=~s/=/\&#61;/g;
#    $input=~s/ /\&#160;/g;

    $input = encode_entities($input);
    $input =~s/ /\&#160;/g;
    return $input;

}

1;
