(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 distributor0 distributor1 - depot
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
    truck0 truck1 - truck
)
(:init
    (at hoist0 depot0) (available hoist0)
    (at hoist1 distributor0) (available hoist1)
    (at hoist2 distributor1) (available hoist2)
    (at truck0 distributor1)
    (at truck1 depot0)
    (at pallet0 depot0) (clear pallet0) (on crate5 pallet0)
    (at pallet1 distributor0) (clear pallet1)
    (at pallet2 distributor1) (clear pallet2) (on crate3 pallet2) (on crate2 crate3)
    (at pallet3 distributor0) (clear pallet3)
    (at pallet4 distributor0) (clear pallet4) (on crate4 pallet4) (on crate0 crate4)
    (at pallet5 distributor1) (clear pallet5) (on crate1 pallet5)
)
(:goal (and
    (on crate0 pallet3)
    (on crate1 crate4)
    (on crate3 pallet1)
    (on crate4 pallet5)
    (on crate5 crate1)
))
)
