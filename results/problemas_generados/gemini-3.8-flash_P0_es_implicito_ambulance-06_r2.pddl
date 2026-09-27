(define (problem transport-patients)
  (:domain ambulance)
  (:objects
    l1 l2 l3 l4 - location
    amb1 amb2 - ambulance
    p1 p2 - patient
  )
  (:init
    (connected l1 l2)
    (connected l2 l1)
    (connected l1 l4)
    (connected l4 l1)
    (connected l2 l3)
    (connected l3 l2)
    (connected l3 l4)
    (connected l4 l3)
    (hospital l3)
    (ambulance-at amb1 l3)
    (ambulance-at amb2 l3)
    (empty amb1)
    (empty amb2)
    (patient-at p1 l2)
    (patient-at p2 l2)
  )
  (:goal
    (and
      (patient-at p1 l3)
      (patient-at p2 l3)
    )
  )
)
