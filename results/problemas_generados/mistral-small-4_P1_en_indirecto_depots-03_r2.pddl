(define (problem depot-problem)
  (:domain Depot)
  (:objects
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 - crate
    depot0 - depot
    distributor0 distributor1 - distributor
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    truck0 truck1 - truck
  )
  (:init
    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)
    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)
    (at truck0 distributor1)
    (at truck1 distributor1)
    (available hoist0)
    (available hoist1)
    (available hoist2)
    (clear crate3)
    (clear crate7)
    (clear pallet0)
    (clear pallet1)
    (clear pallet2)
    (on crate0 crate1)
    (on crate1 crate4)
    (on crate2 pallet1)
    (on crate3 crate5)
    (on crate4 crate7)
    (on crate5 crate6)
    (on crate6 crate3)
    (on crate7 pallet0)
  )
  (:goal (and
    (on crate0 crate4)
    (on crate2 crate6)
    (on crate4 crate7)
    (on crate5 pallet2)
    (on crate6 pallet1)
    (on crate7 pallet0)
  ))
)
