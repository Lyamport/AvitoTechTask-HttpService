def check_valid_ip(ip):
    octets = str(ip).split('.')
    if len(octets) != 4:
        return False
    try:
        if int(octets[0]) == 0:
            return False
        for i in octets:
            if int(i) < 0 or int(i) > 255:
                return False
    except:
        return False
    return True
