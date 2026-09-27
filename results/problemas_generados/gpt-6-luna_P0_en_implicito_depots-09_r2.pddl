(define (problem depot-problem)
  (:domain Depot)
  (:objects
    depot0 - depot
    depot1 - depot
    depot2 - depot
    distributor0 - distributor
    distributor1 - distributor
    distributor2 - distributor
    hoist0 - hoist
    hoist1 - hoist
    hoist2 - hoist
    hoist3 - hoist
    hoist4 - hoist
    hoist5 - hoist
    truck0 - truck
    truck1 - truck
    pallet0 - pallet
    pallet1 - pallet
    pallet2 - pallet
    pallet3 - pallet
    pallet4 - pallet
    pallet5 - pallet
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
    (at hoist1 depot1)
    (at pallet1 depot1)
    (at hoist2 depot2)
    (at truck0 depot2)
    (at pallet2 depot2)
    (at hoist3 distributor0)
    (at truck1 distributor0)
    (at pallet3 distributor0)
    (at hoist4 distributor1)
    (at pallet4 distributor1)
    (at hoist5 distributor2)
    (at pallet5 distributor2)
    (on crate1 pallet0)
    (on crate0 pallet1)
    (on crate3 crate0)
    (on crate2 pallet2)
    (on crate4 crate2)
    (on crate5 crate4)
    (on crate9 crate5)
    (on crate6 pallet5)
    (on crate7 crate6)
    (on crate8 crate7)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (available hoist3)
    (available hoist4)
    (available hoist5)
    (clear crate1)
    (clear crate3)
    (clear crate9)
    (clear pallet3)
    (clear pallet4)
    (clear crate8)
  )
  (:goal
    (and
      (on crate0 crate7)
      (on crate1 pallet4)
      (on crate2 pallet5)
      (on crate3 crate9)
      (on crate4 pallet0)
      (on crate5 pallet2)
      (on crate6 crate5)
      (on crate7 crate1)
      (on crate8 pallet3)
      (on crate9 crate2)
    )
  )
)
