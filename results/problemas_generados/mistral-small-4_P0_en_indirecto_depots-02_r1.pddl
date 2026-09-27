(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 distributor0 distributor1 - depot
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
    truck0 truck1 - truck
)
(:init
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at truck0 depot0)
    (at truck1 distributor0)
    (at crate0 distributor0)
    (on crate0 crate3)
    (on crate3 crate4)
    (at crate1 depot0)
    (on crate1 pallet0)
    (at crate2 distributor1)
    (on crate2 pallet2)
    (at crate3 distributor0)
    (at crate4 distributor0)
    (at crate5 distributor1)
    (on crate5 crate2)
    (clear crate0)
    (clear crate5)
    (clear pallet1)
    (clear pallet2)
    (available hoist0)
    (available hoist1)
    (available hoist2)
)
(:goal (and
    (on crate0 crate1)
    (on crate1 pallet1)
    (on crate2 pallet0)
    (on crate3 crate2)
    (on crate4 pallet1)
    (on crate5 crate0)
))
)
