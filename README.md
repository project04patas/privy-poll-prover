# PrivyPoll Prover - Confidential & Attested DAO Polling on Oasis Sapphire using ROFL TEE

**PrivyPoll Prover** is a decentralized application built for demonstrating secure, private, and verifiable polling for DAOs and other communities, leveraging the unique capabilities of the Oasis Network.

Inspired by the foundational principles of anonymity and privacy that underpin most real-life democratic voting systems, PrivyPoll Prover aims to bring similar confidentiality guarantees to on-chain governance, mitigating issues like voter coercion, bandwagon effects, and social pressure.

## The Problem: Transparency vs. Integrity in DAO Voting

Current DAO voting mechanisms, whether fully on-chain or using off-chain signaling platforms like Snapshot, often suffer from a critical issue: **transparent voting.** While transparency is a Web3 cornerstone, in the context of governance, it can lead to:

*   **Whale Influence:** Early, public votes from large token holders can unduly sway smaller voters.
*   **Bandwagon Effects & Social Pressure:** Voters may conform to perceived popular opinion or influential figures rather than their true convictions.
*   **Voter Apathy:** Fear of retribution or scrutiny for unpopular stances can discourage participation.
*   **Increased Risk of Vote Buying/Coercion:** Publicly verifiable votes can make illicit coordination easier to enforce.

Many real-world democratic systems rely on secret ballots precisely to protect voters and ensure the integrity of the outcome. PrivyPoll Prover brings this crucial concept on-chain in a verifiable way.

## Our Solution: PrivyPoll Prover

PrivyPoll Prover offers a robust solution by architecting a system where:

1.  **Polls are Defined On-Chain:** Poll questions, options, duration, and the authorized off-chain tallying service are registered on an Oasis Sapphire smart contract, providing a transparent and immutable definition of the poll.
2.  **Votes are Cast Confidentially Off-Chain:** Voters submit their choices directly to a designated **Oasis ROFL (Runtime Off-chain Logic) service**. This service runs in a Trusted Execution Environment (TEE), ensuring that individual votes remain private and are never written to any public ledger during the voting period.
3.  **Tallying Happens in Secret:** The ROFL TEE service confidentially accumulates and tallies the votes after the polling period ends. This entire aggregation process is shielded from public view and node operators.
4.  **Results are Attested On-Chain:** Once tallied, the ROFL service submits a *single transaction* containing only the final, aggregated results to the Sapphire smart contract.
5.  **Verification via `roflEnsureAuthorizedOrigin`:** The smart contract cryptographically verifies that the submitted results originate *exclusively* from the pre-authorized ROFL TEE instance for that specific poll using Oasis Sapphire's `Subcall.roflEnsureAuthorizedOrigin` function. This ensures the integrity and provenance of the final tally.

This design ensures that individual voting choices remain secret, while the overall process and the final outcome are verifiable and trustworthy.

## How it Utilizes Oasis Network Technologies

*   **Oasis Sapphire:** The EVM-compatible confidential ParaTime is used to host the `PrivyPollProver.sol` smart contract. This contract manages poll creation, stores the authorized ROFL instance ID for each poll, and records the final attested results.
*   **Oasis ROFL (Runtime Off-chain Logic):** A Python application running in a Docker container within a ROFL TEE acts as the confidential vote receiving and tallying engine. Its identity is anchored on Sapphire.
*   **Appd Service:** The ROFL service uses the Appd service to securely communicate with the Sapphire blockchain, specifically to submit the transaction containing the final results.
*   **`Subcall.roflEnsureAuthorizedOrigin`:** This critical Sapphire precompile is used in the smart contract to ensure that only the designated and legitimate ROFL TEE instance can publish the results for a poll, providing a strong cryptographic link between the off-chain confidential computation and the on-chain record.

## Features

*   **Poll Creation:** Users can define new polls with questions, multiple-choice options, duration, and specify the authorized ROFL instance for tallying.
*   **Confidential Vote Submission:** (Simulated via API call to the ROFL service) Users can cast their votes without revealing their choice publicly.
*   **Private Off-Chain Tallying:** The ROFL service securely counts votes.
*   **Attested Result Publication:** The ROFL service publishes only the final aggregated results to the Sapphire smart contract.
*   **Result Viewing:** Anyone can view the details of polls and their published, attested results.

## Technical Details & How to Run****

**1. Smart Contract (`PrivyPollProver.sol`):**
    *   Language: Solidity
    *   Deployment: Oasis Sapphire Testnet
    *   Key Functions: `createPoll(...)`, `publishResults(...)`, `getPollDetails(...)`, `getPollResults(...)`
    *   [Link to Contract Code in Repo]
    *   [Link to Deployed Contract on Sapphire Testnet Explorer]

**2. ROFL Service (Python):**
    *   Language: Python (using Flask/FastAPI for API endpoint)
    *   Environment: Docker container managed by ROFL
    *   Key Functions: API endpoint for vote submission, in-TEE vote storage (in-memory for demo), tallying logic, Appd service interaction for result submission.
    *   [Link to ROFL Service Code in Repo]

**3. Frontend (Basic HTML/JS):**
    *   Technology: HTML, JavaScript, ethers.js
    *   Functionality: Interface for creating polls, submitting votes (to ROFL API), and viewing results from Sapphire.
    *   [Link to Frontend Code in Repo]
    *   [Link to Live Demo (if applicable)]

**Setup & Running Instructions:**
    *   (Details on how to set up MetaMask for Sapphire Testnet)
    *   (Details on how to run the ROFL service locally, if applicable for judges to test, or point to a hosted demo ROFL instance)
    *   (Details on how to interact with the frontend)

## Why PrivyPoll Prover Stands Out

*   **Solves a Real DAO Problem:** Addresses critical privacy vulnerabilities in current on-chain governance.
*   **Innovative Use of Oasis Stack:** Demonstrates a robust pattern using ROFL for confidential off-chain processing and Sapphire for on-chain attestation and settlement. This is more than just encrypting state; it's verifiable, private off-chain *computation*.
*   **Strong Security Model:** Leverages TEEs for vote secrecy and `roflEnsureAuthorizedOrigin` for result integrity.
*   **Potential for Impact:** Provides a blueprint for more secure, fair, and participatory decentralized governance.

## Future Enhancements

*   Integration with existing DAO frameworks.
*   Support for various voting strategies (e.g., quadratic voting, weighted voting) within the ROFL TEE.
*   Enhanced UI/UX.
*   Gas sponsoring for vote submissions to the ROFL service.
*   Formal audits and production hardening.

## Team

*   [Project @ Projecto4Patas]
*   fb.com/projecto4patas

---

This README aims to be comprehensive yet scannable. Remember to:
*   **Fill in the bracketed information** like "[Name of Hackathon]" and the links.
*   **Tailor the "Technical Details & How to Run"** section very specifically once your code is more complete.
*   **Keep it updated** as your project evolves during the hackathon.
*   A good screenshot or a short GIF of the demo in action can also be very powerful in a README.

Good luck!
