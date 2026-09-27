(define (problem depot-problem)
  (:domain Depot)
  (:objects
    depot0 - depot
    distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    truck0 truck1 - truck
    pallet0 pallet1 pallet2 - pallet
    crate0 crate1 crate2 crate3 - crate
  )
  (:init
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at truck0 depot0)
    (at truck1 depot0)
    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)
    (on crate0 pallet0)
    (on crate3 pallet1)
    (on crate1 pallet2)
    (on crate2 crate1)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (clear crate2)
  )
  (:goal
    (and
      (on crate0 pallet2)
      (on crate1 crate3)
      (on crate2 pallet0)
      (on crate3 pallet1)
    )
  )
)
