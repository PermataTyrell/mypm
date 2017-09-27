#!/usr/bin/perl

#use strict;
#use warnings;
use LWP::UserAgent;
use WWW::Mechanize;
use HTTP::Cookies;
require "lib/form.pl";
require "lib/fcode.pl";
require "lib/counter.pl";
require "lib/fdbupdate.pl";
require "lib/fdbread.pl";
require "lib/fdbsave.pl";

%form;
&form;
my $mukadepanCG = "cgmainpage.html";
my $loginresult = "loginresult.html";
my $ppr;
my %login = ('ahlilfikir' => 'abc123', 'AlfredJabu' => 'abc12345',
             'kelambubiru' => 'abc123', 'babyrina' => 'abc123', 'azlanhussain' => 'nusaxcess73',
             'solehpolysas' => 'cgsoleh', 'rizorx' => 'cgsoleh', 'MoonLT' => 'cgsoleh',
             'Kudin001' => 'cgsoleh', 'Paksu2012' => 'cgsoleh', 'IdeaUmi' => 'cgsoleh');
my $viewpage = $form{forceurl} || $form{forumurl} || 'https://github.com/tyrellsys/bushiroad-com/pull/43';
my $cookiesfile = ($form{poster} || 'azlanhussain').'-cgcookies';
my $cookie_jar = HTTP::Cookies->new(file => $cookiesfile, autosave => 1, autocheck => 0 );
my $mech = WWW::Mechanize->new(cookie_jar => $cookie_jar, stack_depth => 5);
$mech->add_header('User-Agent' => &web_agent);
$mech->add_header( Referer => $viewpage);
#$mech->proxy('http', 'http://190.144.55.147:8080/');
$mech->timeout(30);
$mech->get($viewpage);
my $content = $mech->content();

# untuk simpan page new threads
if ($viewpage!~/do=getnew/){ &fdbsave($content,$mukadepanCG); }

if($content=~/value="Log in"/ && $form{login} && $login{$form{poster}}){
  $mech->tick('cookieuser','1');
  $mech->submit_form(
        form_number => 1,
        fields      => {
            vb_login_username    => $form{poster},
            vb_login_password    => $login{$form{poster}},
        }
    );
  $mech->follow_link(tag => 'meta'); 
  $content = $mech->content();
  &fdbsave($content,$loginresult);

  #print "content-type:text/html\n\n";
  #print "$cookiesfile | $form{poster} | $form{post} | $form{message}";
  #print $content; exit;

}elsif($form{poster} && $form{post} && $form{message}){
  #print "content-type:text/html\n\n";
  #print "$cookiesfile | $form{poster} | $form{post} | $form{message} | $viewpage";
  #print $content; exit;
  if($form{db}){
	my $DB = '/home/gurun/public_html/forumx/data/'.$form{db}.'.dat';
  	my $id = &counterplus('/home/gurun/public_html/forumx/data/'.$form{db}.'.id');
  	&fdbupdate($DB,$id,$id.':'.&fencode($form{poster}).':'.&fencode($viewpage).':'.
		&fencode($form{message}).":NEW\n");
  }else{
  	$mech->submit_form(
 	      form_name => 'vbform',
  	      fields      => {
  	          message    => $form{message}
  	      }
  	);
  	$content = $mech->content();
	$viewpage = $viewpage."&page=1000" if $viewpage !~/page=/i; 
  }
}elsif($form{dbshow}){
	foreach my $x (split "\n",`tail /home/gurun/public_html/forumx/data/$form{dbshow}.dat &`){
		$x=~s/(.*):(.*?)$/$2\/$1/;
		$x=~s/(.*):(.*?)$/$1\|\#\|\|\#\|$2/;
		$x=~s/:/\//g;
		$x=~s/\|\#\|/\n/g;
		$latestrecord .= fdecode($x)."\n======================================================\n";
	}
	$ppr = 'showdb';
}elsif($form{dbedit} && $form{dbeditrecno}){
	my $DB = "/home/gurun/public_html/forumx/data/$form{dbedit}.dat";
	if($form{dbeditsubmit} && $form{dbeditmsg}){
		my ($v,$w,$x,$y,$z) = split /:/,&fdbread($DB,$form{dbeditrecno});
		&fdbupdate($DB,$v,$v.':'.$w.':'.$x.':'.&fencode($form{dbeditmsg}).':'.$z);
		$dbeditmsg = $form{dbeditmsg};
		$dbeditrecno = $form{dbeditrecno};
		$dbedit = $form{dbedit};
		$dbeditsubmit = "<input type=submit name=dbeditsubmit value=Edit>";
	}else{
		my ($v,$w,$x,$y,$z) = split /:/,&fdbread($DB,$form{dbeditrecno});
		if($z=~/DONE/i){
			$dbeditmsg = "RECORD ALREADY BEEN SUBMITTED. NO EDITING IS ALLOWED!!!";
		}else{
			$dbeditmsg = &fdecode($y);
			$dbeditrecno = $form{dbeditrecno};
			$dbedit = $form{dbedit};
			$dbeditsubmit = "<input type=submit name=dbeditsubmit value=Edit>";
		}
	}
	$ppr = 'editdb';
}

print "content-type:text/html\n\n";
print <<CG;
<html>
<head>
<style type="text/css">
html {overflow: auto;}
html, body {margin: 0px; padding: 0px; height: 100%; border: none;}
body { 
   color: #000000; 
   background-color: #D9D9D9;
   line-height: 160%;
   font:10px arial,sans-serif;
   letter-spacing:1.5px;
   font-size: 10pt;
}
.panel {
	display:none;
	position:fixed;
	top:25px;
	z-index:9999;
	color:#000000;
	background:#E7E6E7;
	#min-width:600px;
	padding:5px 10px;
   	letter-spacing:1.5px;
   	font:10px arial,sans-serif;
}
.showforum {
	display: block; width: 100%;top:20px; border: none; overflow-y: auto; overflow-x: hidden;
}
table td {
	text-align: left;
	letter-spacing:1.5px;
	font:10px arial,sans-serif;
}
.toppanel {
	text-align: left;
	letter-spacing:1.5px;
	font:10px arial,sans-serif;
	padding:0;
	position: fixed;
	top: 0;
	height:28px;
	width:100%; 
	display:block; 
	border:none; 
	color:#000000; 
	background:#E7E6E7;
}
#emoticons { margin-left:60px;	}

</style>
<script src="https://cdn.rawgit.com/azlanhussain/seducing-script/master/jquery-1.7.2.min.js" type="text/javascript"></script>
</head>
<body>
<div class='toppanel'>
 &nbsp; ForumX (v 1.0) | 
Go to <select onChange="var op=this.options[this.selectedIndex];/*(op.value)*/">
<option value=> </option>
<option value=>CariGold</option>
<option value=>WangCyber</option>
<option value=>Sabah Forum</option>
</select> <input type=button id=pm value=Post><input type=button id=sp value="Scheduled Post"><input type=button id=esp value="Edit Scheduled Post"> 
</div>

<iframe id=cg class='showforum' src="$viewpage" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>

<form action="http://forumx.gurun.info/index.cgi" menthod=post name=cgpost>
<div id='postforum' class='panel'>
<table>
<tr><td colspan=2><b>
CG
print $mech->title()."</b></td></tr>";
print <<CG;
<tr><td colspan=2>Posting thread <select name=forumurl onchange="var op=this.options[this.selectedIndex];golah(op.value);">
<option value="http://carigold.com/portal/forums/search.php?do=getnew">CariGold.com</option>
CG
print "<option value=\"$viewpage\" SELECTED>$viewpage</option>" if $viewpage;

unless ($viewpage=~/do=getnew/){ $content = &fdbread($mukadepanCG) if -e $mukadepanCG;}

while ($content=~ m/thread_title_(.*?)".*">(.*?)<\/a>/g){
	print  "<option value=\"http://carigold.com/portal/forums/showthread.php?t=".$1."\">".$2."</option>\n";
}

print <<CG;
</select></td></tr>
<tr><td colspan=2 valign=top>or <input id=forceurl name=forceurl size=80 type=text value="$form{forceurl}"></td></tr>
<tr><td valign=top>Message <textarea cols=50 rows=3 id=message name=message>$form{message}</textarea><br>  
<div id="emoticons">
    <a href="#" title=":)"><img alt=":)" border="0" src="http://carigold.com/portal/forums/images/smilies/happy.gif" /></a>
    <a href="#" title=":("><img alt=":(" border="0" src="http://carigold.com/portal/forums/images/smilies/sadd.gif" /></a>
    <a href="#" title=":o"><img alt=":o" border="0" src="http://carigold.com/portal/forums/images/smilies/surprise.gif" /></a>
    <a href="#" title=":D"><img alt=":D" border="0" src="http://carigold.com/portal/forums/images/smilies/biggrinn.gif" /></a>
    <a href="#" title=":(("><img alt=":((" border="0" src="http://carigold.com/portal/forums/images/smilies/crying.gif" /></a>
    <a href="#" title=':">'><img alt=':">' border="0" src="http://carigold.com/portal/forums/images/smilies/blushing.gif" /></a>
    <a href="#" title=":mad:"><img alt=":mad:" border="0" src="http://carigold.com/portal/forums/images/smilies/angry.gif" /></a>
    <a href="#" title=":))"><img alt=":))" border="0" src="http://carigold.com/portal/forums/images/smilies/laughing.gif" /></a>
    <a href="#" title=":eek:"><img alt=":eek:" border="0" src="http://carigold.com/portal/forums/images/smilies/kekeke.gif" /></a>
    <a href="#" title=":-?"><img alt=":-?" border="0" src="http://carigold.com/portal/forums/images/smilies/thinking.gif" /></a>
    <a href="#" title="~X("><img alt="~X(" border="0" src="http://carigold.com/portal/forums/images/smilies/atwitsend.gif" /></a>
</div>
</td>
<td valign=2><select name=poster>
<option></option>
<option>ahlilfikir</option>
<option>AlfredJabu</option>
<option>kelambubiru</option>
<option>babyrina</option>
<option>azlanhussain</option>
<option>solehpolysas</option>
<option>rizorx</option>
<option>MoonLT</option>
<option>Kudin001</option>
<option>Paksu2012</option>
<option>IdeaUmi</option>
</select> <input type=submit value=Login name=login> <br>
<select name=db>
<option></option>
<option>carigold</option>
<option>bump</option>
</select> <input type=submit value=Submit name=post> <input type=button id=clear value=Clear> 
</td></tr>
<tr><td> <a href=loginresult.html target=_blank>Login Status</a> | <a href=cgmainpage.html target=_blank>Status</a></td></tr>
</table>
</div>
<div id=showdb class='panel'>
Select Database <select name=dbshow onchange="var op=this.options[this.selectedIndex];golah(op.value);">
<option> </option>
<option>carigold</option>
<option>bump</option>
</select><br>
<textarea cols=50 rows=10 disabled="disabled">
$latestrecord
</textarea><br>
<a href=cgdaemon.html target=_blank>Show Last Result</a>
</div>
<div id=editdb class='panel'>
Rec no <input name=dbeditrecno size=2 value=$dbeditrecno> Select Database <select name=dbedit onchange="var op=this.options[this.selectedIndex];golah(op.value);">
<option>$dbedit</option>
<option> </option>
<option>carigold</option>
<option>bump</option>
</select><br>
<textarea cols=50 rows=10 name=dbeditmsg>
$dbeditmsg
</textarea><br>
$dbeditsubmit
</div>
</form>
<script language=javascript>
\$FX = jQuery.noConflict(); 

\$FX('#emoticons a').click(function(){

    var smiley = \$FX(this).attr('title');
    var caretPos = caretPos();
    var strBegin = \$FX('#message').val().substring(0, caretPos);
    var strEnd   = \$FX('#message').val().substring(caretPos);
    \$FX('#message').val( strBegin + " " + smiley + " " + strEnd);


    function caretPos() {
    	var el = document.getElementById("message");
    	var pos = 0;
    	// IE Support
    	if (document.selection) 
    	{
        	el.focus ();
        	var Sel = document.selection.createRange();
        	var SelLength = document.selection.createRange().text.length;
        	Sel.moveStart ('character', -el.value.length);
        	pos = Sel.text.length - SelLength;
    	}
    	// Firefox support
    	else if (el.selectionStart || el.selectionStart == '0')
        	pos = el.selectionStart;

    	return pos;

    }

});

function golah (id){
	if (!id) return false;
	document.getElementById('forceurl').value = '';
	document.forms[0].submit();
}
function papar(id) {
	if (!id) return false;
        if (\$FX('#' + id).css('display') == 'block') {
		\$FX('#postforum').css({'display' : 'none'});
		\$FX('#showdb').css({'display' : 'none'});
		\$FX('#editdb').css({'display' : 'none'});
         	\$FX('#' + id).css({'display' : 'none'});
        } else {
		\$FX('#postforum').css({'display' : 'none'});
		\$FX('#showdb').css({'display' : 'none'});
		\$FX('#editdb').css({'display' : 'none'});
         	\$FX('#' + id).css({'display' : 'block'});
        }
}
papar('$ppr');
\$FX('.toppanel #pm').on('click', function(){papar('postforum');});
\$FX('.toppanel #sp').on('click', function(){papar('showdb');});
\$FX('.toppanel #esp').on('click', function(){papar('editdb');});
\$FX('#postforum #clear').on('click', function(){\$FX('#postforum #message').val('');});
</script>
</body>
</html>

CG

sub web_agent{

my @agnt = (
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.3 (KHTML, like Gecko) Chrome/4.0.224.2 Safari/532.3",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.3 (KHTML, like Gecko) Chrome/4.0.223.5 Safari/532.3",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.4 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE) Chrome/4.0.223.3 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.2 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.1 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.1 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.1 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.0 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.8 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.7 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.6 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.6 Safari/532.2",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.222.6 Safari/532.2",
"Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8",
"Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
"Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b1) Gecko/20091014 Firefox/3.6b1 GTB5",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a1pre) Gecko/20090428 Firefox/3.6a1pre",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a1pre) Gecko/20090405 Firefox/3.6a1pre",
"Mozilla/5.0 (X11; U; Linux i686; ru-RU; rv:1.9.2a1pre) Gecko/20090405 Ubuntu/9.04 (jaunty) Firefox/3.6a1pre",
"Mozilla/5.0 (Windows; Windows NT 5.1; es-ES; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre",
"Mozilla/5.0 (Windows; Windows NT 5.1; en-US; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.2) Gecko/20100101 Firefox/3.6",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.2) Gecko/20091111 Firefox/3.6",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b5pre) Gecko/20090517 Firefox/3.5b4pre (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4pre) Gecko/20090409 Firefox/3.5b4pre",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4pre) Gecko/20090401 Firefox/3.5b4pre",
"Mozilla/5.0 (X11; U; Linux i686; nl-NL; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 GTB5 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 GTB5",
"Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5",
"Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.1.5) Gecko/Firefox/3.5.5",
"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU; rv:1.9.1.4) Gecko/20091016 Firefox/3.5.4 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; yie8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; Zune 3.0; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 4.0.20402; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET CLR 4.0.20506)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; chromeframe; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; chromeframe; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; SLCC2)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
"Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
"Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)",
"Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; fr-FR)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; en-US)",
"Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)",
"Mozilla/4.79 [en] (compatible; MSIE 7.0; Windows NT 5.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
"Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
"Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)",
"Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)",
"Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 3.0.04506)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)");

return $agnt[int(rand(int(scalar(@agnt))-1))];
}

1;
