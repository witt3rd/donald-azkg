# Game Theory Cheat Sheet for Computer Scientists

## Introduction
- **Definition**: Mathematical study of strategic interactions among rational decision-makers.
- **Motivations**: Predict outcomes, optimize strategies, design robust systems.
- **Goals**: Find equilibria, ensure fairness, incentivize desired behaviors.
- **CS Relevance**: Multi-agent systems, auctions, routing, security, AI.

## Basic Concepts
- **Players**: Decision-makers (e.g., agents, users).
- **Strategies**: Available actions.
- **Payoffs**: Outcomes/utilities from strategy combinations.
- **Game Types**:
  - Cooperative vs. Non-cooperative
  - Zero-sum vs. Non-zero-sum
  - Simultaneous vs. Sequential
  - Perfect vs. Imperfect Information
  - Complete vs. Incomplete Information
- **Representations**:
  - Normal Form: Matrix for simultaneous games.
  - Extensive Form: Tree for sequential games.

## Solution Concepts
- **Nash Equilibrium (NE)**: No player benefits by unilaterally changing strategy.
  - Pure: Single strategy.
  - Mixed: Randomized strategies.
- **Dominant Strategy**: Always optimal, regardless of others’ actions.
- **Pareto Optimality**: No better outcome for all without harming someone.
- **Subgame Perfect Equilibrium**: NE in every subgame (extensive form).

## Algorithmic Game Theory
- **Focus**: Algorithms for strategic settings.
- **Key Metrics**:
  - Price of Anarchy: Worst NE welfare vs. optimal.
  - Price of Stability: Best NE welfare vs. optimal.
- **Complexity**: NE computation is PPAD-complete; correlated equilibria computable via linear programming.
- **Applications**: Auctions, routing, resource allocation, voting.

## Mechanism Design
- **Goal**: Design games for desired outcomes with self-interested players.
- **Incentive Compatibility**: Truthful reporting is optimal.
- **Examples**: Vickrey auction, VCG mechanism.

## CS Applications
- Multi-agent systems
- Auction design
- Network routing
- Security (e.g., intrusion detection)
- Cryptography (e.g., zero-knowledge proofs)

## Mathematical Framework
- **Utility Functions**: Represent preferences.
- **Best Response**: Maximizes payoff given others’ strategies.
- **Theorems**:
  - Nash’s: Finite games have NE.
  - Folk: Repeated games sustain cooperative payoffs.
  - Revelation Principle: Truthful mechanisms achieve any implementable outcome.

## Tools
- **Gambit**: Computes equilibria ([gambit.sourceforge.net](http://gambit.sourceforge.net)).
- **GAMUT**: Generates test games ([gamut.stanford.edu](http://gamut.stanford.edu)).

## Further Reading
- *Lectures in Game Theory for Computer Scientists* by Apt & Grädel
- *Algorithmic Game Theory* by Nisan et al.
- [MIT OpenCourseWare](https://ocw.mit.edu/courses/6-254-game-theory-with-engineering-applications-spring-2010/)

---

# Comprehensive Game Theory Overview for Computer Scientists

## Introduction
Game theory studies strategic interactions among rational decision-makers, modeling scenarios where outcomes depend on multiple parties’ choices. Its motivations include predicting behaviors, optimizing strategies, and designing systems resilient to strategic manipulation. In computer science, game theory is crucial for multi-agent systems, auctions, network routing, security, and AI, where agents act strategically. The goals are to identify stable outcomes (equilibria), ensure fairness, and create mechanisms that align individual incentives with system objectives.

## Basic Concepts
- **Players**: Entities making decisions (e.g., agents, users, or systems).
- **Strategies**: Possible actions a player can take.
- **Payoffs**: Numerical outcomes reflecting players’ preferences, often represented as utilities.
- **Game Representations**:
  - **Normal Form**: A matrix showing payoffs for simultaneous moves (e.g., Prisoner’s Dilemma: Stay silent/Betray with payoffs -1,-1; -3,0; 0,-3; -2,-2).
  - **Extensive Form**: A tree capturing sequential moves and timing.
- **Game Classifications**:
  - **Cooperative vs. Non-cooperative**: Binding agreements vs. independent actions.
  - **Zero-sum vs. Non-zero-sum**: Fixed vs. variable total payoffs.
  - **Simultaneous vs. Sequential**: Moves occur together or in order.
  - **Perfect vs. Imperfect Information**: All past moves known or not.
  - **Complete vs. Incomplete Information**: All rules/payoffs known or not.
  - **Finite vs. Infinite**: Limited or unlimited moves.

| **Game Type**            | **Description**                              | **Example**                     |
|--------------------------|----------------------------------------------|---------------------------------|
| Cooperative              | Players form binding agreements              | Coalition formation            |
| Non-cooperative          | Players act independently                    | Prisoner’s Dilemma             |
| Zero-sum                 | One player’s gain is another’s loss          | Chess                          |
| Non-zero-sum             | Total payoffs can vary                       | Battle of the Sexes            |
| Perfect Information      | All past moves known                         | Chess                          |
| Imperfect Information    | Some moves unknown                           | Poker                          |

## Solution Concepts
- **Nash Equilibrium (NE)**: A strategy profile where no player can improve their payoff by unilaterally changing their strategy. 
  - **Pure Strategy NE**: Players choose a single strategy.
  - **Mixed Strategy NE**: Players randomize over strategies with probabilities.
  - **Example**: In a coordination game, both players choosing the same action (e.g., “meet at party”) can be a pure NE.
- **Dominant Strategy**: Optimal regardless of others’ actions (e.g., “betray” in Prisoner’s Dilemma).
- **Pareto Optimality**: An outcome where no alternative improves all players’ payoffs without harming someone.
- **Subgame Perfect Equilibrium**: A NE that holds in every subgame of an extensive-form game, often found via backward induction.
- **Key Theorems**:
  - **Nash’s Existence Theorem** (1950): Every finite, non-cooperative game has at least one NE (possibly mixed).
  - **Oddness Theorem** (Wilson, 1971): Finite games typically have an odd number of NE.

## Algorithmic Game Theory
Algorithmic game theory bridges game theory and computer science, focusing on computational challenges in strategic settings. It analyzes algorithms using game-theoretic tools and designs mechanisms that are computationally efficient and robust to strategic behavior.
- **Key Metrics**:
  - **Price of Anarchy**: Ratio of worst NE welfare to optimal welfare, measuring efficiency loss due to selfish behavior.
  - **Price of Stability**: Ratio of best NE welfare to optimal welfare, indicating potential for efficient equilibria.
- **Computational Complexity**:
  - Computing NE is PPAD-complete, even for two-player games, indicating significant computational difficulty.
  - Correlated equilibria, where players follow a joint strategy distribution, can be computed efficiently using linear programming or no-regret learning.
- **Applications**:
  - **Auctions**: Designing mechanisms like Vickrey or VCG for efficient bidding.
  - **Internet Routing**: Modeling selfish routing in networks.
  - **Resource Allocation**: Fair division in distributed systems.
  - **Computational Social Choice**: Voting rules and coalition formation.

## Mechanism Design
Mechanism design, often called “reverse game theory,” involves creating games to achieve specific outcomes despite self-interested players. 
- **Incentive Compatibility**: Mechanisms where truth-telling is a dominant strategy (e.g., Vickrey auction, where bidders report true valuations).
- **Examples**:
  - **Vickrey Auction**: Second-price sealed-bid auction, ensuring truthful bidding.
  - **VCG Mechanism**: Generalizes Vickrey for multi-item auctions, maximizing social welfare.
- **Revelation Principle**: Any implementable outcome can be achieved by a mechanism where players truthfully report their preferences.

## Applications in Computer Science
- **Multi-agent Systems**: Agents coordinate or compete (e.g., distributed AI systems).
- **Auctions**: Online platforms like eBay or Google Ads use game-theoretic principles.
- **Network Games**: Routing protocols where users choose paths to minimize latency.
- **Security**: Models for intrusion detection or honeypot placement.
- **Cryptography**: Zero-knowledge proofs as games between prover and verifier.
- **AI**: Strategic decision-making in games like poker or Go.

## Mathematical Framework
- **Utility Functions**: Map outcomes to numerical values reflecting preferences.
- **Best Response**: A strategy maximizing a player’s payoff given others’ strategies.
- **Fixed-Point Theorems**: 
  - Brouwer’s fixed-point theorem underpins Nash’s existence proof.
  - Used to guarantee equilibrium in continuous strategy spaces.
- **Key Equations**:
  - For a player \( i \), strategy \( s_i \) is a best response if \( u_i(s_i, s_{-i}) \geq u_i(s_i', s_{-i}) \) for all alternative strategies \( s_i' \), where \( u_i \) is the utility function and \( s_{-i} \) are others’ strategies.
  - Mixed strategy NE: Probabilities \( p_i \) satisfy \( u_i(p_i, p_{-i}) = u_i(p_i', p_{-i}) \) for all strategies with positive probability.

## Tools and Software
- **Gambit**: Open-source tool for computing equilibria in finite games ([gambit.sourceforge.net](http://gambit.sourceforge.net)).
- **GAMUT**: Generates test games for algorithm evaluation ([gamut.stanford.edu](http://gamut.stanford.edu)).

## Further Reading
- *Lectures in Game Theory for Computer Scientists* by Apt & Grädel: Focuses on CS applications.
- *Algorithmic Game Theory* by Nisan, Roughgarden, Tardos, & Vazirani: Covers computational aspects.
- [MIT OpenCourseWare: Game Theory with Engineering Applications](https://ocw.mit.edu/courses/6-254-game-theory-with-engineering-applications-spring-2010/): Lecture notes with computational focus.
- [Game Theory - Wikipedia](https://en.wikipedia.org/wiki/Game_theory): General overview.
- [Algorithmic Game Theory - Wikipedia](https://en.wikipedia.org/wiki/Algorithmic_game_theory): CS-specific insights.