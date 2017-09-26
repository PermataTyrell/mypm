#  0: mail
#  1: boundary
#  2: current part number count

require "/home/gurun/public_html/forumx/lib/parse_header.pl";

sub mime_parts {
	my $mail = shift;
	my $bo   = shift;
	my $n    = shift; 

	my @parts = ();
	my @tmp = ();

	if ($bo) {
		$bo =~ s/\$/\\\$/g; 
		@parts = split(/--$bo/, $mail);
		
		pop @parts;
		shift @parts;
	}

	foreach (@parts) {
		$n++;
		my($header,$body) = split(/[\r]?\n[\r]?\n/, $_, 2);
		my %headers = &parse_header($header);

		my $name;
		my $charset;
		my $boundary;
		my $filename;

		my($type, @types) = split(/;\s+/, $headers{'content-type'});
		
		foreach (@types) {
			if (/^charset=["|']?([^"|']*)["|']?/i)   { $charset = $1; }
			if (/^boundary=["|']?([^"|']*)["|']?/i)  { $boundary = $1; }
			if (/^type=["|']?([^"|']*)["|']?/i)      { $type = $1; }
		}

		my($disposition, @types) = split(/;\s+/,$headers{'content-disposition'});
		foreach (@types) {
			if (/^name=["|']?([^"|']*)["|']?/i)  { $name = $1; }
			if (/^filename=["|']?([^"|']*)["|']?/i)  { $filename = $1; }
		}

		$body =~ s/[\r]\n$//g;  # last return away

		my $conid = lc($headers{'content-id'});

		if($conid) {
			$conid = substr($conid,1,length($conid)-2);
		}

		push @tmp, {
			'type'        => lc($type),
			'charset'     => lc($charset),
			'content'     => $body,
			'coding'      => lc($headers{'content-transfer-encoding'}),
			'length'      => length($body),
			'name'        => $name,
			'boundary'    => $boundary,
			'description' => $headers{'content-description'},
			'number'      => $n,
			'headers'     => $header,
			'filename'    => $filename,
			'disposition' => $disposition,
			'content-id'  => $conid,
		};
		
	}
	return @tmp;
}

1;
