#  Parse HTML form, POST or GET.  Returns pointer to hash of name,value
#  Updated on Jan. 16th 2006 - Insert code for multipart/form-data to check
#  if file uploading being used

require "lib/mime_parts.pl"; # for multipart/form-data

sub form  {

	my ($buffer, @pairs, $pair, $name, $value);

#  ----------New code for multipart/form-data----------------
	my ($type, $boundary) = split(/;\s*/, $ENV{'CONTENT_TYPE'},2);
	if (lc($type) eq "multipart/form-data") {
		$boundary =~ s/^.*boundary=["|']?([^"|']*)["|']?.*$/\1/ig;
	
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		foreach (&mime_parts($buffer, $boundary)) {
			if ($_->{'type'}) {
				$form{"$_->{'name'}"}->{'type'}     = $_->{'type'};
				$form{"$_->{'name'}"}->{'content'}  = $_->{'content'} if($_->{'content'});
				$form{"$_->{'name'}"}->{'length'}   = $_->{'length'}   if($_->{'length'});
				$form{"$_->{'name'}"}->{'filename'} = $_->{'filename'} if($_->{'filename'});
			} else {
				$form{"$_->{'name'}"} = $_->{'content'};
			}
		}
	return 0;
	}

#  --------------------------------------------------------------

	if ($ENV{REQUEST_METHOD} eq "POST")	{
		read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}  else  {
		$buffer = $ENV{QUERY_STRING};
	}

	# Split the name-value pairs
	@pairs = split(/&/, $buffer);

	foreach $pair (@pairs)
	{
    	($name, $value) = split(/=/, $pair);
    	$value =~ tr/+/ /;
    	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    	$value =~ s/ ~!/  ~!/g;

		if ($form{$name})	{
			$form{$name} .= "\0$value"
		} else {
	    		$form{$name} = $value;
		}
	} 

}

1;

