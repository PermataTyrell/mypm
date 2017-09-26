use strict;
use MIME::Lite;

sub sendmail {

        my $from = shift;
        my $to = shift;
        my $subject = shift;
        my $message = shift;

        # create a new message
        my $msg = MIME::Lite->new(From => $from, To => $to, Subject => $subject, Data => $message);

        # send the email
        #MIME::Lite->send('sendmail', "/usr/lib/sendmail -t -oi -oem");
        $msg->send();

        return undef;
}

sub sendmail_cc {

        my $from = shift;
        my $to = shift;
        my $cc = shift;
        my $subject = shift;
        my $message = shift;

        # create a new message
        my $msg = MIME::Lite->new(From => $from, To => $to, Cc => $cc, Subject => $subject, Data => $message);

        # send the email
        #MIME::Lite->send('sendmail', "/usr/lib/sendmail -t -oi -oem");
        $msg->send();

        return undef;
}

1;
