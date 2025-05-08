import smartpy as sp

@sp.module
def main():
    
    class Election(sp.Contract):
        def __init__(self, owner):
            self.data.owner = owner
            self.data.votes = sp.big_map()
            self.data.results = sp.big_map()
            self.data.isApplyPeriod = False
            self.data.isVotePeriod = False
            self.data.userList = set()
            sp.cast(self.data.userList, sp.set[sp.address])

        @sp.entrypoint
        def addUsers(self, addresses: sp.list[sp.address]):
            assert self.data.owner == sp.sender, "ONLY_OWNER"
            for i in addresses:
                self.data.userList.add(i)

        @sp.entrypoint
        def openOrCloseApplyPeriod(self):
            assert self.data.owner == sp.sender, "ONLY_OWNER"
            assert self.data.isVotePeriod == False, "NOT_AVAILABLE_DURING_VOTE_PERIOD"
            if self.data.isApplyPeriod == False:
                self.data.isApplyPeriod = True
            else:
                self.data.isApplyPeriod = False

        @sp.entrypoint
        def openOrCLoseVotePeriod(self):
            assert self.data.owner == sp.sender, "ONLY_OWNER"
            assert self.data.isApplyPeriod == False, "NOT_AVAILABLE_DURING_APPLY_PERIOD"
            if self.data.isVotePeriod == False:
                self.data.isVotePeriod = True
            else:
                self.data.isVotePeriod = False

        @sp.entrypoint
        def applyCandidate(self):
            assert self.data.userList.contains(sp.sender), "NOT_REGISTERED"
            assert not self.data.results.contains(sp.sender), "ALREADY_APPLIED"
            assert self.data.isApplyPeriod == True, "NOT_AN_APPLY_PERIOD"
            self.data.results[sp.sender] = 0

        @sp.entrypoint
        def vote(self, candidate):
            sp.cast(candidate, sp.address)
            assert self.data.userList.contains(sp.sender), "NOT_REGISTERED"
            assert not self.data.votes.contains(sp.sender), "ALREADY_VOTED"
            assert self.data.results.contains(candidate), "INVALID_CANDIDAT"
            assert self.data.isVotePeriod == True, "NOT_A_VOTE_PERIOD"
            self.data.votes[sp.sender] = candidate
            self.data.results[candidate] += 1

@sp.add_test()
def test():
        scenario = sp.test_scenario("Election", main)
        scenario.h1("Testing Election Contract")

        owner = sp.test_account("Owner")
    
        election = main.Election(owner.address)
        scenario += election
    
        alice = sp.test_account("Alice")
        bob = sp.test_account("Bob")
        charlie = sp.test_account("Charlie")

    ############################################

        scenario.h2("Adding voters")
        election.addUsers([alice.address, bob.address, charlie.address], _sender = owner)

        scenario.h2("Apply Period")
        election.openOrCloseApplyPeriod(_sender = owner)

    #

        scenario.h2("Applying")
        election.applyCandidate(_sender = alice)

        scenario.h2("Applying")
        election.applyCandidate(_sender = bob)

    #

        scenario.h2("Close Apply Period")
        election.openOrCloseApplyPeriod(_sender = owner)

        scenario.h2("Vote Period")
        election.openOrCLoseVotePeriod(_sender = owner)

    #

        scenario.h2("Voting")
        election.vote(alice.address, _sender = alice)

        scenario.h2("Voting")
        election.vote(bob.address, _sender = bob)

        scenario.h2("Voting")
        election.vote(alice.address, _sender = charlie)

    #

        scenario.h2("Close Vote Period")
        election.openOrCLoseVotePeriod(_sender = owner)

    #
    
        scenario.verify(election.data.results[alice.address] == 2)
        scenario.verify(election.data.results[bob.address] == 1)