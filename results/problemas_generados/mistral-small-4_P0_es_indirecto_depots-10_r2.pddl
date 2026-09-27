(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 depot1 depot2 distributor0 distributor1 distributor2 - place
    hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist
    truck0 truck1 - truck
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
)
(:init
    (at hoist0 depot0) (at hoist1 depot1) (at hoist2 depot2)
    (at hoist3 distributor0) (at hoist4 distributor1) (at hoist5 distributor2)
    (at truck0 distributor1) (at truck1 depot0)
    (available hoist0) (available hoist1) (available hoist2)
    (available hoist3) (available hoist4) (available hoist5)
    (on crate2 pallet0) (clear crate2)
    (on crate3 pallet8) (clear crate3)
    (on crate5 pallet2) (on crate1 crate5) (on crate0 crate1) (clear crate0)
    (on crate4 pallet3) (clear crate4)
)
(:goal (and
    (on crate0 pallet0)
    (on crate1 pallet5)
    (on crate2 pallet4)
    (on crate3 pallet7)
    (on crate4 pallet9)
    (on crate5 pallet2)
))
)
