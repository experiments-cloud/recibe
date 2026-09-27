(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    truck0 truck1 - truck
    pallet0 pallet1 pallet2 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 - crate
)
(:init
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at truck0 distributor1)
    (at truck1 distributor1)
    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (on crate0 crate1)
    (on crate1 crate4)
    (on crate4 crate7)
    (on crate3 crate5)
    (on crate5 crate6)
    (clear crate0)
    (clear crate2)
    (clear crate3)
)
(:goal (and
    (on crate0 crate4)
    (on crate2 crate6)
    (on crate4 crate7)
    (on crate5 pallet2)
    (on crate6 pallet1)
    (on crate7 pallet0)
))
)
