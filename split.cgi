#!/usr/bin/perl
use CGI qw(:standard);
use JSON;
use Digest::SHA qw(sha1_hex);
use Cache::Memcached::Fast;
use Data::Dumper;
use strict;

my $DEBUG = 0;

my $query = CGI->new;
my $payload = join(' ', $query->keywords);
warn "Payload:" . $payload if $DEBUG;

my $computed_sig = sha1_hex($payload);
my $url_sig = $query->url_param('signature');

warn "comp sig:$computed_sig" if $DEBUG;
warn "sig in  : " . $url_sig if $DEBUG;

# Unless signature sent and is correct , send 403 code
if ((!$url_sig) || ($url_sig != $computed_sig)) {
	print $query->header( -status => 403 );
	exit;
}
	
my $json = new JSON;
$json = $json->allow_nonref();

my $username = $ENV{REMOTE_USER};
warn "Username is:" . $username if $DEBUG;

my $data = join(' ', $query->keywords);
warn "Data:$data" if $DEBUG;

my $json_array = $json->decode( $data );
warn "JSON:" . Data::Dumper::Dumper(\$json_array) if $DEBUG;

# Unless parameter sent, send a 422
unless ($json_array->{string}) {
	print $query->header( -status => 422 );
	exit;
}

my %response;
$response{odd};
$response{even};

my @chars = split('',$json_array->{string});
while (@chars) {
	push @{$response{odd}}, shift(@chars);
	if (@chars) {
		push @{$response{even}}, shift(@chars);
	}
}

warn "Response:" . Data::Dumper::Dumper(\%response) if $DEBUG;
my $json_response = $json->encode(\%response);

# Store in memcached
my $memd = new Cache::Memcached::Fast({servers => [ '127.0.0.1:1337' ]});
$memd->set($username, $json_response, 86400); # Expire time of one day in seconds

print $query->header('application/json');
print $json_response;
