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
    crate6 - crate
    crate7 - crate
    crate8 - crate
    crate9 - crate
  )
  (:init
    (at hoist0 depot0)
    (at truck0 depot0)
    (at pallet0 depot0)
    (at crate4 depot0)
    (on crate1 pallet0)
    (on crate3 crate1)
    (on crate4 crate3)
    (clear crate4)
    (available hoist0)

    (at hoist1 distributor0)
    (at truck1 distributor0)
    (at pallet1 distributor0)
    (at crate8 distributor0)
    (on crate6 pallet1)
    (on crate7 crate6)
    (on crate8 crate7)
    (clear crate8)
    (available hoist1)

    (at hoist2 distributor1)
    (at pallet2 distributor1)
    (at crate9 distributor1)
    (on crate0 pallet2)
    (on crate2 crate0)
    (on crate5 crate2)
    (on crate9 crate5)
    (clear crate9)
    (available hoist2)
  )
  (:goal
    (and
      (on crate0 crate5)
      (on crate1 pallet1)
      (on crate2 crate0)
      (on crate3 pallet2)
      (on crate4 crate6)
      (on crate5 crate4)
      (on crate6 crate9)
      (on crate7 crate1)
      (on crate8 crate3)
      (on crate9 pallet0)
    )
  )
)
