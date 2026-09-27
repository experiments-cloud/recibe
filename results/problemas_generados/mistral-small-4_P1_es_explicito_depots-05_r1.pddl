(define (problem depots-problema)
  (:domain Depot)
  (:objects
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 - crate
    depot0 - depot
    distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    truck0 truck1 - truck
  )
  (:init
    (at crate0 distributor1)
    (at crate1 depot0)
    (at crate2 distributor1)
    (
