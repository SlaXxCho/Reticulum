import RNS
from RNS.Link import Link


def create_link(destination, profile="hybrid_light"):
    link = Link(destination)
    link.set_security_profile(minimum_profile="classic", preferred_profile=profile)
    return link


def send_critical(link):
    link.negotiate_security()
    link.send_secure(
        data="mensaje crítico",
        security_tag="MAX_SECURITY"
    )


# Usage sketch:
# destination = RNS.Destination(...)
# link = create_link(destination, profile="hybrid_light")
# send_critical(link)
