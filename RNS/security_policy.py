from RNS.crypto_profiles import SecurityTag, Medium


class SecurityPolicyEngine:
    def __init__(self, profile_manager):
        self.profile_manager = profile_manager

    def _required_profile_for_tag(self, security_tag):
        tag = security_tag if isinstance(security_tag, SecurityTag) else SecurityTag(security_tag)
        if tag == SecurityTag.MAX_SECURITY:
            return "hybrid_strong"
        if tag == SecurityTag.MUST_DELIVER:
            return self.profile_manager.minimum_profile
        if tag == SecurityTag.PREFERRED_SECURE:
            return "hybrid_light"
        return "classic"

    def evaluate(self, security_tag, remote_capabilities, current_profile, medium=Medium.UNKNOWN):
        required = self._required_profile_for_tag(security_tag)
        best_common = self.profile_manager.choose_best_common(remote_capabilities, medium=medium)

        if best_common is None:
            return {
                "allow_send": False,
                "block": True,
                "reason": "No shared crypto profiles",
                "required_profile": required,
                "require_pqc_upgrade": False,
                "allow_downgrade": False,
            }

        required_rank = self.profile_manager.rank(required)
        current_rank = self.profile_manager.rank(current_profile)
        best_rank = self.profile_manager.rank(best_common.name)

        require_pqc = required_rank > self.profile_manager.rank("classic")
        allow_downgrade = current_rank >= self.profile_manager.rank(self.profile_manager.minimum_profile)

        if best_rank < required_rank:
            return {
                "allow_send": security_tag in (SecurityTag.MUST_DELIVER, SecurityTag.STANDARD, "MUST_DELIVER", "STANDARD"),
                "block": security_tag in (SecurityTag.MAX_SECURITY, "MAX_SECURITY"),
                "reason": "Required profile not available",
                "required_profile": required,
                "target_profile": best_common.name,
                "require_pqc_upgrade": False,
                "allow_downgrade": False,
            }

        return {
            "allow_send": True,
            "block": False,
            "reason": "Policy satisfied",
            "required_profile": required,
            "target_profile": best_common.name,
            "require_pqc_upgrade": require_pqc and current_rank < required_rank,
            "allow_downgrade": allow_downgrade,
        }
