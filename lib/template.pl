use strict;

require "/home/gurun/public_html/forumx/lib/fdbread.pl";

$lib::template::securitydb = "data/security.dat";
$lib::template::user = $ENV{'REMOTE_USER'};
$lib::template::scriptname = $ENV{'SCRIPT_NAME'};
$lib::template::scriptname =~s/^(.*)\/(.*)/$2/;

sub header {

print "content-type:text/html\n\n
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" /> 
<style type=\"text/css\">
html, body, form, fieldset {
	margin: 0;
	padding: 0;
}
body { 
   font-family:Tahoma, Arial, Helvetica, sans-serif; 
   color: #ffffff; 
   background-color: #D9D9D9;
   line-height: 160%;
   font-size: 10pt;
}
table {
   font-size: 10pt;
   line-height: 160%;
   color: #ffffff;
   valign:top; 
}
h1 { 
   font-family: \"Segoe UI\", \"Trebuchet MS\", Arial, Helvetica, sans-serif;
   font-size: 170%;
   line-height: 90%;
   font-weight: bold; 
   color: #ffffff; 

} 
h2 { 
   font-family: \"Segoe UI\", \"Trebuchet MS\", Arial, Helvetica, sans-serif;
   font-size: 150%;
   font-weight: bold; 
   color: #ffffff; 
   border-bottom: 1px solid #848383; 
} 
h3 { 
   font-family: \"Segoe UI\", \"Trebuchet MS\", Arial, Helvetica, sans-serif;
   font-size: 120%;
   font-weight: bold; 
   color: C1C1C0; 
} 
a {
   color: #ffffff; 
   text-decoration:none;
}
a:hover {
   color: #8B8B8B; 
   text-decoration:none;
}
p, pre, blockquote, ul, ol, h1, h2, h3, h4, h5, h6 {
	margin: 1em 0;
	padding: 0;
}

#footer {
   width=100%;
   text-align:center;
   padding:5px;
   color: #ffffff; 
}
#box400 {
   width:400px;
   background-color:#848383;
   padding:5px;
}
#box390 {
   width:390px;
   background-color:#747473;
   padding:10px;
}
#box450 {
   width:450px;
   background-color:#848383;
   padding:5px;
}
#box440 {
   width:440px;
   background-color:#747473;
   padding:10px;
}
#box500 {
   width:600px;
   background-color:#848383;
   padding:5px;
}
#box490 {
   width:590px;
   background-color:#747473;
   padding:10px;
}
#box600 {
   width:600px;
   background-color:#848383;
   padding:5px;
}
#box590 {
   width:580px;
   background-color:#747473;
   padding:10px;
}
#box800 {
   width:800px;
   background-color:#848383;
   padding:5px;
}
#box790 {
   width:780px;
   background-color:#747473;
   padding:10px;
}
#boxleft {
   text-align:left;
   width:100%;
   padding: 0px 0px 0px 10px;
}
#boxright {
   text-align:right;
   width:100%;
   padding: 0px 20px 0px 0px;
}
#list {
   text-align:left;
}
form {
	margin: 0;
	padding: 0;
}

input.css, textarea.css {
	background-color: inherit;
	border: 1px solid #ccc;
	color: #333;
	display: block;
	padding: 2px;
        valign:top;
}
input.css { 
             width: 200px;
}
textarea.css:hover, input.css:hover {
	background-color: #fff;
	border: 1px solid #accc39;
}
</style>
</head>
<body><center>";

my $chk = &fdbread($lib::template::securitydb,$lib::template::user);
if($chk!~/$lib::template::scriptname/g){
     print "<div id=box400><div id=box390>";
     print "<h3>You're not authorized to access this page!</h3>";
     print "</div></div></center></html>";
     exit;
}else{
     return 0;
}

}

sub footer {

my $othrmenu = "<a href='cg.cgi'>CariGold</a> | <a href='UpdateUserSetting.cgi'>Update User Settings</a> | <a href='UpdateSXWebEngine.cgi'>Update Seducer Script</a> | <a href='CfgSummary.cgi'>Summary</a> | <a href='UserLog.cgi'>User Log</a> | <a href='UpdateUserRec.cgi'>User Record</a> | ";
 
my $chk = &fdbread($lib::template::securitydb,$lib::template::user);
if($chk=~/$lib::template::scriptname/g){
     print "</div><div id=footer>$othrmenu<a href='run.cgi'>Shell</a> | <a href='index.cgi'>Edit</a> | <a href='packaging.cgi'>Packaging</a> | <a href='security.cgi'>Security</a></div></div></center></html>";
}else{
     print "</div></div></center></html>";
}

return 0;

}

1;
