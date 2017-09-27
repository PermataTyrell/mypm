# Returns hash where names are header names.
#
# Parameters:
#  0: header

sub parse_header {
	my $HEADER = shift;

	$HEADER =~ s/\n\s+/ /g;
	my %head = ( FROM, split /^([-\w]+):\s*/m, $HEADER );
	foreach $key (keys %head) {
		$head{ lc($key) } = $head{$key};
		chomp($head{ lc($key) });
		chomp($head{$key});
	}
	return %head;
}

sub parse_header_mail {
	my $HEADER = shift;

	$HEADER =~ s/\n\s+/ /g;
	my %head = ( FROM, split /^([-\w]+):\s*/m, $HEADER );
	foreach $key (keys %head) {
		chomp($head{$key});
	}
	return %head;
}

1;
