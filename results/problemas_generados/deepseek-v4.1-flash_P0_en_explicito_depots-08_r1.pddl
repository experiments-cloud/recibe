(define (problem depot-problem)
  (:domain Depot)
  (:objects
    depot0 - depot
    distributor0 distributor1 - distributor
    truck0 truck1 - truck
    hoist0 hoist1 hoist2 - hoist
    pallet0 pallet1 pallet2 - pallet
    crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 - crate
  )
  (:init
    (at crate0 distributor1)
    (at crate1 depot0)
    (at crate2 distributor1)
    (at crate3 distributor0)
    (at crate4 distributor0)
    (at crate5 distributor1)
    (at crate6 depot0)
    (at crate7 distributor0)
    (at crate8 distributor0)
    (at crate9 distributor0)
    (at crate10 distributor1)
    (at crate11 depot0)
    (at crate12 distributor0)
    (at crate13 distributor0)
    (at crate14 distributor0)

    (at hoist0 depot0)
    (at hoist1 distributor0)
    (at hoist2 distributor1)

    (at pallet0 depot0)
    (at pallet1 distributor0)
    (at pallet2 distributor1)

    (at truck0 distributor1)
    (at truck1 depot0)

    (on crate0 pallet2)
    (on crate1 pallet0)
    (on crate2 crate0)
    (on crate3 pallet1)
    (on crate4 crate3)
    (on crate5 crate2)
    (on crate6 crate1)
    (on crate7 crate4)
    (on crate8 crate7)
    (on crate9 crate8)
    (on crate10 crate5)
    (on crate11 crate6)
    (on crate12 crate9)
    (on crate13 crate12)
    (on crate14 crate13)

    (available hoist0)
    (available hoist1)
    (available hoist2)

    (clear crate10)
    (clear crate11)
    (clear crate14)
  )
  (:goal
    (and
      (on crate0 crate8)
      (on crate1 crate9)
      (on crate10 crate4)
      (on crate11 crate5)
      (on crate12 pallet2)
      (on crate2 crate1)
      (on crate3 crate12)
      (on crate4 crate11)
      (on crate5 crate0)
      (on crate8 pallet0)
      (on crate9 pallet1)
    )
  )
)
