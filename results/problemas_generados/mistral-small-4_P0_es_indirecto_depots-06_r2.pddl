(define (problem pddl-problema)
(:domain Depot)
(:objects
    truck0 truck1 - truck
    hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
    depot0 depot1 depot2 - depot
    distributor0 distributor1 distributor2 - distributor
)
(:init
    (at truck0 depot1)
    (at truck1 depot2)
    (at hoist0 depot0)
    (at hoist1 depot1)
    (at hoist2 depot2)
    (at hoist3 distributor0)
    (at hoist4 distributor1)
    (at hoist5 distributor2)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (available hoist3)
    (available hoist4)
    (available hoist5)
    (at crate0 pallet1)
    (at crate1 pallet0)
    (at crate4 pallet2)
    (at crate5 pallet3)
    (on crate3 pallet5)
    (on crate2 crate3)
    (clear pallet4)
    (clear pallet0)
    (clear crate0)
    (clear crate1)
    (clear crate4)
    (clear crate5)
    (clear crate2)
)
(:goal (and
    (on crate0 crate4)
    (on crate2 pallet3)
    (on crate3 pallet0)
    (on crate4 pallet5)
))
)
