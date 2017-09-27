use strict;

require "/home/gurun/public_html/forumx/lib/fdbread.pl";
require "/home/gurun/public_html/forumx/lib/template-gosms.pl";

sub security {
        my $file = $ENV{'SCRIPT_NAME'};
        my $user = $ENV{'REMOTE_USER'};

        my $SECURITYDB = "data/security.dat";

        $file =~s/^(.*)\/(.*)/$2/;

        my $chk = &fdbread($SECURITYDB,$user);

        if($chk=~/$file/g){
             return undef;

        }else{
             my $msg = "Content-type:text/html\n\n";
             $msg = $msg.&header."<h3>You're not authorized to access this page!</h3>".&footer;
             return $msg;
        }
}

1;
