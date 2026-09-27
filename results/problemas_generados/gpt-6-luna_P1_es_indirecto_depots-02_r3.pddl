(define (problem depot-problema)
  (:domain depot)
  (:objects
    crate0 crate1 crate2 crate3 crate4 crate5 - crate
    depot0 - depot
    distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    truck0 truck1 - truck
  )
  (:init
    (at crate1 depot0)
    (at crate4 distributor0)
    (at crate5 distributor1)
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)
    (at truck0 depot0)
    (at truck1 distributor0)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (clear crate1)
    (clear crate4)
    (clear crate5)
    (on crate1 pallet0)
    (on crate0 pallet1)
    (on crate3 crate0)
    (on crate4 crate3)
    (on crate2 pallet2)
    (on crate5 crate2)
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
