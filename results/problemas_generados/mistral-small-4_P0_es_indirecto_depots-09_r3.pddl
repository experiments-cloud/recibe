(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 depot1 depot2 distributor0 distributor1 distributor2 - place
    hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
    truck0 truck1 - truck
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 - crate
)
(:init
    (at hoist0 depot0) (available hoist0) (at pallet0 depot0) (clear pallet0)
    (at hoist1 depot1) (available hoist1) (at pallet1 depot1) (clear pallet1)
    (at hoist2 depot2) (available hoist2) (at pallet2 depot2) (clear pallet2)
    (at hoist3 distributor0) (available hoist3) (at pallet3 distributor0) (clear pallet3)
    (at hoist4 distributor1) (available hoist4) (at pallet4 distributor1) (clear pallet4)
    (at hoist5 distributor2) (available hoist5) (at pallet5 distributor2) (clear pallet5)
    (at truck0 depot2)
    (at truck1 distributor0)
    (at crate1 pallet0)
    (on crate3 pallet1) (at crate3 depot1) (clear crate3)
    (on crate0 crate3) (at crate0 depot1)
    (on crate9 pallet2) (at crate9 depot2) (clear crate9)
    (on crate5 crate9) (at crate5 depot2)
    (on crate4 crate5) (at crate4 depot2)
    (on crate2 crate4) (at crate2 depot2)
    (on crate8 pallet5) (at crate8 distributor2) (clear crate8)
    (on crate7 crate8) (at crate7 distributor2)
    (on crate6 crate7) (at crate6 distributor2)
)
(:goal (and
    (on crate0 crate7)
    (at crate1 pallet4)
    (at crate2 pallet5)
    (on crate3 crate9)
    (at crate4 pallet0)
    (at crate5 pallet2)
    (on crate6 crate5)
    (on crate7 crate1)
    (at crate8 pallet3)
    (on crate9 crate2)
))
)
