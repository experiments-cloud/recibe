(define (problem depot-problem)
(:domain Depot)
(:objects
depot0 distributor0 distributor1 - place
hoist0 hoist1 hoist2 - hoist
pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
truck0 truck1 - truck
crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 - crate
)
(:init
(at hoist0 depot0) (at hoist1 distributor0) (at hoist2 distributor1)
(at truck0 distributor0) (at truck1 distributor0)
(at pallet0 depot0) (at pallet1 distributor0) (at pallet2 distributor1) (at pallet3 distributor1) (at pallet4 distributor0) (at pallet5 distributor0)
(at crate0 distributor0) (at crate1 distributor0) (at crate2 depot0) (at crate3 distributor1) (at crate4 distributor1) (at crate5 distributor0) (at crate6 distributor0) (at crate7 distributor1) (at crate8 distributor0) (at crate9 distributor1)
(on crate2 pallet0)
(on crate1 crate5) (on crate5 crate6) (on crate6 pallet1)
(on crate0 pallet4)
(on crate3 crate8) (on crate8 pallet5)
(on crate9 pallet2)
(on crate4 crate7) (on crate7 pallet3)
(clear crate1) (clear crate3) (clear crate4) (clear crate9)
(available hoist0) (available hoist1) (available hoist2)
)
(:goal (and
(on crate0 pallet3) (on crate1 crate0) (on crate3 crate8) (on crate6 pallet2)
(on crate7 pallet1) (on crate8 pallet4) (on crate9 pallet0)
))
)
