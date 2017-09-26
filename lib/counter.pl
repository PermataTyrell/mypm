use strict;

#############################
# Updated : 30/04/2006
#
# Library utk uruskan counter
#############################

require "lib/logit.pl";

sub counterplus {
	my $file = shift;
	my $val  = shift;

	if ($val eq "") { $val = 1; }  ## One if not defined (accept 0)

	my $n;

	if (-e $file) {
		if (-s $file > 40) {
			## Can't contain 40 digits - corrupted. Create new file
			$n = $val;
			&counterinit($file, $n);
		} else {
			open (COUNTER, "+<$file") || goto ERR;         ## Open for update
			flock (COUNTER, 2);                            ## Exclusive lock
			$n = <COUNTER>;                                ## Read amount

			$n = $n + $val;                                ## Plus counter
			seek (COUNTER, 0, 0);                          ## -> top of the file
			print COUNTER $n;                              ## Print amount
			truncate (COUNTER, tell(COUNTER));             ## Cut rest of the file
			close COUNTER;                                 ## Close it
		}
	} else {
		## Not found, create it
		$n = $val;
		&counterinit($file, $n);
	}
	return $n;

ERR:
	return undef;
}

# Do not test .n extension - handy routine for other purposes also

sub counterinit {
	my $file = shift;
	my $val  = shift;

	open (COUNTER, ">$file") || goto ERR;
	flock (COUNTER, 2);
	print COUNTER $val;
	close (COUNTER);
	return 1;

ERR:
	return 0;
}

# Do not test .n extension - handy routine for other purposes also

sub counterget {
	my $file = shift;

	&logit("Get $file", "debug","data/sys");

	if (-e $file) {
		open (COUNTER, $file) || goto ERR;
		flock(COUNTER, 1);
		my $val = <COUNTER>;
		close (COUNTER);
		return $val;
	} else {
		return undef;
	}

ERR:
	return undef;
}

1;
