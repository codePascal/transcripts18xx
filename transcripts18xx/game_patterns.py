#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import abc


class GamePattern(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def extract_pattern(self, line: str) -> dict | None:
        """Extract relevant game details using regex patterns."""
        pass


class GamePattern1817(GamePattern):

    def __init__(self):
        super().__init__()

    def extract_pattern(self, line: str) -> dict | None:
        # Match game phase and rounds
        phase_match = re.search(r'-- Phase (\d+)', line)
        round_match = re.search(r'-- Operating Round (\d+\.\d+)', line)

        # Match player actions
        bid_match = re.search(r'(\w+) bids \$(\d+) for (.+)', line)
        buy_match = re.search(r'(\w+) buys (\d+)% share of (\w+) from the Treasury for \$(\d+)', line)
        short_match = re.search(r'(\w+) shorts (\w+)', line)
        loan_match = re.search(r'(\w+) takes a loan and receives \$(\d+)', line)
        merge_match = re.search(r'(\w+) merges with (\w+) at share price \$(\d+)', line)

        # Extract details
        if phase_match:
            return dict(
                event='Phase Change',
                phase=phase_match.group(1)
            )
        if round_match:
            return dict(
                event='Operating Round',
                round=round_match.group(1)
            )
        if bid_match:
            return dict(
                event='Bid',
                player=bid_match.group(1),
                amount=int(bid_match.group(2)),
                item=bid_match.group(3)
            )
        if buy_match:
            return dict(
                event="Stock Purchase",
                player=buy_match.group(1),
                percentage=int(buy_match.group(2)),
                company=buy_match.group(3),
                amount=int(buy_match.group(4))
            )
        if short_match:
            return {"event": "Short Selling", "player": short_match.group(1), "company": short_match.group(2)}
        if loan_match:
            return {"event": "Loan Taken", "player": loan_match.group(1), "amount": int(loan_match.group(2))}
        if merge_match:
            return {"event": "Merger", "company_1": merge_match.group(1), "company_2": merge_match.group(2),
                    "share_price": int(merge_match.group(3))}
        return None
