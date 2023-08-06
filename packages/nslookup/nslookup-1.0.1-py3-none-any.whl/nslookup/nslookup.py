#!/usr/bin/env python3
import dns.resolver, dns.exception

class DNSresponse:
    """data object for DNS answer
    response_full - full DNS response raw
    answer - DNS answer to the query
    """
    def __init__(self, response_full=[], answer=[]):
        self.response_full = response_full
        self.answer = answer

class Nslookup:
    """Object for DNS lookup init with DNS servers"""
    cloudflare_dns = ["1.1.1.1", "1.0.0.1"]


    def __init__(self, dns_servers=cloudflare_dns):
        self.dns_servers = dns_servers


    def base_lookup(self, domain, record_type):
        """Get the DNS record, if any, for the given domain.
        https://github.com/xn-twist/xn-twist/pull/31/files
        """
        # set DNS server for lookup
        dns_resolver = dns.resolver.Resolver()
        dns_resolver.nameservers = self.dns_servers

        try:
            # get the dns resolutions for this domain
            answer = dns_resolver.query(domain, record_type)
            return answer
        except dns.resolver.NXDOMAIN:
            # the domain does not exist so dns resolutions remain empty
            pass
        except dns.resolver.NoAnswer as e:
            # the resolver is not answering so dns resolutions remain empty
            print("the DNS servers {} did not answer".format(dns_resolver.nameservers), e)
        except dns.resolver.NoNameservers as e:
            # the resolver is not answering so dns resolutions remain empty
            print("the nameservers did not answer", e)
        except dns.exception.DNSException as e:
            print("DNS resolving error occurred", e)


    def dns_lookup(self, domain):
        dns_answer = self.base_lookup(domain, "A")
        if dns_answer:
            dns_response = [answer.to_text() for answer in dns_answer.response.answer]
            ips = [ip.address for ip in dns_answer]
            return DNSresponse(dns_response, ips)
        return DNSresponse()


    def soa_lookup(self, domain):
        soa_answer = self.base_lookup(domain, "SOA")
        if soa_answer:
            soa_response = [answer.to_text() for answer in soa_answer.response.answer]
            soa = [next(answer.__iter__()).to_text() for answer in soa_answer.response.answer]
            return DNSresponse(soa_response, soa)
        return DNSresponse()
