(define (problem depot-problem)
  (:domain Depot)
  (:objects
    depot0 - depot
    distributor0 - distributor
    distributor1 - distributor
    hoist0 - hoist
    hoist1 - hoist
    hoist2 - hoist
    truck0 - truck
    truck1 - truck
    pallet0 - pallet
    pallet1 - pallet
    pallet2 - pallet
    crate0 - crate
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
  )
  (:init
    (at hoist0 depot0)
    (at truck0 depot0)
    (at pallet0 depot0)
    (at crate1 depot0)
    (on crate1 pallet0)
    (clear crate1)
    (available hoist0)

    (at hoist1 distributor0)
    (at truck1 distributor0)
    (at pallet1 distributor0)
    (at crate0 distributor0)
    (at crate3 distributor0)
    (at crate4 distributor0)
    (on crate0 pallet1)
    (on crate3 crate0)
    (on crate4 crate3)
    (clear crate4)
    (available hoist1)

    (at hoist2 distributor1)
    (at pallet2 distributor1)
    (at crate2 distributor1)
    (at crate5 distributor1)
    (on crate2 pallet2)
    (on crate5 crate2)
    (clear crate5)
    (available hoist2)
  )
  (:goal
    (and
      (on crate0 crate1)
      (on crate1 pallet2)
      (on crate2 pallet0)
      (on crate3 crate2)
      (on crate4 pallet1)
      (on crate5 crate0)
    )
  )
)
