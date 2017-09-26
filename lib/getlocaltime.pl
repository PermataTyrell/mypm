use strict;
  
sub getlocaltime {
	my $time = shift;
	if (!$time) {
		$core::time = time();
		$time = $core::time;
	}
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($time);

	$year += 1900; ## 99 -> 1999
	$mon  += 1;    ## 0..11 -> 1..12
	$sec   = sprintf("%02d",$sec);
	$min   = sprintf("%02d",$min);
	$hour  = sprintf("%02d",$hour);
	$mday  = sprintf("%02d",$mday); ## Must
	$mon   = sprintf("%02d",$mon);  ## Must
	
	#        0     1    2     3    4     5     6     7     8
	return ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
}       
        
1;

