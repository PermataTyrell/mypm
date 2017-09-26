# Search line(s) from flat database, or whole database.
#
#
# Parameters:
#
# 0: filename
# 1: line ID (first variable).
# 2: Col number. If want to select some other col than 0 when
#    selecting rows at $_[1]
# 3: Match multiple lines. This parameter is at the same time
#    maximum number of matches.
# 4: Line number, first is 1. If this is set, $_[1] can't be set
#
# Returns: lines
#
######################################################################

use strict;             

require "lib/files_general.conf";
require "lib/logit.pl";

sub fdbread {
	my $file          = shift;
	my $id            = shift;
	my $col           = shift;
	my $multiplelines = shift;
	my $linen         = shift;

	if ($col eq "") { $col  = 0; }

	if (!-e $file) {
		## File not found
		&logit("$file not found", "file","sys");
		return undef;
	}

	my @data = ();
	local *DBREAD;

	if (!$id && !$linen) {
		## Whole db
		if (-s $file > $lib::files::general::maxdbsize) {
			&logit("Too big db: $file - check your configuration or file may be corrupted ", "error","sys");
			return undef;
		}
		open (DBREAD, "<$file") || goto ERR;
		flock (DBREAD, 1) || goto ERR;
		#$/ = "";
		my $alldata;
		while(<DBREAD>) { $alldata.= $_; }
		#$/ = "\n";
		close DBREAD;
		return $alldata;
	} else {
		open (DBREAD, "<$file") || goto ERR;
		flock (DBREAD, 1) || goto ERR;
		while (<DBREAD>) {
			my @info = split(/:/);

			if ($id ne "") {
				if ($info[$col] eq $id) {
					if ($multiplelines) {
						push (@data, $_);
						$multiplelines--;
						if (!$multiplelines) { last; }
					} else {
						close DBREAD;
						return $_;
					}
				}
			} else {
				if ($linen == $.) {
					close DBREAD;
					return $_;
				}
			}
		}
		close DBREAD;
	}
	return @data;

ERR:
	close DBREAD;
	&logit("$file \#$id$linen $!", "file","sys");
	return undef;
}

1;
