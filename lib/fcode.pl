use strict;

require "lib/files_general.conf";

sub fencode {
        my $VALUE = shift;
        if (defined $VALUE) {
                $VALUE =~ s/$lib::files::general::coldelim1/$lib::files::general::coldelim2/g;
                $VALUE =~ s/$lib::files::general::linedelim1/$lib::files::general::linedelim2/g;
#                $VALUE =~ s/$lib::files::general::dolsign1/$lib::files::general::dolsign2/g;
	        $VALUE=~s/\r//g;
    	        $VALUE=~s/\xA0/ /g;

        }
        return $VALUE;
}
        
sub fdecode {
        my $VALUE = shift;
        if (defined $VALUE) {
                $VALUE =~ s/$lib::files::general::coldelim2/$lib::files::general::coldelim1/g;
                $VALUE =~ s/$lib::files::general::linedelim2/$lib::files::general::linedelim1/g;
#                $VALUE =~ s/$lib::files::general::dolsign2/$lib::files::general::dolsign1/g;
        }
        return $VALUE;
}

1;
