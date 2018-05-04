#!/usr/bin/perl
use CGI qw(:standard);
use Cache::Memcached::Fast;
use Data::Dumper;
use strict;

my $DEBUG = 0;

my $query = CGI->new;

my $username = $ENV{REMOTE_USER};
warn "Username is:" . $username if $DEBUG;

# Pull from memcached
my $memd = new Cache::Memcached::Fast({servers => [ '127.0.0.1:1337' ]});
my $json_response = $memd->get($username); # Response is stored in memcached already encoded
warn "Response:" . Data::Dumper::Dumper(\$json_response) if $DEBUG;

print $query->header('application/json');
print $json_response;
