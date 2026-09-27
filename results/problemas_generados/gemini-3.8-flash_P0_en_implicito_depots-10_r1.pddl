(define (problem depot-prob)
(:domain Depot)
(:objects
    depot0 depot1 depot2 - depot
    distributor0 distributor1 distributor2 - distributor
    truck0 truck1 - truck
    hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
)
(:init
    (at hoist0 depot0)
    (available hoist0)
    (at truck1 depot0)
    (at pallet0 depot0)
    (at crate2 depot0)
    (on crate2 pallet0)
    (clear crate2)
    (at pallet7 depot0)
    (clear pallet7)
    (at pallet8 depot0)
    (at crate3 depot0)
    (on crate3 pallet8)
    (clear crate3)

    (at hoist1 depot1)
    (available hoist1)
    (at pallet1 depot1)
    (clear pallet1)

    (at hoist2 depot2)
    (available hoist2)
    (at pallet2 depot2)
    (at crate0 depot2)
    (on crate0 pallet2)
    (at crate1 depot2)
    (on crate1 crate0)
    (at crate5 depot2)
    (on crate5 crate1)
    (clear crate5)

    (at hoist3 distributor0)
    (available hoist3)
    (at pallet3 distributor0)
    (at crate4 distributor0)
    (on crate4 pallet3)
    (clear crate4)
    (at pallet9 distributor0)
    (clear pallet9)

    (at hoist4 distributor1)
    (available hoist4)
    (at truck0 distributor1)
    (at pallet4 distributor1)
    (clear pallet4)
    (at pallet6 distributor1)
    (clear pallet6)

    (at hoist5 distributor2)
    (available hoist5)
    (at pallet5 distributor2)
    (clear pallet5)
)
(:goal (and
    (on crate0 pallet0)
    (on crate1 pallet5)
    (on crate2 pallet4)
    (on crate3 pallet7)
    (on crate4 pallet9)
    (on crate5 pallet1)
))
)
