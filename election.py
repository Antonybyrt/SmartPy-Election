import smartpy as sp

@sp.module
def main():
    
    class Election(sp.Contract):
        def __init__(self):
            self.data.votes = sp.big_map()
            self.data.results = sp.big_map()

        @sp.entrypoint
        def applyCandidate(self):
            assert not self.data.results.contains(sp.sender), "ALREADY_APPLIED"
            self.data.results[sp.sender] = 0

        @sp.entrypoint
        def vote(self, candidate):
            sp.cast(candidate, sp.address)
            assert not self.data.votes.contains(sp.sender), "ALREADY_VOTED"
            assert self.data.results.contains(candidate), "INVALID_CANDIDAT"
            self.data.votes[sp.sender] = candidate
            self.data.results[candidate] += 1

@sp.add_test()
def test():
        scenario = sp.test_scenario("Election", main)
        scenario.h1("Testing Election Contract")
    
        election = main.Election()
        scenario += election
    
        alice = sp.test_account("Alice")
        bob = sp.test_account("Bob")
        charlie = sp.test_account("Charlie")

        scenario.h2("Applying")
        election.applyCandidate(_sender = alice)

        scenario.h2("Applying")
        election.applyCandidate(_sender = bob)

        scenario.h2("Voting")
        election.vote(alice.address, _sender = alice)

        scenario.h2("Voting")
        election.vote(bob.address, _sender = bob)

        scenario.h2("Voting")
        election.vote(alice.address, _sender = charlie)
    
        scenario.verify(election.data.results[alice.address] == 2)
        scenario.verify(election.data.results[bob.address] == 1)