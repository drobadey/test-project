

def redact_a_ssn(ssn: str) -> str:
    last4 = ssn[-4:]
    # we could do something like this, but the thinking is that the client
    # may have its own standard like ***-**- or whatever.
    # return "###-##-{last4}".format(last4=last4)
    return last4
