(define (problem depot-problem)
  (:domain Depot)
  (:objects
    depot0 - depot
    depot1 - depot
    depot2 - depot
    distributor0 - distributor
    distributor1 - distributor
    distributor2 - distributor
    truck0 - truck
    truck1 - truck
    hoist0 - hoist
    hoist1 - hoist
    hoist2 - hoist
    hoist3 - hoist
    hoist4 - hoist
    hoist5 - hoist
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
  )
  (:init
    (at crate0 depot1)
    (at crate1 depot0)
    (at crate2 distributor2)
    (at crate3 distributor2)
    (at crate4 depot2)
    (at crate5 distributor0)
    (at hoist0 depot0)
    (at hoist1 depot1)
    (at hoist2 depot2)
    (at hoist3 distributor0)
    (at hoist4 distributor1)
    (at hoist5 distributor2)
    (at pallet0 depot0)
    (at pallet1 depot1)
    (at pallet2 depot2)
    (at pallet3 distributor0)
    (at pallet4 distributor1)
    (at pallet5 distributor2)
    (at truck0 depot1)
    (at truck1 depot2)
    (on crate0 pallet1)
    (on crate1 pallet0)
    (on crate2 pallet5)
    (on crate3 crate2)
    (on crate4 pallet2)
    (on crate5 pallet3)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (available hoist3)
    (available hoist4)
    (available hoist5)
    (clear crate0)
    (clear crate1)
    (clear crate3)
    (clear crate4)
    (clear crate5)
    (clear pallet4)
  )
  (:goal
    (and
      (on crate0 crate4)
      (on crate2 pallet3)
      (on crate3 pallet0)
      (on crate4 pallet5)
    )
  )
)
