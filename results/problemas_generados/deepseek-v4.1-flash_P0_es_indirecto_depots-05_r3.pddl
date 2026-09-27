(define (problem depot-problem)
  (:domain Depot)
  (:requirements :typing)
  (:objects
    depot0 - depot
    distributor0 - distributor
    distributor1 - distributor
    hoist0 - hoist
    hoist1 - hoist
    hoist2 - hoist
    pallet0 - pallet
    pallet1 - pallet
    pallet2 - pallet
    truck0 - truck
    truck1 - truck
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
    (at pallet0 depot0)
    (at hoist1 distributor0)
    (at pallet1 distributor0)
    (at hoist2 distributor1)
    (at pallet2 distributor1)
    (at truck0 depot0)
    (at truck1 distributor0)
    (at crate1 depot0)
    (at crate3 depot0)
    (at crate4 depot0)
    (at crate6 distributor0)
    (at crate7 distributor0)
    (at crate8 distributor0)
    (at crate0 distributor1)
    (at crate2 distributor1)
    (at crate5 distributor1)
    (at crate9 distributor1)
    (on crate1 pallet0)
    (on crate3 crate1)
    (on crate4 crate3)
    (on crate6 pallet1)
    (on crate7 crate6)
    (on crate8 crate7)
    (on crate0 pallet2)
    (on crate2 crate0)
    (on crate5 crate2)
    (on crate9 crate5)
    (clear crate4)
    (clear crate8)
    (clear crate9)
    (available hoist0)
    (available hoist1)
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
