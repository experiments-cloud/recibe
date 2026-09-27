(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 depot1 depot2 distributor0 distributor1 distributor2 - depot
    hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
    truck0 truck1 - truck
)
(:init
    (at hoist0 depot0) (available hoist0)
    (at hoist1 depot1) (available hoist1)
    (at hoist2 depot2) (available hoist2)
    (at hoist3 distributor0) (available hoist3)
    (at hoist4 distributor1) (available hoist4)
    (at hoist5 distributor2) (available hoist5)
    (at pallet0 depot0) (at pallet1 depot1) (at pallet2 depot2)
    (at pallet3 distributor0) (at pallet4 distributor1) (at pallet5 distributor2)
    (at crate0 pallet1) (at crate1 pallet0) (at crate4 pallet2)
    (at crate5 pallet3)
    (on crate3 crate2) (at crate2 pallet5)
    (at crate3 pallet5)
    (clear crate0) (clear crate1) (clear crate4) (clear crate5)
    (clear crate3)
    (at truck0 depot1)
    (at truck1 depot2)
)
(:goal (and
    (on crate0 crate4)
    (on crate2 pallet3)
    (on crate3 pallet0)
    (on crate4 pallet5)
))
)
