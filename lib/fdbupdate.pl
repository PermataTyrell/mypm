use strict;

require "/home/gurun/public_html/forumx/lib/isokfname.pl";
require "/home/gurun/public_html/forumx/lib/files.conf";
require "/home/gurun/public_html/forumx/lib/logit.pl";

sub fdbupdate {
	my $file         = shift; ## 0
	my $id           = shift; ## 1
	my $newline      = shift; ## 2
	my $col          = shift; ## 3
	my $multiple     = shift; ## 4
	my $updatecolid  = shift; ## 5

	if (!$col) { $col = 0; }

	if (not &isokfname($file)) { return 0; }          ## If illegal characters, exit

	#####(< Read full database to memory >)#####
	if (!-e $file) {
		&logit("create file $file", "debug","sys");
		open (DBUPDATECREATE, ">$file") || &logit("$file $!", "file","sys");
		close DBUPDATECREATE;
	}
	if (-s $file > $lib::files::general::maxdbsize) {
		&logit("Too big db: $file - check your configuration or file may be corrupted ", "error","sys");
		return undef;
	}

	open (FDBUPDATE, "+<$file") || goto ERR;
	flock(FDBUPDATE, 2);
	my @data = <FDBUPDATE>;                                  ## Read full file to memory
	seek (FDBUPDATE, 0, 0);                                  ## Set pointer at top of the file


	#####(< Go through the db >)#####
	my $found = 0;                                          ## Line is found
	my $searching = 1;                                      ## Continue searching

	foreach my $line (@data) {                              ## Each line

		my $update_thisline = 0;

		if ($searching) {
			
			## Update this line?
			my @info = split (/:/, $line);          ## Line info
			if ($info[$col] eq $id) { $update_thisline = 1; }
		}
		if ($update_thisline) {
			if ($updatecolid ne "") {
				chomp($line);
				my @info = split (/:/, $line);## Line info
				my $tmpstring;
				my $colid;
				my $maxc = $#info;
				if ($maxc < $updatecolid) { $maxc = $updatecolid; }
				if ($maxc > 100) {
					&logit("updating field $maxc... quite big table", "debug","sys");
				}
				for ($colid = 0; $colid <= $maxc; $colid++) {
					if ($updatecolid == $colid) {
						$found++;
						$tmpstring .= $newline . ":";
					} else {
						$tmpstring .= $info[$colid] . ":";
					}
				}
				$found++;
				print FDBUPDATE $tmpstring . "\n";
			} else {
				## Print new line
				$found++;
				if ($newline) {
					chomp($newline); $newline .= "\n";              ## Make sure that there is \n
					print FDBUPDATE $newline;
				}
			}
			if (!$multiple) { $searching = 0; }
		} else {
			## Not requested line, print old. Also remove blank lines
			if ($line ne "\n") {
				print FDBUPDATE $line;
			}
		}
	}


	#####[ Add line if not found ]#####
	if (!$found && $newline) {
		if (!$updatecolid ne "") {
			chomp($newline); $newline .= "\n";              ## Make sure that there is \n
			print FDBUPDATE $newline;
		}
	}


	#####[ Close file properly ]#####
	truncate (FDBUPDATE, tell(FDBUPDATE));                              ## Set eof
	close FDBUPDATE;

	undef @data;
	return $found;

ERR:
	&logit("$file $!", "file","sys");
	return undef;
}

1;
