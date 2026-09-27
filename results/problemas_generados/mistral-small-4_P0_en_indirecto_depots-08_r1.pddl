(define (problem DepotProblem)
(:domain Depot)
(:objects
    depot0 - depot
    distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    pallet0 - pallet
    pallet1 - pallet
    pallet2 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 - crate
    truck0 truck1 - truck
)
(:init
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)
    (at truck0 distributor1)
    (at truck1 depot0)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (clear pallet0)
    (clear pallet1)
    (clear pallet2)
    (on crate11 pallet0)
    (on crate6 crate11)
    (on crate1 crate6)
    (on crate14 pallet1)
    (on crate13 crate14)
    (on crate12 crate13)
    (on crate9 crate12)
    (on crate8 crate9)
    (on crate7 crate8)
    (on crate4 crate7)
    (on crate3 crate4)
    (on crate10 pallet2)
    (on crate5 crate10)
    (on crate2 crate5)
    (on crate0 crate2)
)
(:goal (and
    (on crate0 crate8)
    (on crate1 crate9)
    (on crate10 crate4)
    (on crate11 crate5)
    (on crate12 pallet2)
    (on crate2 crate1)
    (on crate3 crate12)
    (on crate4 crate11)
    (on crate5 crate0)
    (on crate8 pallet0)
    (on crate9 pallet1)
))
)
