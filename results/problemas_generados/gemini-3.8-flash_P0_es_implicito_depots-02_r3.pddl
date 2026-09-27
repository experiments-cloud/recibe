(define (problem depot-prob)
(:domain Depot)
(:objects
    depot0 - depot
    distributor0 distributor1 - distributor
    truck0 truck1 - truck
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
)
(:init
    (at hoist0 depot0)
    (available hoist0)
    (at truck0 depot0)
    (at pallet0 depot0)
    (at crate1 depot0)
    (on crate1 pallet0)
    (clear crate1)

    (at hoist1 distributor0)
    (available hoist1)
    (at truck1 distributor0)
    (at pallet1 distributor0)
    (at crate0 distributor0)
    (at crate3 distributor0)
    (at crate4 distributor0)
    (on crate0 pallet1)
    (on crate3 crate0)
    (on crate4 crate3)
    (clear crate4)

    (at hoist2 distributor1)
    (available hoist2)
    (at pallet2 distributor1)
    (at crate2 distributor1)
    (at crate5 distributor1)
    (on crate2 pallet2)
    (on crate5 crate2)
    (clear crate5)
)
(:goal (and
    (on crate0 crate1)
    (on crate1 pallet2)
    (on crate2 pallet0)
    (on crate3 crate2)
    (on crate4 pallet1)
    (on crate5 crate0)
))
)
