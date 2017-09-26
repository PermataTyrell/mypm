
sub fdbsave {
	my $file = pop; ## last item


	open (DBSAVE, ">$file") || goto ERR;
	flock (DBSAVE, 2);
	my $result = print DBSAVE @_;

	if(!$result) { 
		## Write failed, let's bail out
		close(DBSAVE);
		goto ERR; 
	}
	
	close (DBSAVE);

	undef @_;
	return 1;

ERR:
	undef @_;
	return 0;
}

1;

