sub urlenc {
	my $enc = shift;
	
	$enc =~ s/([^a-zA-Z0-9_\-.])/uc sprintf("%%%02x",ord($1))/eg;

	return $enc;
}

1;

