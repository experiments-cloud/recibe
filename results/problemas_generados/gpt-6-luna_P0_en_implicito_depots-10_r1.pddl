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
    pallet6 - pallet
    pallet7 - pallet
    pallet8 - pallet
    pallet9 - pallet
    crate0 - crate
    crate1 - crate
    crate2 - crate
    crate3 - crate
    crate4 - crate
    crate5 - crate
  )
  (:init
    (at hoist0 depot0)
    (at truck1 depot0)
    (at pallet0 depot0)
    (at pallet7 depot0)
    (at pallet8 depot0)
    (at hoist1 depot1)
    (at pallet1 depot1)
    (at hoist2 depot2)
    (at pallet2 depot2)
    (at hoist3 distributor0)
    (at pallet3 distributor0)
    (at pallet9 distributor0)
    (at hoist4 distributor1)
    (at truck0 distributor1)
    (at pallet4 distributor1)
    (at pallet6 distributor1)
    (at hoist5 distributor2)
    (at pallet5 distributor2)
    (on crate2 pallet0)
    (on crate3 pallet8)
    (on crate4 pallet3)
    (on crate0 pallet2)
    (on crate1 crate0)
    (on crate5 crate1)
    (clear crate2)
    (clear crate3)
    (clear crate4)
    (clear crate5)
    (clear pallet1)
    (clear pallet4)
    (clear pallet5)
    (clear pallet6)
    (clear pallet7)
    (clear pallet9)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (available hoist3)
    (available hoist4)
    (available hoist5)
  )
  (:goal
    (and
      (on crate0 pallet0)
      (on crate1 pallet5)
      (on crate2 pallet4)
      (on crate3 pallet7)
      (on crate4 pallet9)
      (on crate5 pallet1)
    )
  )
)
