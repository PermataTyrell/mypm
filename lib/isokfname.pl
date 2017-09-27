use strict;

require "lib/logit.pl";

sub isokfname {
	my $file = shift;

	if ($file =~ /\0/) {
		&logit("File name contains null byte ($file)!", "security","sys");
		return 0;
	}
	if ($file =~ /\|/) {
		&logit("File name contains pipe ($file)!", "security","sys");
		return 0;
	}
	if ($file =~ /\.\.\//) {
		&logit("File name contains two dots and slash ($file)!", "security","sys");
		return 0;
	}
	my $tmpfile = $file;
	$tmpfile =~ s/([\&;\`'\\\|"*?~<>^\(\)\[\]\{\}\$\n\r])/\\$1/g;
	if ($tmpfile ne $file) {
		&logit("File name contains some non-allowed characters ($file)!", "security","sys");
		return 0;
	}

	return 1;

}

1;

