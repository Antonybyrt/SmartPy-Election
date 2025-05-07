# 🗳️ Delegate Election Smart Contract (SmartPy)

This project implements a delegate election system using [SmartPy](https://smartpy.io/), a Pythonic smart contract language for the [Tezos blockchain](https://tezos.com/). The contract allows users to register as candidates, vote for their preferred delegate, and automatically determine the winner after the voting period.

## 📦 Features(Work in progress)

- Candidate registration with address
- One-person-one-vote system
- Voting restricted to registered users by the owner
- Election closing by the owner
- Automatic calculation of the winning delegate
- Written in SmartPy and ready for testing/deployment on Tezos
- Hashed addresses for anonymous voting
- Owner can reset the contract data
- Vote statistics

## 📁 Project Structure

```bash
.
├── README.md
├── election.py            # SmartPy contract