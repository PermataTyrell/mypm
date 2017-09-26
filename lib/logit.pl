########################################################################
# lib/sys/logit.pl v. 1.0.0
#
# Log information (add line to log)
#
#
# Returns: nothing
# 
# Examples:
#  &logit("Bug! No x parameter defined.", "error");
#
# Parameters:
#  Please follow parameter instructions to make logs more understandable,
#  standard and to make analyzing easy.
#
#  0: Message. Couple of keywords to begin the string will help
#     to make log analyzes...
#     Bug!             Missing parameter or other error which is considered as a bug.
#     Security.        Information related to security issues. Does not
#                      have to mean security violence.
#
#  1: type:            level:      description
#     debug              0         only for debugging, logged if debug mode is on
#     info               0         informative log
#     warning            1         warning, something not working too smoothly
#     error              2         major software error
#     critical           3         critical software or user error
#
#  2: logfile instead of system.log
#
# standard v1: Not checked
# 
########################################################################

use strict;

require "/home/gurun/public_html/forumx/lib/getlocaltime.pl";

sub logit {
	my $engine = shift;
	my $msisdn  = shift;
	my $log   = shift;

	$engine =~s/\s/./;
	$engine =~s/(.*?)\s/\L$1 \E/; # make sure the first word is in lowercase 
	$msisdn =~s/\+//g;

	if($log=~/image/) {
		my($package, $filename, $line) = caller;
		print STDERR "eeeks: $package, $filename, $line\n";
	}

	## Debug mode?
	if ($msisdn eq 'debug' && !$core::debugmode) { return; }

	## Get date
	my ($sec, $min, $hour, $day, $month, $year, $wday) = (&getlocaltime())[0,1,2,3,4,5,6];

	## Define log file
	if ($log) {
		$log = "$log\.log";
	} else {
		if(defined $core::cwdir) {
			$log = "$core::cwdir\.log";
		} else {
			$log = "system.log";
		}
	}

	## format
	$engine =~ s/\n|\t//g;

	## Get client
	my $client = $ENV{'REMOTE_ADDR'} if $ENV{'REMOTE_ADDR'};

	## Which sub called me?
	my $sub = (caller(2))[3];
	$sub.= "->" . (caller(1))[3];
	if ($core::debugmode) {
		my $sub1 = (caller(3))[3];
		if ($sub1) { $sub = $sub1 . "->" . $sub; }
	}
	$sub =~ s/main\:\://g;


	## Who am I?
	my $script;
	if ($0 =~ /\//) {
		my @info = split(/\//, $0);
		$script = $info[$#info - 1] . "/" . $info[$#info];
		$script=~s{\0}{}g;
	} else {
		$script = $0;
		$script=~s{\0}{}g;
	}
	my @MONTH=("","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");
	my $datefixed = "$day\/$MONTH[$month]\/$year\:$hour\:$min\:$sec +0000";


	#####[ Print logline ]#####
	open (LOG, ">>$log") ||
		#printf STDERR ("$msisdn - - [$datefixed] [file] [client $ENV{'REMOTE_ADDR'}] $engine - %-16s - Can't open $log $!\n", $0);
		printf STDERR ("$msisdn - - [$datefixed] [file] [client ] $engine - %-16s - Can't open $log $!\n", $0);
	flock (LOG, 2);
	print LOG                       "$msisdn - - [$datefixed] \"GET \/$engine\" 200 10 \n";
	#if ($client) { print LOG        "[$client] "; }
	#if ($main::U) { print LOG       "[$main::U] "; }
	close LOG;

}

1;
