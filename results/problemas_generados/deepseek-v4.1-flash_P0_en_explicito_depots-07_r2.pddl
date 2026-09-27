(define (problem depot-problem)
 (:domain Depot)
 (:objects
   depot0 - depot
   distributor0 - distributor
   distributor1 - distributor
   truck0 - truck
   truck1 - truck
   hoist0 - hoist
   hoist1 - hoist
   hoist2 - hoist
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
   (at crate0 distributor0)
   (at crate1 distributor0)
   (at crate2 depot0)
   (at crate3 distributor0)
   (at crate4 distributor1)
   (at crate5 distributor0)
   (at crate6 distributor0)
   (at crate7 distributor1)
   (at crate8 distributor0)
   (at crate9 distributor1)
   (at hoist0 depot0)
   (at hoist1 distributor0)
   (at hoist2 distributor1)
   (at pallet0 depot0)
   (at pallet1 distributor0)
   (at pallet2 distributor1)
   (at pallet3 distributor1)
   (at pallet4 distributor0)
   (at pallet5 distributor0)
   (at truck0 distributor0)
   (at truck1 distributor0)
   (on crate0 pallet4)
   (on crate1 pallet1)
   (on crate2 pallet0)
   (on crate3 pallet5)
   (on crate4 pallet3)
   (on crate5 crate1)
   (on crate6 crate5)
   (on crate7 crate4)
   (on crate8 crate3)
   (on crate9 pallet2)
   (available hoist0)
   (available hoist1)
   (available hoist2)
   (clear crate0)
   (clear crate2)
   (clear crate6)
   (clear crate7)
   (clear crate8)
   (clear crate9)
 )
 (:goal
   (and
     (on crate0 pallet3)
     (on crate1 crate0)
     (on crate3 crate8)
     (on crate6 pallet2)
     (on crate7 pallet1)
     (on crate8 pallet4)
     (on crate9 pallet0)
   )
 )
)
