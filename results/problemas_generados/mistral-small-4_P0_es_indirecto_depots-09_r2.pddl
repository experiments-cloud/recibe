(define (problem pddl_problem)
(:domain Depot)
(:objects
    hoist0 hoist1 hoist2 - hoist
    hoist3 - hoist
    hoist4 hoist5 - hoist
    pallet0 - pallet
    pallet1 - pallet
    pallet2 - pallet
    pallet3 - pallet
    pallet4 - pallet
    pallet5 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 - crate
    truck0 - truck
    truck1 - truck
    depot0 depot1 depot2 - depot
    distributor0 distributor1 distributor2 - distributor
)
(:init
    (at hoist0 depot0)
    (at pallet0 depot0)
    (clear pallet0)
    (on crate1 pallet0)
    (at hoist1 depot1)
    (at pallet1 depot1)
    (clear pallet1)
    (on crate0 pallet1)
    (on crate3 crate0)
    (at hoist2 depot2)
    (at pallet2 depot2)
    (clear pallet2)
    (on crate2 pallet2)
    (on crate4 crate2)
    (on crate5 crate4)
    (on crate9 crate5)
    (at hoist3 distributor0)
    (at pallet3 distributor0)
    (clear pallet3)
    (at hoist4 distributor1)
    (at pallet4 distributor1)
    (clear pallet4)
    (at hoist5 distributor2)
    (at pallet5 distributor2)
    (clear pallet5)
    (on crate6 pallet5)
    (on crate7 crate6)
    (on crate8 crate7)
    (at truck0 depot2)
    (at truck1 distributor0)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (available hoist3)
    (available hoist4)
    (available hoist5)
)
(:goal (and
    (on crate0 crate7)
    (on crate1 pallet4)
    (on crate2 pallet5)
    (on crate3 crate9)
    (on crate4 pallet0)
    (on crate5 pallet2)
    (on crate6 crate5)
    (on crate7 crate1)
    (on crate8 pallet3)
    (on crate9 crate2)
))
)
