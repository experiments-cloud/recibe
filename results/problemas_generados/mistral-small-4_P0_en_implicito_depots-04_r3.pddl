(define (problem DepotProblem)
(:domain Depot)
(:objects
  depot0 distributor0 distributor1 - place
  truck0 truck1 - truck
  hoist0 hoist1 hoist2 - hoist
  pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
  crate0 crate1 crate2 crate3 crate4 crate5 - crate
)
(:init
  (at hoist0 depot0)
  (at hoist1 distributor0)
  (at hoist2 distributor1)
  (at truck0 distributor1)
  (at truck1 depot0)
  (at pallet0 depot0)
  (at pallet1 distributor0)
  (at pallet2 distributor1)
  (at pallet3 distributor0)
  (at pallet4 distributor0)
  (at pallet5 distributor1)
  (on crate5 pallet0)
  (on crate4 crate0)
  (on crate3 crate2)
  (on crate1 pallet5)
  (clear crate1)
  (clear crate3)
  (clear pallet1)
  (clear pallet2)
  (clear pallet4)
  (clear pallet5)
  (available hoist0)
  (available hoist1)
  (available hoist2)
)
(:goal (and
  (on crate0 pallet3)
  (on crate1 crate4)
  (on crate3 pallet1)
  (on crate4 pallet5)
  (on crate5 crate1)
))
)
